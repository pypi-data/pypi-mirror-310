"""
cdf_helpers.py

High level functionality built on top of Cognite's Python SDK

Most functions require the global cdf client to be set up before using them.
"""

import functools
import json
import os
import sys
import time
import traceback
from dataclasses import asdict
from datetime import datetime
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from shutil import make_archive, unpack_archive
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union, cast

import pandas as pd
from cognite.client import CogniteClient
from cognite.client.config import global_config
from cognite.client.data_classes import FileMetadata, FileMetadataUpdate, Function
from cognite.client.exceptions import CogniteAPIError, CogniteNotFoundError

from akerbp.mlops.core import config, exceptions
from akerbp.mlops.core.helpers import confirm_prompt
from akerbp.mlops.core.logger import get_logger

global_config.disable_pypi_version_check = True
logger = get_logger(__name__)


global_client: Dict[str, CogniteClient] = {}
client_secrets = config.client_secrets

env_vars = config.ENV_VARS


def set_up_cdf_client(context: str = "read") -> None:
    """
    Set up the global client used by most helpers. This needs to be called
    before using any helper.

    Args:
        context (str): either 'read', 'write'. Defaults to 'read'
    """
    client_secret_labels = []
    if context == "read":
        client_secret_labels.append("read")
    elif context == "write":
        client_secret_labels.extend(["read", "write"])
    else:
        raise ValueError("Context should be either 'read', 'write'")

    for k in client_secret_labels:
        if k not in global_client:
            global_client[k] = get_client(
                client_id=client_secrets[f"id-{k}"],
                client_secret=client_secrets[f"secret-{k}"],
                tenant_id=client_secrets["tenant-id"],
                base_url=client_secrets["base-url"],
            )


def get_client(
    client_id: str,
    client_secret: str,
    tenant_id: Optional[str] = None,
    base_url: Optional[str] = None,
) -> CogniteClient:
    """
    Create a CDF client with a given client id and secret

    Args:
        client_id (string): client id for the CDF project
        client_secret (string): client secret for the CDF project
    Returns:
        (CogniteClient): Cognite client to interact with CDF
    """
    from cognite.client import ClientConfig, CogniteClient
    from cognite.client.credentials import OAuthClientCredentials

    # input checks
    if base_url is None:
        base_url = client_secrets["base-url"]
        if base_url is None:
            raise ValueError(
                "base_url is not set. Cannot create a Cognite client without the OIDC base url used in defining scopes."
            )

    if tenant_id is None:
        tenant_id = client_secrets["tenant-id"]
        if tenant_id is None:
            raise ValueError(
                "tenant_id is not set. Cannot create a Cognite client without the tenant id used in defining the token url."
            )

    creds = OAuthClientCredentials(
        token_url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=[f"{base_url}/.default"],
    )

    project = "akbp-subsurface"
    cnf = ClientConfig(
        client_name="mlops-client",
        project=project,
        credentials=creds,
        base_url=base_url,
    )

    client = CogniteClient(cnf)
    # assert client.login.status().logged_in
    return client


def validate_function_name(function_name: str, verbose: bool = True) -> bool:
    """
    Validate that function name follows MLOps standard: model-service-env
    Updated to still return true if the external id of the function does
    not follow the mlops convention, to allow listing arbitrary functions.

    Args:
        function_name (string): function name to validate
        verbose (bool, optional): whether to print a warning if the function name is not valid.
            Defaults to True

    Returns:
        (bool): True if name is valid, False otherwise
    """
    supported_services = ["prediction", "training"]
    supported_environments = ["dev", "test", "prod"]
    # Check external id using mlops convention
    try:
        if len(splitted_function_name := function_name.split("-")) > 3:
            _, service, environment, _ = splitted_function_name
        elif len(splitted_function_name) == 3:
            _, service, environment = splitted_function_name
        else:
            _, service, environment = None, None, None
    except ValueError:
        if verbose:
            m = f"Expected function name format: 'model-service-environment', got {function_name}"
            logger.error(m)
        return True
    if service not in supported_services:
        if verbose:
            m = f"Supported services: {supported_services}, got {service} from {function_name}"
            logger.error(m)
        return True
    if environment not in supported_environments:
        if verbose:
            m = f"Supported environments: {supported_environments}, got {environment} from {function_name}"
            logger.error(m)
        return True
    return True


def delete_function(function_name: str, confirm: bool = True) -> None:
    """
    Delete a deployed function

    Args:
        function_name (string): external id of function to delete
        confirm: (bool, optional) whether the user will be asked to confirm deletion.
            Defaults to True
    """
    if not validate_function_name(function_name):
        raise exceptions.FunctionNameError(f"Function name {function_name} is invalid")

    if len(splitted_function_name := function_name.split("-")) > 3:
        model, service, environment, version = splitted_function_name
    else:
        model, service, environment = splitted_function_name

    confirmed = False

    if confirm:
        if len(splitted_function_name) > 3:
            question = f"Delete {model=}, {service=}, {environment=}, {version=}?"
        else:
            question = f"Delete {model=}, {service=}, {environment=}?"
        confirmed = confirm_prompt(question)

    if not confirm or confirmed:
        client = global_client["write"]
        try:
            client.functions.delete(external_id=function_name)
            logger.info(f"Deleted function with external id {function_name}")
        except CogniteNotFoundError:
            logger.error(f"Couldn't find function with external id {function_name}")


def create_function_from_folder(
    human_readable_name: str,
    function_name: str,
    folder: str,
    handler_path: str,
    python_runtime: str,
    description: str = "",
    metadata: Optional[Dict[str, str]] = None,
    owner: str = "",
    secrets: Optional[Dict[str, str]] = None,
) -> Any:
    """
    Create a Cognite function from a folder. Any existing function with the same
    external id is overwritten if it already exist in CDF.

    Args:
        human_readable_name (str): name of function to create
        function_name (str): external id of function to create
        folder (str): path where the source code is located
        handler_path (str): path to the handler file
        python_runtime (str): Python runtime to use for the function
        description (string): model description
        metadata (Dict[str, str], optional): model metadata
            Defaults to an empty dictionary.
        owner (str): the function's owner's email
        secrets (Dict[str, Any], optional): Client secrets or similar that should be passed to the function.
            Defaults to an empty dictionary.

    Returns:
        (Any): the created function
    """
    if secrets is None:
        secrets = {}
    if metadata is None:
        metadata = {}
    client = global_client["write"]

    try:
        client.functions.delete(external_id=function_name)
        logger.info(
            f"Function {human_readable_name} with external id {function_name} already exist and will be overwritten"
        )
    except CogniteNotFoundError:
        logger.info(
            f"Function {human_readable_name} with external id {function_name} does not exist and will be created"
        )
        pass

    envs = {
        **asdict(env_vars),
        "DEPLOYMENT_PLATFORM": "cdf",
    }  # ensure CDFLogger is used
    envs = {k.upper(): str(v) for k, v in envs.items() if v is not None}
    try:
        function = client.functions.create(
            name=human_readable_name,
            folder=folder,
            function_path=handler_path,
            external_id=function_name,
            description=description,
            metadata=metadata,
            runtime=python_runtime,
            owner=owner,
            secrets=secrets,
            env_vars=envs,
        )
        logger.info(f"Environment variables: {envs}")
        logger.info(
            f"Starting deployment of function {human_readable_name} with external id {function_name}"
        )
    except CogniteAPIError:
        logger.info(
            f"Failed to create function {human_readable_name} with external id {function_name}"
        )
        raise

    return function


def create_function_from_file(
    human_readable_name: str,
    function_name: str,
    file_id: int,
    description: str,
    metadata: Dict[str, str],
    owner: str,
    python_runtime: str,
    secrets: Optional[Dict[str, str]] = None,
) -> Any:
    """
    Create a Cognite function from a file deployed to CDF Files.
    If there exist a function with the same external id, the function is
    overwritten.

    Args:
        human_readable_name (str): name of the function to create
        function_name (str): external id of the function to create
        file_id (int): the id for the function file in CDF Files
        description (str): function documentation
        owner (str): the function's owner's email
        python_runtime (str): Python runtime to use for the function
        secrets (dict, optional): Client secrets or similar that should be passed to the function.
            Defaults to an empty dictionary

    Returns:
        (Any): the created function
    """
    if secrets is None:
        secrets = {}
    client = global_client["write"]
    try:
        client.functions.delete(external_id=function_name)
        logger.info(
            f"Function {human_readable_name} with external id {function_name} already exist and will be overwritten"
        )
    except CogniteNotFoundError:
        logger.info(
            f"Function {human_readable_name} with external id {function_name} does not exist and will be created"
        )
        pass

    envs = {
        **asdict(env_vars),
        "DEPLOYMENT_PLATFORM": "cdf",
    }  # ensure CDFLogger is used
    envs = {k.upper(): str(v) for k, v in envs.items() if v is not None}
    try:
        function = client.functions.create(
            name=human_readable_name,
            file_id=file_id,
            external_id=function_name,
            description=description,
            metadata=metadata,
            runtime=python_runtime,
            owner=owner,
            secrets=secrets,
            env_vars=envs,
        )
        logger.info(
            f"Created function {human_readable_name} with external id {function_name}: {file_id=}"
        )
    except CogniteAPIError as e:
        logger.info(
            f"Failed to create function {human_readable_name} with external id {function_name}"
        )
        logger.info(f"Message returned from the Cognite API: {e.message}")

    return function


def robust_create(create_function: partial) -> Function:
    """
    Robust creation of a CDF Function. Wait until the function status is ready
    or failed. If it fails, it will try again `max_error` times

    Args:
        create_function (partial): partial function that creates the CDF function
    """
    max_errors = 3

    for trial in range(max_errors):
        logger.info(f"Creating function (trial {trial + 1}/{max_errors})")
        function = create_function()
        status = wait_function_status(function)
        logger.info(f"Function status is {status}")
        if function.status == "Ready":
            break
        if function.status == "Failed" and trial < max_errors - 1:
            logger.warning(f"Function failed: {function.id=}")
            logger.info(f"Error was: {function.error=}")
            logger.info("Try to create function again")
        else:
            raise Exception(
                f"Function deployment error, exceeded failure limit ({max_errors}): {function.error=}"
            )
    return function


CDFInfo = TypedDict("CDFInfo", {"metadata": dict, "description": str, "owner": str})


def deploy_function(
    human_readable_name: str,
    function_name: str,
    python_runtime: str,
    folder: Optional[str] = None,
    handler_path: Optional[str] = None,
    secrets: Dict[str, str] = client_secrets,
    info: Optional[CDFInfo] = None,
) -> Function:
    """
    Deploys a model as a Cognite function from a folder where the source code is located.
    The argument handler_path points to a file in the folder within which a function named handle is defined.

    Args:
        human_readable_name (str): name of the function to create
        function_name (str): external id of the function to create
        python_runtime (str): the python runtime to use for the function
        folder (str, optional): path where the source code is located.
            Defaults to str(Path().resolve()).
        handler_path (str, optional): path to the handler file.
            Defaults to "handler.py".
        secrets (Dict[str, Any], optional): Client secrets or similar that should be passed to the function.
            Defaults to the global client_secrets dictionary.
        info (Dict[str, Union[str, Dict[str, str]]], optional): dictionary containing info for a specific service, as specified in the settings
            Defaults to a dictionary with empty fields for description, metadata and owner.
    """
    if folder is None:
        folder = str(Path().resolve())
    if handler_path is None:
        handler_path = "handler.py"
    if info is None:
        info = {"description": "", "metadata": {}, "owner": ""}
    try:
        description = info["description"]
    except KeyError:
        raise Exception(
            "Description field is missing, please update mlops_settings.yaml"
        ) from None

    try:
        owner = info["owner"]
    except KeyError:
        raise Exception(
            "Owner field is missing, please update mlops_settings.yaml"
        ) from None

    # Validate metadata one last time
    metadata = info["metadata"]

    # Deploy
    f = functools.partial(
        create_function_from_folder,
        human_readable_name,
        function_name,
        folder,
        handler_path,
        python_runtime,
        description,
        metadata,
        owner,
        secrets,
    )
    return robust_create(f)


def redeploy_function(
    human_readable_name: str,
    function_name: str,
    file_id: int,
    description: str,
    metadata: Dict[str, str],
    owner: str,
    python_runtime: str,
    secrets: Dict[str, str] = client_secrets,
) -> None:
    """
    Deploys a Cognite function from a folder.

    Args:
        function_name (str): name of the function to create
        file_id (int): the id for the function file in CDF Files
        owner (str): the function's owner's email
        description (str): function description
        metadata (Dict[str, str]): dictionary containing function metadata
        python_runtime (str): the python runtime to use for the function
        secrets: (dict, optional) Client secrets or similar that should be passed to the function.
            Defaults to the global client_secrets dictionary.
    """
    f = functools.partial(
        create_function_from_file,
        human_readable_name,
        function_name,
        file_id,
        description,
        metadata,
        owner,
        python_runtime,
        secrets,
    )
    robust_create(f)


def get_function_call_response_metadata(function_id: int) -> Dict[str, Any]:
    """
    Generate metadata for a function
    Args:
        function_id (int): function's id in CDF
    Returns:
        (dict): function call response metadata
    """
    client = global_client["read"]
    function = client.functions.retrieve(id=function_id)

    ts = function.created_time / 1000  # type: ignore
    created_time = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    metadata = {
        "external_id": function.external_id,  # type: ignore
        "description": function.description,  # type: ignore
        "owner": function.owner,  # type: ignore
        "status": function.status,  # type: ignore
        "file_id": function.file_id,  # type: ignore
        "created_time": created_time,
    }
    return metadata


def call_function(function_name: str, data: Dict, retries: int = 1) -> Any:
    """
    Call a function deployed in CDF based on the external id

    Args:
        function_name (str): external id of the deployed function in CDF
        data (dict): model payload

    Returns:
        (dict): function call response
    """
    client = global_client["write"]
    function = client.functions.retrieve(external_id=function_name)
    logger.info(f"Retrieved function with external-id {function_name} from CDF")
    call_complete = False
    t_start = time.process_time()
    while not call_complete:
        try:
            call = function.call(data)  # type: ignore
            call_complete = True
        except CogniteAPIError:
            if retries:
                retries -= 1
                logger.warning(
                    f"Call to {function_name=} failed: Traceback {traceback.format_exc()}"
                )
                logger.warning(f"Retrying function call to {function_name=}")
            else:
                logger.error("Test call to deployed model failed")
                raise
    logger.info(f"Called function ({call.id=})")
    response = call.get_response()
    time.sleep(2)  # Give cognite some time to collect the logs
    logs = call.get_logs()
    for log in logs:
        logger.info(
            "Call log time: %s - Call log message: %s",
            pd.to_datetime(log.timestamp, unit="ms"),
            log.message,
        )
    status = response["status"]  # type: ignore
    if status == "error":
        error_message = response.get("error_message", "No error message provided")  # type: ignore
        exception_message = f"Function call failed with {status=}: {error_message}"
        logger.error(exception_message)
        raise exceptions.FunctionCallError(exception_message)
    if response is None:
        # Something failed in the call. Retrieve the call logs and raise an exception
        logger.error(f"Function call with id {call.id} failed!")
        raise exceptions.MissingResponseError(
            f"Function call with id {call.id} returned an empty response"
        )
    duration = time.process_time() - t_start
    logger.info(f"Function call complete ({call.id=}, {duration=}): {status=}")
    return response


def call_function_process_wrapper(function_name: str, data: Dict) -> Any:
    """
    Set up the cdf client and call a function based on external id.
    This wrapper makes it possible to call a function from an independent processess invoked by the multiprocessing library

    Args:
        function_name (str): function's external id in CDF
        data (dict): data for the call
    Returns:
        (dict): function call response
    """
    set_up_cdf_client("write")
    return call_function(function_name, data)


def call_function_parallel(
    function_name: str, data: Dict, n_calls: Optional[int] = None
) -> Any:
    """
    Make parallel calls to a function deployed in CDF, based on the external id of the function

    Args:
        function_name (str): function's external id in CDF
        data (dict): list of data for the call
        n_calls (int, optional): number of parallel calls (set None to use all available cpu cores).
            Defaults to None.
    """
    f = partial(call_function_process_wrapper, function_name)
    with Pool(n_calls) as p:
        return p.map(f, data)


def test_function(function_name: str, data: Dict) -> None:
    """
    Call a function with data and verify that the response's
    status is 'ok'

    Args:
        function_name (str): function's external id in CDF
        data (dict): data for the call

    Raises:
        ValueError: if the function name is invalid
    """
    logger.info(f"Testing function {function_name}")
    if not validate_function_name(function_name):
        raise ValueError()
    output = call_function(function_name, data)
    assert output["status"] == "ok"
    logger.info("Test call was successful :)")


def wait_function_status(function: Function, status: Optional[List[str]] = None) -> Any:
    """
    Wait until function status is in `status`
    By default it waits for Ready or Failed, which is useful when deploying.
    It implements some control logic, since polling status can fail.

    Args:
        function (Function): function to wait for
        status (List[str], optional): list of statuses to wait for. Defaults to ["Ready", "Failed"].

    Returns:
        (str): function status
    Raises:
        CogniteAPIError: if the function status fails to update
    """
    if status is None:
        status = ["Ready", "Failed"]
    polling_wait_seconds_base = 10.0
    polling_wait_seconds = polling_wait_seconds_base
    max_api_errors_base = 5
    max_api_errors = max_api_errors_base

    logger.info("Wait for function to be ready or to fail")
    while function.status not in status:
        try:
            time.sleep(polling_wait_seconds)
            function.update()
            logger.info(f"{function.status=}")
            polling_wait_seconds = polling_wait_seconds_base
            max_api_errors = max_api_errors_base
        except CogniteAPIError as e:
            max_api_errors -= 1
            logger.warning("Could not update function status, will try again")
            polling_wait_seconds *= 1.2
            if not max_api_errors:
                logger.error("Could not update function status.")
                raise e

    return function.status


def list_functions(tags: Optional[List] = None, model_env: Optional[str] = None) -> Any:
    """
    List deployed functions, optionally filtering by environment (dev, test
    or prod) or set of tags.

    Input:
        - tags: (List[str], optional): list of tags to search for in the function description.
            Defaults to [].
        - model_env: (str, optional) the environment. Defaults to None

    Output:
        - (List[str]): list of function names (i.e. external_id's )
    """
    if tags is None:
        tags = []
    client = global_client["read"]
    functions = client.functions.list(limit=-1)

    def _validate_function(function: Any) -> bool:
        return validate_function_name(function.external_id, verbose=True)

    functions = filter(_validate_function, functions)  # type: ignore
    if model_env is not None:

        def _get_function_environment(function: Any) -> str:
            if function.external_id.split("-") > 1:
                return str(function.external_id.split("-")[2])
            else:
                return "unknown"

        def _env_index(function_name: Any) -> bool:
            return _get_function_environment(function_name) == model_env

        functions = filter(_env_index, functions)  # type: ignore
    if tags:

        def _contains_tag(function: Any, tag: Any) -> bool:
            if tag in function.description:
                return True
            else:
                return False

        def _tags_index(function: Any) -> bool:
            return any(_contains_tag(function, tag) for tag in tags)

        functions = filter(_tags_index, functions)  # type: ignore
    functions = [f.external_id for f in functions]  # type: ignore
    functions = sorted(functions)  # type: ignore
    return functions


def download_file(
    file_id: Dict[str, Union[str, int]], path: Union[Path, str], **kwargs
) -> None:
    """
    Download file from Cognite

    Args:
        id (dict): dictionary with id type (either "id" or "external_id") as key
        path (Union[Path, str]): path to file
    """
    client = global_client["read"]

    external_id = kwargs.get("external_id", None)

    if external_id is not None:
        logger.info(f"Download file with {external_id=} to {path}")
        client.files.download_to_path(path, **external_id)
    else:
        logger.info(f"Download file with {file_id=} to {path}")
        client.files.download_to_path(path, **file_id)  # type: ignore


def upload_file(
    external_id: str,
    path: Union[Path, str],
    metadata: Optional[Dict[str, str]] = None,
    directory: str = "/",
    overwrite: bool = True,
    dataset_id: Optional[int] = None,
) -> FileMetadata:
    """
    Upload file to Cognite

    Args:
        external_id (str): external id
        path (Union[Path, str]): path of local file to upload
        metadata(dict, optional): dictionary with file metadata. Defaults to empty dict.
        directory(str, optional): directory to upload file to. Defaults to "/".
        overwrite (bool, optional): what to do when the external_id exists already. Defaults to True
        dataset_id (int, optional): dataset id. Defaults to None

    Returns:
        (FileMetadata): file metadata
    """
    if metadata is None:
        metadata = {}
    client = global_client["write"]

    metadata = {
        k: v if isinstance(v, str) else json.dumps(v) for k, v in metadata.items()
    }

    file_info = client.files.upload(
        path=path,  # type: ignore
        external_id=external_id,
        metadata=metadata,
        directory=directory,
        overwrite=overwrite,
        data_set_id=dataset_id,  # type: ignore
    )
    return file_info  # type: ignore


def upload_folder(
    external_id: str,
    path: Path,
    metadata: Optional[Dict] = None,
    overwrite: bool = False,
    target_folder: str = "/",
    dataset_id: Optional[int] = None,
) -> FileMetadata:
    """
    Upload folder content to Cognite. It compresses the folder and uploads it.

    Args:
        external_id (str): external id (should be unique in the CDF project)
        path: (Path) path of local folder where content is stored
        metadata (dict, optional): file metadata. Defaults to empty dict
        overwrite (bool, optional): if overwrite==False and `external_id` exists => exception. Defaults to False
        target_folder (str): path where compressed file should be stored. Defaults to "/".
        dataset_id (int, optional): dataset id. Defaults to None

    Returns:
        (FileMetadata): file metadata
    """
    if metadata is None:
        metadata = {}
    fname = external_id.replace("/", "-")
    base_name = path / f"{fname}_archive"
    archive_name = make_archive(str(base_name), "gztar", path)
    file_info = upload_file(
        external_id=external_id,
        path=archive_name,
        metadata=metadata,
        overwrite=overwrite,
        directory=target_folder,
        dataset_id=dataset_id,
    )
    archive_path = Path(archive_name)
    archive_path.unlink()
    return file_info


def download_folder(external_id: str, path: Path) -> None:
    """
    Download content from Cognite to a folder. It is assumed to have been
    uploaded using `upload_folder()`, so it downloads a file and decompresses
    it.

    Args:
        external_id (str): external id
        path: (Path) path of local folder where content will be stored
    """
    fname = external_id.replace("/", "-")
    base_name = path / f"{fname}_archive.tar.gz"
    download_file({"external_id": external_id}, base_name)
    unpack_archive(base_name, base_name.parent)
    base_name.unlink()
    logger.info(f"Model file/s downloaded to {path}")


def log_system_info() -> None:
    """
    Can be called from a handler to log CDF environment information
    """
    logger.debug(f"Python version:\n{os.popen('python --version').read()}")
    logger.debug(f"Python path:\n{sys.path}")
    logger.debug(f"Current working directory:\n{Path.cwd()}")
    logger.debug(f"Content:\n{os.popen('ls -la *').read()}")
    logger.debug(f"Packages:\n{os.popen('pip freeze').read()}")


def query_file_versions(
    directory_prefix: str,
    external_id_prefix: str,
    metadata: Optional[Dict] = None,
    uploaded: Optional[bool] = True,
    dataset_id: Optional[int] = None,
) -> pd.DataFrame:
    """
    Find all file versions that match a query.

    Args:
        directory_prefix (str): directory prefix
        external_id_prefix (str): external id prefix
        metadata (dict): metadata
        uploaded (bool, optional): Whether file has been uploaded. Defaults to True.
        dataset_id (int): dataset id
    Returns:
        (pd.DataFrame): file versions
    """
    if metadata is None:
        metadata = {}
    client = global_client["read"]
    file_list = client.files.list(
        limit=-1,
        directory_prefix=directory_prefix,
        external_id_prefix=external_id_prefix,
        metadata=metadata,
        uploaded=uploaded,  # type: ignore
        data_set_ids=dataset_id,  # type: ignore
    ).to_pandas(camel_case=False)

    return file_list


def delete_file(file_id: Dict) -> None:
    """
    Delete file from Cognite

    Args:
        id (dict): dictionary with id type (either "id" or "external_id") as key
    """
    client = global_client["write"]
    client.files.delete(**file_id)
    logger.info(f"Deleted file with {file_id=}")


def copy_file(
    source_ext_id: str,
    target_ext_id: str,
    overwrite: bool = False,
    dataset_id: Optional[int] = None,
    **kwargs,
) -> None:
    """
    Copy content and metadata of a file in CDF Files

    Args:
        - source_ext_id (str): external id for source file
        - target_ext_id (str): external id for target file
        - overwrite (bool, optional): should target file be overwritten if it exists. Defaults to False
        - dataset_id (int, optional): dataset id for the target file. Defaults to None
    """
    overwrite_name = kwargs.get("overwrite_name", False)
    name = kwargs.get("name", None)
    try:
        client = global_client["write"]
    except KeyError as e:
        raise exceptions.MissingClientError(
            "No CDF client with Files permissions was set up"
        ) from e
    f = client.files.retrieve(external_id=source_ext_id)
    file_content = client.files.download_bytes(external_id=source_ext_id)
    if overwrite_name:
        if name is None:
            raise Exception(
                "You need to set the 'name' kwarg if you want to overwrite the name of the file to copy"
            )
    else:
        name = f.name  # type: ignore
    f = client.files.upload_bytes(
        file_content,
        name=name,
        external_id=target_ext_id,
        metadata=f.metadata,  # type: ignore
        directory=f.directory,  # type: ignore
        overwrite=overwrite,
        data_set_id=dataset_id,  # type: ignore
    )
    m = f"Copied source {source_ext_id} to {target_ext_id}, {f.dump()}"
    logger.info(m)


def file_exists(
    external_id: str, directory: str, dataset_id: Optional[int] = None
) -> bool:
    """
    Check if a file exists in a folder (regardless of uploaded status)

    Args:
        external_id (str): external file-id
        directory (str): directory to search in
        dataset_id (int, optional): dataset id. Defaults to None
    Returns
        (bool): whether file exists
    """
    file_list = query_file_versions(
        directory_prefix=directory,
        external_id_prefix=external_id,
        uploaded=None,
        dataset_id=dataset_id,
    )
    if file_list.empty:
        exists = False
    else:
        exists = True
    return exists


def get_dataset_id(external_id: Optional[str] = None) -> Optional[int]:
    """
    Get dataset id for a file

    Args:
        external_id (str, optional): dataset external id, or `None` for no dataset. Defaults to None
    Returns:
        (int) dataset id, or `None` for no dataset
    """
    if external_id:
        client = global_client["read"]
        dataset = client.data_sets.retrieve(external_id=external_id)
        return int(dataset.id)  # type: ignore
    else:
        return None


def file_to_dataset(
    file_external_id: str, dataset_external_id: Optional[str] = None
) -> None:
    """
    Assign a file to a dataset.

    Args
        file_external_id (str): external id of the file
        dataset_external_id(str, optional): the dataset's external id, `None` for no. Defaults to None
    """
    client = global_client["write"]
    dataset_id = get_dataset_id(dataset_external_id)
    file_metadata_update = FileMetadataUpdate(external_id=file_external_id)
    file_metadata_update = file_metadata_update.data_set_id.set(dataset_id)
    _ = client.files.update(file_metadata_update)
    logger.info(f"Assigned dataset {dataset_id} to file {file_external_id}")


def get_latest_artifact_version(external_id: str) -> int:
    """Extract the latest artifact version based on the external id of a function.
    If no artifacts are found for the specified function, the version is set to 1.

    Args:
        external_id (string): external id of the function

    Returns:
        (int): latest artifact version of the function
    """
    if len(splitted_external_id := external_id.split("-")) > 3:
        env = splitted_external_id[-2]
    else:
        env = splitted_external_id[-1]
    model_name = splitted_external_id[0]

    artifact_external_id = model_name + "/" + env
    artifact_versions = query_file_versions(
        directory_prefix="/mlops", external_id_prefix=artifact_external_id
    )
    if len(artifact_versions) == 0:
        raise ValueError(
            f"No artifacts found for function with external id {external_id}. Please ensure you upload your artifacts before starting deployment."
        )
    else:
        latest_artifact_version = artifact_versions.loc[
            artifact_versions["uploaded_time"].argmax()
        ].metadata["version"]

    return int(latest_artifact_version)


def get_arguments_for_redeploying_numbered_models(
    external_id: str,
) -> Tuple[str, str, str, Dict[str, str], str]:
    """Extract data needed to redeploy the latest function from CDF files using a predictable external id,
    i.e. witout the model version number. In this way the client does not have to care about version numbers.
    In addition to copying the data fields of the function, the version number is added to the metadata (set to 1 if it does not exist)

    Args:
        external_id (str): external id of the deployed function in CDF

    Returns:
        (tuple): tuple containing the data needed for redeploying the latest function with a predictable external id
    """
    client = global_client["read"]
    latest_function = client.functions.retrieve(external_id=external_id)
    name = latest_function.name  # type: ignore
    file_id = latest_function.file_id  # type: ignore
    description = latest_function.description  # type: ignore
    owner = latest_function.owner  # type: ignore
    metadata = latest_function.metadata  # type: ignore
    return name, file_id, description, metadata, owner  # type: ignore


def setup_schedule_for_latest_model_in_prod(
    external_id: str,
    function_id: int,
    client: Optional[CogniteClient] = None,
) -> None:
    if client is None:
        client = global_client["write"]
    schedules = client.functions.schedules.list(
        function_external_id=external_id,
    )
    if len(schedules) > 0:
        logger.info("A schedule already exist and will be overwritten")
        for schedule in schedules:
            schedule_id = cast(int, schedule.id)
            client.functions.schedules.delete(id=schedule_id)

    _ = client.functions.schedules.create(
        name="Keep warm schedule",
        description="Keep the function warm by calling it with an empty payload every 30 minutes during extended working hours on weekdays",
        cron_expression="*/30 5-17 * * 1-5",
        function_id=function_id,
        data={},
    )
    logger.info("Schedule created")


def garbage_collection(
    c: config.ServiceSettings,
    function_name: str,
    env: str,
    client: Optional[CogniteClient] = None,
    remove_artifacts: bool = False,  # for mlops only
) -> None:
    """Garbage collection of old models in CDF"""
    models_to_keep = c.models_to_keep
    keep_all_models = c.keep_all_models if c.keep_all_models is not None else False
    if client is None:
        client = global_client["read"]
    if models_to_keep is None:
        if keep_all_models is True:
            logger.info("Keeping all models alive as specified in the settings file")
            return
        else:
            logger.info("Number of models to keep alive not specified in settings file")
            logger.info("Setting number of models to keep to 3 (default)")
            models_to_keep = 3
    else:
        logger.info(
            f"Number of models to keep alive inferred from settings file ({models_to_keep})"
        )
        models_to_keep = int(models_to_keep)

    existing_functions: List[str] = [
        cast(str, f.external_id)
        for f in client.functions.list(external_id_prefix=function_name)
    ]
    version_ids = [eid for eid in existing_functions if eid.count("-") == 3]
    latest_artifact_version = get_latest_artifact_version(external_id=function_name)

    if (
        models_to_keep is not None
        and models_to_keep >= len(version_ids)
        and len(version_ids) != 0
    ):
        logger.info(
            f"Number of alive models ({len(version_ids)}) fewer than/equal to the number of models to keep alive ({models_to_keep}). Skipping garbage collection."
        )
    elif len(version_ids) == 0:  # Special case for mlopsdemo during testing
        if remove_artifacts:  # equivalent to c.model_name == "mlopsdemo"
            logger.info(
                f"Deleting non-numbered models of model {c.model_name} in {env}"
            )
            delete_function(function_name=function_name, confirm=False)
            m, _, e = function_name.split("-")
            if (
                latest_artifact_version != 1
            ):  # Need at least a single artifact to be able to deploy
                delete_file(
                    file_id={"external_id": f"{m}/{e}/{latest_artifact_version}"}
                )

    else:
        logger.info(
            f"Starting garbage collection of model {c.human_friendly_model_name} in {env}"
        )

        external_ids_sorted = [
            function_name + "-" + str(v)
            for v in sorted([
                int(external_id.split("-")[-1]) for external_id in version_ids
            ])
        ]

        num_models_to_delete = len(version_ids) - models_to_keep
        external_ids_to_delete = external_ids_sorted[:num_models_to_delete]

        for external_id in external_ids_to_delete:
            version = external_id.split("-")[-1]
            logger.info(f"Deleting version {version} of model {c.model_name} in {env}")
            delete_function(function_name=external_id, confirm=False)
            if remove_artifacts is True:
                m, _, e, v = external_id.split("-")
                delete_file(file_id={"external_id": f"{m}/{e}/{v}"})

        if remove_artifacts:
            # Remove any non versioned models too (artifacts already removed)
            non_versioned_models = set(existing_functions) - set(version_ids)
            for external_id in non_versioned_models:
                logger.info(f"Deleting non-versioned model {external_id} in {env}")
                delete_function(function_name=external_id, confirm=False)


def cdf_metadata_validation(
    metadata: dict,
) -> None:
    metadata_fields = metadata.keys()
    if (no_of_metadata_fields := len(metadata_fields)) > 16:
        # Cognite limitation is 16, but we add model version, mlops version and mlpet version
        # to metadata on deployment.
        raise ValueError(
            f"Too many fields in the metadata specification, exceeding the maximum of 13 fields. Number of fields in settings file {no_of_metadata_fields}"
        )
    try:
        for key, value in metadata.items():
            key_ = str(key)
            value_ = str(value)
            if len(key_) > 32:
                raise ValueError(
                    f"Key '{key}' exceeds the maximum length of 32 characters ({len(key_)})."
                )

            if len(value_) > 512:
                raise ValueError(
                    f"Value '{value}' of '{key}' exceeds the maximum length of 512 characters ({len(value_)})."
                )

        # Maximum size of entire metadata cannot exceed 4096 bytes
        if (metadata_size := len(json.dumps(metadata).encode())) > 4096:
            raise ValueError(
                f"Size of metadata exceeds the maximum size of 4096 bytes ({metadata_size})."
            )
    except ValueError:
        logger.error(f"Metadata validation failed: {metadata=}")
        raise


def delete_test_payload(external_id: str) -> None:
    client = global_client["write"]
    try:
        client.files.delete(external_id=external_id)
        logger.info(f"Deleted test payload with external id {external_id}")
    except CogniteNotFoundError:
        logger.info(f"Test payload with external id {external_id} does not exist")
        pass
    except CogniteAPIError:
        logger.error(f"Failed to delete test payload with external id {external_id}")
