"""
service.py

Prediction service.
"""

import ast
import json
import traceback
import uuid
from dataclasses import asdict
from datetime import datetime
from importlib import import_module
from typing import Dict

from cognite.client import CogniteClient
from cognite.client.exceptions import CogniteNotFoundError

from akerbp.mlops.core import config
from akerbp.mlops.core.exceptions import MissingFieldError
from akerbp.mlops.core.helpers import input_data_validation, response_validation
from akerbp.mlops.core.logger import get_logger

logger = get_logger(__name__)
c = config.read_service_settings()
try:
    model_module = import_module(c.model_import_path)
except Exception as e:
    settings_dataclass = {k: str(v) for k, v in asdict(c).items()}
    raise Exception("Something failed when trying to import your model's code!") from e

predict = model_module.predict
_initialization = model_module.initialization
ModelException = model_module.ModelException


def initialization(secrets: Dict) -> None:
    """
    Read initialization object required by `predict`
    """
    # This check adds a little overhead to each prediction
    if "init_object" not in globals():
        global init_object
        artifact_folder = c.artifact_folder
        init_object = _initialization(artifact_folder, secrets)  # type: ignore


def parse_payload(input_data: Dict, client: CogniteClient) -> Dict:
    input_wells = input_data["input"]

    for i, well_data in enumerate(input_wells):
        if input_file_reference := well_data.get("input_file_reference", ""):
            logger.info(
                f"Received input file reference: {input_file_reference}. Downloading input logs from CDF"
            )
            try:
                start = datetime.now()
                bytes_data = client.files.download_bytes(
                    external_id=input_file_reference
                )
                input_logs = json.loads(bytes_data)
                input_data["input"][i]["input_logs"] = input_logs
                logger.info(
                    f"Downloading input logs from file reference took {datetime.now() - start} s!"
                )
            except Exception as e:
                raise Exception(
                    f"Failed to load input file from CDF for file reference {well_data['input_file_reference']}"
                ) from e
        else:
            logger.warning(
                "DeprecationWarning: Sending input logs directly to the model will soon be deprecated. Migrate to sending a reference to input files in CDF using the 'input_file_reference' field to suppress this warning",
            )

    return input_data


def service(data: Dict, secrets: Dict, platform: str = "cdf") -> Dict:
    """
    Generate prediction for an input
    If the input dictionary (data) contains a key-value pair "return_file" = True,
    the resulting predictions are uploaded to Files in CDF.
    The response will now contain a field 'prediction_file' with a reference to a binary file
    containing the predictions. Otherwise, i.e. if "return_file" = False or the input dictionary does
    not contain a "return_file" key, the predictions are passed to the 'prediction' field of the response,
    and the field 'prediction_file' is set to False.

    Inputs:
        data: input to the model (sent by a user through the API)
        secrets: api keys that the model may need during initialization
    Output:
        Dictionary containing the function call response with a status field ('ok' or 'error').
        If status is 'ok' the response will have fields for 'prediction' and 'prediction_file'
        Otherwise, the response contains a field 'message' with the corresponding error message
    """
    completed_successfully = True
    try:
        if platform == "cdf":
            import akerbp.mlops.cdf.helpers as mlops_helpers

            mlops_helpers.client_secrets = secrets
            mlops_helpers.set_up_cdf_client(context="write")
        logger.info("Initializing model")
        initialization(secrets)
        logger.info("Model initialized")

        data = parse_payload(
            input_data=data, client=mlops_helpers.global_client["read"]
        )

        try:
            skip_input_validation = ast.literal_eval(
                str(c.info["prediction"]["metadata"]["supports_external_retrieval"])
            )
        except KeyError as e:
            raise MissingFieldError(
                "Field 'supports_external_retrieval' is missing from the metadata specification in mlops_settings.yaml"
            ) from e
        if skip_input_validation:
            logger.info(
                "Skipping input data validation as data is retrieved externally"
            )
            logger.info(
                "Call predict on the initialized model using the retrieved data"
            )
        else:
            logger.info("Performing input data validation")
            required_input = ast.literal_eval(
                str(c.info["prediction"]["metadata"]["required_input"])
            )
            is_input_data_valid = input_data_validation(
                required_input=required_input,
                input_payload=data,
            )
            if is_input_data_valid:
                logger.info("Input data successfully validated")
            else:
                raise KeyError(
                    f"Payload is missing at least one of the required curves: {required_input}"
                )
            logger.info(
                "Call predict on the initialized model using the provided payload"
            )
        y = predict(data, init_object, secrets)  # type: ignore
        logger.info("Performing response validation")
        is_response_valid = response_validation(response=y)
        if is_response_valid:
            logger.info("Response succesfully validated")
        else:
            raise Exception(
                "Response structure is invalid. See above warning for the set of required fields in the response"
            )

        logger.info("Predictions obtained")
        write_predictions_to_file = data.get("return_file", False)
        if write_predictions_to_file:
            logger.info("Writing predictions to file")
            if platform == "cdf":
                import base64

                public_key = data.get("public_key", None)
                content = str(json.dumps(y))
                data_encrypted = False
                if public_key is None:
                    logger.warning(
                        "Public key is not provided. The predictions will not be encrypted. This is not recommended!"
                    )
                    encrypted_content = None
                    encrypted_key = None
                else:
                    import os

                    from cryptography.hazmat.primitives import hashes, padding
                    from cryptography.hazmat.primitives.asymmetric import (
                        padding as asym_padding,
                    )
                    from cryptography.hazmat.primitives.ciphers import (
                        Cipher,
                        algorithms,
                        modes,
                    )
                    from cryptography.hazmat.primitives.serialization import (
                        load_pem_public_key,
                    )

                    logger.info("Encrypting predictions")
                    # Encrypt content with AES
                    key = os.urandom(32)
                    iv = b"1234567890123456"
                    algo = algorithms.AES(key)
                    encryptor = Cipher(algo, modes.CBC(iv)).encryptor()
                    padder = padding.PKCS7(algo.block_size).padder()
                    padded_data = padder.update(content.encode()) + padder.finalize()
                    encrypted_content = (
                        encryptor.update(padded_data) + encryptor.finalize()
                    )
                    logger.info("Encrypting AES key with RSA public key")
                    # Encrypt key with RSA public key
                    public_key = load_pem_public_key(
                        public_key.encode(),
                    )
                    encrypted_key = public_key.encrypt(
                        key,
                        asym_padding.OAEP(
                            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None,
                        ),
                    )
                    data_encrypted = True
                    logger.info("Predictions encrypted")
                cdf_client = mlops_helpers.global_client["write"]
                prediction_id = uuid.uuid4().hex
                external_file_id = f"{c.model_name}_predictions_{prediction_id}.binary"
                try:
                    cdf_client.files.delete(external_id=external_file_id)
                except CogniteNotFoundError:
                    pass
                cdf_client.files.upload_bytes(
                    content=encrypted_content
                    if encrypted_content is not None
                    else content,
                    name=f"{c.model_name}_predictions_{prediction_id}",
                    external_id=external_file_id,
                )
                logger.info(f"Prediction file uploaded to {external_file_id}")
                return {
                    "status": "ok",
                    "prediction": {},
                    "prediction_file": external_file_id,
                    "model_id": c.model_id,
                    "data_encrypted": data_encrypted,
                    "encrypted_key": base64.b64encode(encrypted_key).decode()
                    if encrypted_key is not None
                    else None,
                }
            elif platform == "gc":
                raise NotImplementedError
            else:
                raise ValueError(f"Platform {platform} is not supported")
        else:
            logger.info("Writing predictions to the response")
            return {
                "status": "ok",
                "prediction": y,
                "prediction_file": "",
                "model_id": c.model_id,
            }
    except KeyError:
        completed_successfully = False
        error_message = "Unable to obtain a prediction with the provided payload"
        tb = traceback.format_exc()
    except ModelException:
        completed_successfully = False
        error_message = "Could not get a prediction"
        tb = traceback.format_exc()
    except Exception:
        completed_successfully = False
        error_message = ""
        tb = traceback.format_exc()
    finally:
        if not completed_successfully:
            error_message += f" See the traceback for more details:\n{tb}"
            logger.error(error_message)
    return {"status": "error", "message": error_message, "model_id": c.model_id}
