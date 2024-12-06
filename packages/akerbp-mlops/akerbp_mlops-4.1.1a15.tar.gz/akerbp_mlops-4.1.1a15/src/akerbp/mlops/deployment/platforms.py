# platforms.py
import typing


@typing.no_type_check
def get_methods():
    """
    Return a dictionary with methods to deploy and test functions for each
    platform (cdf or local). This decouples platforms and deployment

    Returns:
        (dict): dictionary with methods for deploying and testing functions for each platform supported by the framework
    """
    methods = {}

    # cdf
    from akerbp.mlops.cdf.helpers import (
        cdf_metadata_validation as cdf_metadata_validation,
    )
    from akerbp.mlops.cdf.helpers import deploy_function as cdf_deploy
    from akerbp.mlops.cdf.helpers import redeploy_function as cdf_redeploy
    from akerbp.mlops.cdf.helpers import test_function as cdf_test

    methods["cdf"] = cdf_deploy, cdf_redeploy, cdf_test, cdf_metadata_validation

    # local (methods don't do anything)
    local_deploy = local_test = local_redeploy = local_metadata_validation = (
        lambda *args, **kwargs: None
    )
    methods["local"] = (
        local_deploy,
        local_redeploy,
        local_test,
        local_metadata_validation,
    )

    return methods
