# helpers.py
import os
import re
import subprocess
import time
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Union

import requests

from akerbp.mlops.core import mappings
from akerbp.mlops.core.logger import get_logger

logger = get_logger(__name__)


def get_top_folder(path: Union[Path, str]) -> Union[Path, str]:
    """
    Get the top folder of a path.

    Args:
        path (Union[Path, str]): Path to get the top folder from.

    Returns:
        (Union[Path, str]): top parent folder in path
    """
    if isinstance(path, str):
        return Path(path).parts[0]
    elif isinstance(path, Path):
        return path.parents[len(path.parents) - 2]


def as_import_path(file_path: Optional[str]) -> Optional[str]:
    """Return path as an import path for python modules


    Args:
        file_path (str, optional): path to file

    Returns:
        (Union[str, None]): path to .py-file with .py extension removed(for importing modules)
    """
    if file_path:
        if not isinstance(file_path, str):
            file_path = str(file_path)
        return file_path.replace(os.sep, ".").replace(".py", "")
    else:
        logger.debug("Empty file path -> empty import path returned")
        return None


def confirm_prompt(question: str) -> bool:
    """Helper function to ask user for confirmation

    Args:
        question (str): question to ask user

    Returns:
        (bool): True if user confirms, False otherwise
    """
    reply = None
    while reply not in ("y", "n"):
        reply = input(f"{question} (y/n): ").lower()
    return reply == "y"


def input_data_validation(
    required_input: List[str],
    input_payload: Dict,
) -> bool:
    """Check if the input data contains all the required input curves.
    Note that the input potentially consists of multiple wells according to the payload structures.

    If input logs are provided in the payload, they need to be provided in the field 'input_logs',
    otherwise the validation fails.
    If no input logs are provided, the validation passes if either the field 'well' or
    'well' and 'keyword_arguments' are specified

    Args:
        required_input (List[str]): list of required input curves
        input (Dict): dictionary containing the input data

    Returns:
        bool: whether the input data contains all the required input curves or not
    """
    if required_input is None:
        print("No required input here")
        return True
    curve_mapping = mappings.curve_mappings
    validated = []
    input_wells = input_payload["input"]
    for well_data in input_wells:
        try:
            curves_in_well_data = list(well_data["input_logs"].keys())
            curves_in_well_data_standardized = [
                curve_mapping[curve]
                if curve != "WELL" and curve in curve_mapping.keys()
                else curve
                for curve in curves_in_well_data
            ]
            diff = set(required_input) - set(curves_in_well_data_standardized)

            if len(diff) > 0:
                logger.warning(
                    f"Not all required input curves are provided. Missing: {diff}"
                )
                validated.append(False)
            else:
                validated.append(True)
        except KeyError:
            wrong_input_log_specification = False
            for key in well_data.keys():
                if isinstance(well_data[key], dict) and len(well_data[key].keys()) > 0:
                    wrong_input_log_specification = True
                    break
            if wrong_input_log_specification:
                logger.warning(
                    f"Data is required to be specified as 'input_logs' in the payload, not '{key}'"
                )
                validated.append(False)
            elif "well" in well_data.keys() and "keyword_arguments" in well_data.keys():
                validated.append(True)
            elif "well" in well_data.keys():
                validated.append(True)
            else:
                logger.warning(
                    "Payload not properly specified. Need to specify field 'well', and optionally 'keyword_arguments' if no input logs are provided"
                )
    if sum(validated) < len(input_wells):
        return False
    else:
        return True


def response_validation(response: List[Dict]) -> bool:
    """Validates the reponse of each model call,
    making sure that it contains at least 'well_name' and 'DEPTH'

    Args:
        response (List[Dict]): response from predict function
        required_output (List[str]): List of required output curves

    Returns:
        bool: whether or not response is valid in terms of structure and required output curves
    """
    required_output_fields = {"well_name", "DEPTH"}
    validated_response = []
    for res in response:
        response_output_curves = set(res.keys())
        if required_output_fields.issubset(response_output_curves):
            validated_response.append(True)
        else:
            logger.warning(
                f"The response does not have the required fields: {required_output_fields}"
            )
            validated_response.append(False)
    return sum(validated_response) == len(validated_response)


def subprocess_wrapper(
    cmd: List[str], retry: int = 1, log_output=True, skiplines=None, **kwargs
) -> str:
    encoding = kwargs.pop("encoding", "utf-8")
    if skiplines is None:
        pat = None
    else:
        pat = re.compile("|".join(skiplines))
    output = ""
    for i in range(retry):
        completed_process = False
        try:
            logger.info(
                f"Running subprocess.check_output with the following commands: {cmd}"
            )
            output = subprocess.check_output(cmd, encoding=encoding, **kwargs)
        except subprocess.CalledProcessError as e:
            output = e.output
            if i == (retry - 1):
                raise e
            else:
                logger.warning(
                    f"Command {cmd} failed with exit code {e.returncode}. Retrying..."
                )
                time.sleep(15)
        else:
            completed_process = True
        finally:
            if log_output:
                for line in output.splitlines():
                    line.strip()
                    if pat is not None and pat.search(line):
                        logger.info(
                            f"Skipping subprocess output due to provided skiplines pattern {pat}"
                        )
                        continue
                    if completed_process:
                        logger.info(line)
                    else:
                        logger.error(line)
    return output


def requests_wrapper(
    request_type: str,
    url: str,
    data: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    **kwargs,
) -> requests.Response:
    """
    Wrapper for requests.get and requests.post with error handling

    Args:
        request_type (str): type of request, either 'get' or 'post'
        url (str): url to send request to
        data (Dict, optional): data to send in request. Defaults to None.
        headers (Dict, optional): headers to send in request. Defaults to None.

    Returns:
        (requests.Response): response from request
    """
    try:
        response = requests.request(
            request_type,
            url,
            data=data,
            headers=headers,
            **kwargs,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        trace = traceback.format_exc()
        logger.error(
            f"Something failed with your request to the following {url}: {e}\n{trace}"
        )
        raise e
    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        logger.error(f"Error when sending request to {url}: {e}\n{trace}")
        raise e
    return response
