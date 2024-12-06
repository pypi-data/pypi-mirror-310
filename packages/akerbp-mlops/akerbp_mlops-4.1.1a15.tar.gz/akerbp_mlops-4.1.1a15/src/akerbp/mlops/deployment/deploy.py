"""
deploy.py

Deploy services in either Google Cloud Run or CDF Functions.
Model registry uses CDF Files.
"""

import ast
import os
import traceback
from pathlib import Path
from typing import Dict, List, Optional

import akerbp.mlops.model_manager as mm
from akerbp.mlops import __version__ as package_version
from akerbp.mlops.core.config import (
    HelperModel,
    ServiceSettings,
    read_env_vars,
    read_project_settings,
    store_service_settings,
)
from akerbp.mlops.core.exceptions import DependencyMismatchError

# Global variables
from akerbp.mlops.core.logger import get_logger
from akerbp.mlops.deployment import helpers

logger = get_logger(__name__)


def deploy_model(  # noqa: C901
    model_settings: ServiceSettings,
) -> str:
    """
    Deploy a model.

    This will create a deployment folder and change current working directory
    to it.

    Return "OK" if deployment was successful, otherwise return a string with the traceback for the failed deployment

    Args:
        model_settings (ServiceSettings): settings for the model service
        platform_methods (dict): where key is the platform and value is a tuple with deploy and test functions.
            Defaults to the globally set platform_methods variable.

    Returns:
        (str): status of the deployment
    """
    c = model_settings
    try:
        original_req_file = c.req_file
        envs = read_env_vars()
        env = envs.model_env
        testing_only = eval(envs.testing_only)
        service_name = envs.service_name
        platform = envs.platform
        if service_name is None:
            raise ValueError(
                "SERVICE_NAME environment variable must be set to either 'prediction' or 'training'"
            )
        deployment_folder = helpers.deployment_folder_path(c.model_name)
        function_name = f"{c.model_name}-{service_name}-{env}"

        # Handle mlops internal testing settings
        mlops_testing = ast.literal_eval(os.environ.get("LOCAL_MLOPS_TESTING", "False"))  # type: ignore

        logger.info(
            f"Starting deployment and/or testing of model {c.human_friendly_model_name}"
        )

        if (service_name == "prediction") and c.artifact_folder:
            if platform == "cdf" or platform == "local":
                mm.set_active_dataset(c.dataset)
                c.model_id = mm.set_up_model_artifact(c.artifact_folder, c.model_name)

        logger.info("Create deployment folder and move required files/folders")
        deployment_folder.mkdir()
        # Write settings to deployment folder
        store_service_settings(c, deployment_folder / "mlops_service_settings.yaml")
        logger.info("Service settings %s", c)
        # Update requirements file with mlops version
        req_file = helpers.create_temporary_copy(c.req_file)
        c.req_file = req_file

        helpers.set_mlops_import(
            req_file=c.req_file,
            platform=c.platform,
            deployment_folder=deployment_folder if mlops_testing else None,
        )
        helpers.copy_to_deployment_folder(c.files, deployment_folder)

        logger.info(f"cd {deployment_folder}")
        os.chdir(deployment_folder)

        # Main model requirements
        main_model_requirements = helpers.requirements_to_dict(c.req_file)

        handle_helper_models_and_dependency_mismatch(
            c, main_model_requirements, c.helper_models, c.packages_to_check
        )

        # Deploy to CDF
        if c.platform == "cdf":
            if testing_only:
                logger.info(
                    f"Running tests for model {c.human_friendly_model_name} in {env}, will not deploy"
                )
                helpers.run_tests(c, setup_venv=True, deploy=False)
            else:
                helpers.do_deploy(
                    c,
                    env,
                    service_name,
                    function_name,
                    deployment_folder,
                    setup_venv=True,
                )
        return "OK"
    except (Exception, KeyboardInterrupt):
        # Remove deployment folder if it exists
        helpers.rm_deployment_folder(c.model_name)
        # Remove temporary requirements file if it exists
        if c.req_file != original_req_file:
            req_file = Path(c.req_file).resolve()
            logger.info("Removing temporary requirements file %s", req_file)
            if req_file.exists():
                req_file.unlink()
        trace = traceback.format_exc()
        return f"Model failed to deploy and/or tests failed! See the following traceback for more info: \n\n{trace}"


def handle_helper_models_and_dependency_mismatch(
    c: ServiceSettings,
    main_model_requirements: Dict[str, str],
    helper_models: Optional[List[HelperModel]],
    packages_to_check: Optional[List[str]],
):
    if helper_models is None:
        if packages_to_check is not None:
            logger.warning(
                "packages_to_check specified in mlops_settings, but helper_models is not. Will not check for dependency mismatch between main and helper models."
            )
        return
    root = Path().resolve()
    for helper_model in helper_models:
        logger.info(
            f"Checking for dependency mismatch between main model {c.model_name} and helper model {helper_model.model_name} for the following package(s): {packages_to_check}"
        )
        model_name = helper_model.model_name
        env = helper_model.env if helper_model.env is not None else "prod"
        version = helper_model.version
        helper_model_target = (
            root / helper_model.target_path
            if helper_model.target_path is not None
            else root / model_name
        )
        mm.download_deployment_folder(
            model_name=model_name,
            env=env,
            version=version,
            target_path=str(helper_model_target),
            files_to_ignore=[
                "handler.py",
                "mlops_service_settings.yaml",
            ],
        )
        path_to_helper_model_requirements = helper_model_target / "requirements.txt"
        if packages_to_check is None:
            logger.warning(
                f"{model_name} specified in mlops_settings as a helper model, but packages_to_check is not. Will not check for dependency mismatch between the main and {model_name} models."
            )
        else:
            # Build dictionary of helper model requirements
            helper_model_requirements = helpers.requirements_to_dict(
                path_to_helper_model_requirements
            )
            (
                is_dependency_mismatch,
                mismatched_packages,
            ) = helpers.check_mismatch_in_model_requirements(
                main_model_requirements=main_model_requirements,
                helper_model_requirements=helper_model_requirements,
                packages_to_check=packages_to_check,
            )
            if is_dependency_mismatch:
                raise DependencyMismatchError(
                    f"Dependency mismatch detected for helper model {helper_model} for the following package(s): {mismatched_packages}"
                )
            else:
                logger.info("No dependency mismatch detected for helper model")

        # Remove helper_model requirements file as this interferes with Cognite deployment
        path_to_helper_model_requirements.unlink()


def deploy(project_settings: List[ServiceSettings]) -> None:
    """
    Deploy a machine learning project that potentially contains multiple models.
    Deploy each model in the settings and make sure that if one model fails it
    does not affect the rest. At the end, if any model failed, it raises an
    exception with a summary of all models that failed.

    Args:
        Project settings as described by the user in the config file.

    Raises:
        Exception: If any model failed to deploy.
    """
    failed_models = {}
    cwd_path = Path.cwd()

    for c in project_settings:
        status = deploy_model(c)
        if status != "OK":
            logger.error(status)
            failed_models[c.human_friendly_model_name] = status

        logger.info("cd ..")
        os.chdir(cwd_path)
        helpers.rm_deployment_folder(c.model_name)

    if failed_models:
        for model, message in failed_models.items():
            logger.error(f"Model {model} failed: {message}")
        raise Exception("At least one model failed.")


def main() -> None:
    logger = get_logger(name="akerbp.mlops.deployment.deploy.py")
    if ast.literal_eval(os.environ.get("LOCAL_MLOPS_TESTING", "False")):
        message = "Deploying prediction service using the built wheel for testing purposes before releasing"
    else:
        message = f"Deploying prediction service using MLOps framework version {package_version}"

    logger.info(message)
    mm.setup()
    settings = read_project_settings()
    deploy(settings)


if __name__ == "__main__":
    main()
