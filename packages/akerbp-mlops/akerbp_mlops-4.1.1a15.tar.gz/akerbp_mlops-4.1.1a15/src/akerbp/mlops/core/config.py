# config.py
import os
import re
import traceback
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import yaml
from pydantic import FilePath
from pydantic.dataclasses import dataclass

from akerbp.mlops.core import helpers
from akerbp.mlops.core.exceptions import (
    FieldValueError,
    MissingFieldError,
    MissingMetadataError,
)
from akerbp.mlops.core.logger import get_logger

logger = get_logger(__name__)


def validate_categorical(
    setting: Union[str, None, bool], name: str, allowed: List[Optional[str]]
) -> None:
    """Helper function to validate categorical variables in the framework

    Args:
        setting (Optional[str]): variable to validate. Defaults to None
        name (str): name of the variable to validate
        allowed (List[Optional[str]]): list of allowed values for the variable.

    Raises:
        ValueError: message with the name of the invalid variable and the allowed values
    """
    if setting not in allowed:
        m = f"{name}: allowed values are {allowed}, got '{setting}'"
        raise ValueError(m)


@dataclass
class EnvVar:
    """Dataclass for keeping track of environmental variables

    Attributes:
        model_env (Optional[str]): environment. Defaults to None
        service_name (Optional[str]): service name. Defaults to None
        platform (Optional[str]): platform. Defaults to None
    """

    model_env: Optional[str] = None
    service_name: Optional[str] = None
    platform: Optional[str] = None
    testing_only: Optional[Union[str, bool]] = False

    def __post_init__(self):
        """Post initialization function of the dataclass that validates the attributes env, platform and service_name
        Allowed values for attributes:
            model_env: 'dev', 'test', 'prod'
            platform: 'cdf', 'local'
            service_name: 'training', 'prediction'
        """
        if self.model_env:
            validate_categorical(self.model_env, "Environment", ["dev", "test", "prod"])
        else:
            logger.warning("MODEL_ENV environmental variable is not set")
        validate_categorical(self.platform, "Platform", ["cdf", "local"])
        if self.model_env and self.model_env != "dev":
            validate_categorical(
                self.service_name, "Service  name", ["training", "prediction"]
            )


def read_env_vars() -> EnvVar:
    """
    Read environmental variables and initialize EnvVar object with those that
    were set (i.e. ignored those with None value). Note that
    Default values:
        DEPLOYMENT_PLATFORM: 'cdf'
        TESTING_ONLY: 'False'
    """
    envs = {
        "model_env": os.getenv("MODEL_ENV"),
        "service_name": os.getenv("SERVICE_NAME"),
        "platform": os.getenv("DEPLOYMENT_PLATFORM", "cdf"),
        "testing_only": os.getenv("TESTING_ONLY", "False"),
    }
    envs = {k: v for k, v in envs.items() if v is not None}

    return EnvVar(
        model_env=envs.get("model_env"),
        service_name=envs.get("service_name"),
        platform=envs.get("platform"),
        testing_only=envs.get("testing_only"),
    )


ENV_VARS = read_env_vars()


@dataclass
class AvailableSecrets:
    """
    dataclass for keeping track of secrets available to the model endpoint
    for authentication

    Attributes:
        tenant_id (Optional[str]): CDF tenant id. Defaults to None
        base_url (Optional[str]): CDF base url. Defaults to None
        id_read (Optional[str]): CDF client id for read operations. Defaults to None
        secret_read (Optional[str]): CDF client secret for read operations. Defaults to None
        id_write (Optional[str]): CDF client id for write operations. Defaults to None
        secret_write (Optional[str]): CDF client secret for write operations. Defaults to None
    """

    tenant_id: Optional[str] = None
    base_url: Optional[str] = None
    id_read: Optional[str] = None
    secret_read: Optional[str] = None
    id_write: Optional[str] = None
    secret_write: Optional[str] = None
    osdu_id: Optional[str] = None
    osdu_secret: Optional[str] = None
    osdu_base_url: Optional[str] = None
    osdu_dp_id: Optional[str] = None

    def __post_init__(self):
        """Post initialization function of the dataclass that validates the attribute base_url"""
        # Ensure there are no trailing slashes in the base url
        if self.base_url is not None:
            self.base_url = re.sub(r"/$", "", self.base_url)

        if self.osdu_base_url is not None:
            self.osdu_base_url = re.sub(r"/$", "", self.osdu_base_url)


def read_secrets() -> Dict[str, str]:
    secrets = asdict(
        AvailableSecrets(
            tenant_id=os.getenv("COGNITE_TENANT_ID"),
            base_url=os.getenv("COGNITE_OIDC_BASE_URL"),
            id_read=os.getenv("COGNITE_CLIENT_ID_READ"),
            secret_read=os.getenv("COGNITE_CLIENT_SECRET_READ"),
            id_write=os.getenv("COGNITE_CLIENT_ID_WRITE"),
            secret_write=os.getenv("COGNITE_CLIENT_SECRET_WRITE"),
            osdu_id=os.getenv("OSDU_CLIENT_ID"),
            osdu_secret=os.getenv("OSDU_CLIENT_SECRET"),
            osdu_base_url=os.getenv("OSDU_API_BASE_URL"),
            osdu_dp_id=os.getenv("OSDU_DATA_PARTITION_ID"),
        )
    )
    return {k.replace("_", "-"): v for k, v in secrets.items() if v is not None}


client_secrets = read_secrets()


def generate_default_project_settings(
    yaml_file: Path = Path("mlops_settings.yaml"), n_models: int = 2
) -> None:
    """Generate default the mlops_settings.yaml file from a hardcoded template

    Args:
        yaml_file (Path, optional): path to the mlops_settings.yaml file. Defaults to Path("mlops_settings.yaml")
        n_models (int, optional): number of models to generate. Defaults to 2

    """
    if yaml_file.exists():
        raise Exception(f"Settings file {yaml_file} exists already.")

    default_config_template = [
        """
model_name: my_model
human_friendly_model_name: 'My model'
model_file: model_code/my_model.py
req_file: model_code/requirements.model
test_file: model_code/test_model.py
artifact_folder: artifact_folder
platform: cdf
dataset: mlops
helper_models:
    - model_name: helper_model_1
      env: dev
      version: 1
      target_path: model_code/helper_model_1
packages_to_check:
    - akerbp-mlpet
info:
    prediction:
        description: Description prediction service for my_model
        metadata:
            required_input:
                - input_1
                - input_2
            optional_input:
                - optional_input_1
                - optional_input_2
            keyword_arguments:
                - name: keyword_1
                  required: True
                - name: keyword_2
                  required: False
                  default: 0
            training_wells:
                - 3/1-4
            input_types:
                - float
                - int
            units:
                - s/ft
                - 1
            output_curves:
                - output_1
            output_units:
                - s/ft
            petrel_exposure: False
            supports_external_retrieval: False
            imputed: True
            num_filler: -999.15
            cat_filler: UNKNOWN
        owner: datascientist@akerbp.com
"""
    ]
    default_config_list = default_config_template * n_models
    default_config = "---".join(default_config_list)
    with yaml_file.open("w") as f:
        f.write(default_config)


def validate_model_reqs(req_file: FilePath) -> None:
    # Model reqs is renamed to requirements.txt during deployment
    if req_file.name == "requirements.model":
        with req_file.open() as f:
            req_file_string = f.read()
            if "akerbp-mlops" not in req_file_string:
                m = "Model requirements should include akerbp-mlops package"
                raise Exception(m)
            if "MLOPS_VERSION" not in req_file_string:
                m = 'akerbp-mlops version should be "MLOPS_VERSION"'
                raise Exception(m)


@dataclass
class HelperModel:
    """dataclass for keeping track of helper models

    Attributes:
        model_name (str): name of the helper model
        env (Optional[str]): environment of the helper model. Defaults to None
        version (Optional[int]): version of the helper model. Defaults to None
        target_path (Optional[str]): path to the helper model. Defaults to None
    """

    model_name: str
    env: Optional[str] = None
    version: Optional[int] = None
    target_path: Optional[str] = None


@dataclass
class ServiceSettings:
    """dataclass for keeping track of service settings variables

    Attributes:
        model_name (str): name of the model
        human_friendly_model_name (str): human friendly name of the model, displayed on CDF
        model_file (FilePath): path to the model interface
        req_file (FilePath): path to the model requirements
        info (dict): info of the model. Defaults to None
        test_file (FilePath, optional): path to the model test suite. Defaults to None
        artifact_folder (FilePath, optional): path to the model artifacts. Defaults to None
        platform (str, optional): platform of the model. Defaults to "cdf"
        dataset (str, optional): dataset of the model. Defaults to "mlops"
        model_id (str, optional): id of the model. Defaults to None

    """

    model_name: str  # Remember to modify generate_default_project_settings()
    human_friendly_model_name: str
    model_file: FilePath  # if fields are modified
    req_file: FilePath
    info: Dict
    test_file: Optional[FilePath] = None
    artifact_folder: Optional[Path] = None
    artifact_version: Optional[int] = None
    keep_all_models: Optional[bool] = None
    models_to_keep: Optional[int] = None
    helper_models: Optional[List[HelperModel]] = None
    packages_to_check: Optional[List[str]] = None
    python_version: str = "not_set"
    platform: str = "cdf"
    dataset: str = "mlops"
    model_id: Optional[str] = None

    def __post_init_post_parse__(self):
        """post initialization function of the dataclass that validates model requirements and deployment platform variables.
        Moreover, the model interface and test suite import paths are set as class attributes,
        as well as a dictionary containing the required files for running the model (based on deployment platform)

        Raises:
            Exception: If model name contains special characters not supported by the framework
            ValueError: If specifying a model id when deploying a training service
        """
        logger.info("Running ServiceSettings post init post parse!")
        envs = ENV_VARS
        # Validation
        if not re.match("^[A-Za-z0-9_]*$", self.model_name):
            m = "Model name can only contain letters, numbers and underscores"
            raise Exception(m)

        validate_model_reqs(self.req_file)

        validate_categorical(self.platform, "Deployment platform", ["cdf", "local"])

        if self.platform == "cdf":
            validate_python_runtime(self.python_version)

        if self.model_id and envs.service_name == "training":
            raise ValueError("Unexpected model_id setting (training service)")

        self.model_import_path = helpers.as_import_path(self.model_file)
        self.test_import_path = helpers.as_import_path(self.test_file)

        self.files = {
            "model code": helpers.get_top_folder(self.model_file),
            "handler": ("akerbp.mlops.cdf", "handler.py"),
            "artifact folder": self.artifact_folder,
        }


def store_service_settings(
    c: ServiceSettings, yaml_file: Path = Path("mlops_service_settings.yaml")
) -> None:
    """Store service settings in a yaml file during deployment

    Args:
        c (ServiceSettings): service settings for the model to deploy
        yaml_file (Path, optional): path to service settings. Defaults to Path("mlops_service_settings.yaml").

    """
    logger.info("Write service settings file to %s", yaml_file.resolve())

    def factory(data: List[Tuple[str, Any]]) -> Dict[str, str]:
        """
        Take a list of tuples as input. Returns a suitable dictionary.
        Transforms Path objects to strings (linux style path).

        Args:
            data (List[Tuple[str, Any]]): list of tuples to transform

        Returns:
            Dict[str, str]: dictionary with the transformed paths
        """

        def path2str(x: Union[Path, str]) -> str:
            """transforms a Path to a string

            Args:
                x (Union[Path, str]): input path

            Returns:
                str: output string
            """
            if not isinstance(x, Path):
                return x
            else:
                return x.as_posix()

        d = {k: path2str(v) for k, v in data}
        return d

    service_settings = asdict(c, dict_factory=factory)
    with yaml_file.open("w") as f:
        yaml.dump(service_settings, f)


@dataclass
class ProjectSettings:
    """
    dataclass for keeping track of project settings

    Attributes:
        project_settings (List[ServiceSettings]): list of service settings
    """

    project_settings: List[ServiceSettings]


def enforce_string_values_in_function_metadata(
    project_settings: ProjectSettings,
) -> ProjectSettings:
    """The metadata field in CDF functions requires both keys and values to be strings.
    This function iterates through the metadata of each model defined in the mlops settings file,
    and enforce the values to be string (keys are strings by default)

    Args:
        project_settings (ProjectSettings): project settings for each model defined in the settings file

    Returns:
        (ProjectSettings): project settings for each model defined in the settings file
    """
    for i, model_settings in enumerate(project_settings.project_settings):
        for service in list(model_settings.info.keys()):
            metadata = model_settings.info[service]["metadata"]
            for k, v in metadata.items():
                metadata[k] = str(v)
            model_settings.info[service]["metadata"] = metadata
        project_settings.project_settings[i] = model_settings
    return project_settings


def read_project_settings(
    yaml_file: Path = Path("mlops_settings.yaml"),
) -> List[ServiceSettings]:
    """Read project settings from the mlops_setting.yaml file

    Args:
        yaml_file (Path, optional): path to mlops settings. Defaults to Path("mlops_settings.yaml").

    Returns:
        List[ServiceSettings]: list of service settings for each model specified in the settings file
    """
    logger.info("Read project settings")
    with yaml_file.open() as f:
        settings = yaml.safe_load_all(f.read())

    downstream_settings = []
    for setting in settings:
        downstream_settings.append(setting)
        valid_metadata, missing_fields = settings_validation(settings=setting)
        if valid_metadata:
            continue
        else:
            logger.error(
                "Invalid metadata specification due to missing fields or invalid values"
            )
            error_message = f"The following field(s) are missing from the metadata specification: {missing_fields}"
            raise MissingMetadataError(error_message)

    model_settings = [ServiceSettings(**s) for s in downstream_settings]
    project_settings = ProjectSettings(project_settings=model_settings)
    project_settings = enforce_string_values_in_function_metadata(project_settings)

    return project_settings.project_settings


def settings_validation(
    settings: dict,
) -> Tuple[bool, List[str]]:
    """Checks whether the mlopds settings contains all the required fields, as specified on confluence

    Args:
        settings (dict): mlops settings as dictionary

    Returns:
        bool: whether metadata is validated
    """
    required_fields = [
        "required_input",
        "optional_input",
        "output_curves",
        "petrel_exposure",
        "keyword_arguments",
        "supports_external_retrieval",
    ]

    required_fields_petrel = [
        "petrel_template_family",
    ]
    metadata = settings["info"]["prediction"]["metadata"]
    metadata_fields = metadata.keys()

    missing_fields = []
    for field in required_fields:
        if field == "petrel_exposure":
            try:
                petrel_exposure = metadata[field]
                if petrel_exposure:
                    for petrel_field in required_fields_petrel:
                        if petrel_field not in metadata_fields:
                            missing_fields.append(petrel_field)
            except KeyError:
                pass

        if field not in metadata_fields:
            missing_fields.append(field)

    if len(missing_fields) == 0:
        return True, missing_fields
    else:
        return False, missing_fields


def validate_python_runtime(python_runtime: str) -> None:
    """Validates the python runtime specified in the mlops settings file

    Args:
        settings (dict): mlops settings as dictionary

    Raises:
        ValueError: if python runtime is not supported
        MissingFieldError: if python runtime is not specified
    """
    # TODO: keep below list updated if cognite sdk adds support for new python runtimes
    allowed_runtimes = ["py38", "py39", "py310", "py311"]
    if python_runtime == "not_set":
        raise MissingFieldError(
            "Python runtime not specified. Please ensure to included it in your mlops_settings.yaml file! "
            f"Supported versions are {allowed_runtimes}."
        )
    elif python_runtime not in allowed_runtimes:
        raise FieldValueError(
            f"Python version {python_runtime} is not supported. Supported versions are {allowed_runtimes}"
        )


def read_service_settings(
    yaml_file: Path = Path("mlops_service_settings.yaml"),
) -> ServiceSettings:
    """Read service settings from the mlops_service_settings.yaml file during deployment

    Args:
        yaml_file (Path, optional): path object to settings file. Defaults to Path("mlops_service_settings.yaml").

    Returns:
        ServiceSettings: service settings for the model to deploy
    """
    logger.info("Read service settings")
    with yaml_file.open() as f:
        settings = yaml.safe_load(f.read())
    service_settings = ServiceSettings(**settings)
    return service_settings


def validate_user_settings(yaml_file: Path = Path("mlops_settings.yaml")) -> None:
    """Validate the mlops_settings.yaml file

    Args:
        yaml_file (Path, optional): path to settings file. Defaults to Path("mlops_settings.yaml").
    """
    try:
        read_project_settings(yaml_file)
        logger.info("Settings file is ok :)")
    except Exception:
        trace = traceback.format_exc()
        error_message = f"Settings file is not ok! Fix this:\n{trace}"
        logger.error(error_message)
