class MissingFieldError(Exception):
    """Raised when fields are missing from mlops_settings.yaml"""


class FieldValueError(Exception):
    """Raised when field values are invalid"""


class MissingMetadataError(Exception):
    """Raised when fields are missing from the metadata (from mlops_settings.yaml)"""


class TooMuchMetadata(Exception):
    """Raised when there is too much metadata (from mlops_settings.yaml)"""


class TestError(Exception):
    """Raised when tests are failing"""


class DeploymentError(Exception):
    """Raised when deployment fails"""


class FunctionNameError(Exception):
    """Raised when function name (in CDF) is invalid"""


class FunctionCallError(Exception):
    """Raised when function call fails"""


class MissingClientError(Exception):
    """Raised when a global cognite client is missing, i.e. not set up"""


class VirtualEnvironmentError(Exception):
    """Raised when something is wrong when creating or deleting a virtual environment during deployments"""


class MLOpsError(Exception):
    """Generic MLOps exception"""


class MissingDeploymentFolder(Exception):
    """Raised when failing to download the deployment folder"""


class MissingResponseError(Exception):
    """Raised when function call return an empty response"""


class MissingModelArtifactsError(Exception):
    """Raised when queried model artifacts are missing"""


class MissingSettingsFileError(Exception):
    """Raised when mlops_settings.yaml is missing"""


class DependencyMismatchError(Exception):
    """Raised when there is a mismatch between main model and helper model dependencies"""
