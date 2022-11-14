# Jormungandr - Onboarding
from src.domain.enums.response.code import InternalCode
from src.domain.validators.validator import UserParams
from src.services.user_register import UserService
from src.domain.response.model import ResponseModel
from src.domain.exceptions.exceptions import (
    InvalidEmail,
    EmailAlreadyExists,
    ErrorOnSendAuditLog,
    ErrorOnSendIaraMessage,
)

# Standards
from http import HTTPStatus

# Third party
import flask
from etria_logger import Gladsheim


async def create_user() -> flask.Response:
    raw_payload = flask.request.json
    try:
        payload_validated = UserParams(**raw_payload)
        user_service = UserService(payload_validated=payload_validated)
        await user_service.verify_email_already_exists()
        success = await user_service.register()
        response = ResponseModel(
            success=success,
            code=InternalCode.SUCCESS.value,
            message="User successfully created",
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except InvalidEmail as ex:
        message = "Validator::validate_email::Invalid email format"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS.value,
            message=ex.msg,
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except EmailAlreadyExists as ex:
        message = "UserService::verify_email_already_exists:: Email already exists"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False,
            code=InternalCode.DATA_ALREADY_EXISTS.value,
            message=ex.msg,
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except (ErrorOnSendAuditLog, ErrorOnSendIaraMessage) as ex:
        message = "Audit::register_user_log::Error on trying to register log"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.PARTNERS_ERROR.value, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ValueError as ex:
        message = "Invalid params"
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS.value, message=message
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        message = "Unexpected error occurred"
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR.value,
            message=message,
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
