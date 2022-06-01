# Jormungandr
from src.domain.enums.response.code import InternalCode
from src.domain.validator import UserParams
from src.services.user_register import UserService
from src.domain.response.model import ResponseModel
from src.domain.exceptions import (
    InvalidEmail,
    EmailAlreadyExists,
    ErrorOnRegisterUserSocial,
    ErrorOnSendAuditLog,
)

# Standards
from http import HTTPStatus

# Third party
from flask import request
from etria_logger import Gladsheim


async def create_user():
    raw_params = request.json
    message = "Unexpected error occurred"
    try:
        user_params = UserParams(**raw_params).dict()
        user_service = UserService(user_params=user_params)
        await user_service.verify_email_already_exists()
        success = await user_service.register()
        response = ResponseModel(
            success=success,
            code=InternalCode.SUCCESS,
            message="User successfully created",
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except EmailAlreadyExists as ex:
        response = ResponseModel(
            success=True,
            code=InternalCode.DATA_ALREADY_EXISTS,
            message=ex.msg,
        ).build_http_response(status=HTTPStatus.CONFLICT)
        return response

    except ErrorOnRegisterUserSocial:
        response = ResponseModel(
            success=False, code=InternalCode.PARTNERS_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnSendAuditLog:
        response = ResponseModel(
            success=False, code=InternalCode.PARTNERS_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except InvalidEmail as ex:
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message=ex.msg,
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ValueError:
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
