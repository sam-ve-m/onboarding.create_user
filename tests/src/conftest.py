# Jormungandr - Onboarding
from func.src.services.user_register import UserService
from tests.src.stub import stub_payload_validated


# Third party
from pytest import fixture


@fixture(scope="function")
def user_service():
    setup_service_instance = UserService(payload_validated=stub_payload_validated)
    yield setup_service_instance
