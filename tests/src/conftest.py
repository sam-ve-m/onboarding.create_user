# Jormungandr-Onboarding
from func.src.services.user_register import UserService
from .stub import stub_user_params

# Third party
from pytest import fixture


@fixture(scope="function")
def user_service():
    setup_service_instance = UserService(user_params=stub_user_params)
    return setup_service_instance
