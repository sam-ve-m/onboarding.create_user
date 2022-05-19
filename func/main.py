# Jormungandr
from src.domain.enums.response.code import InternalCode
from src.domain.validator import UserParams
from src.services.user_register import UserService
from src.domain.response.model import ResponseModel
from src.domain.exceptions import (InvalidEmail, EmailAlredyExists,
                                   ErrorOnRegisterUserSocial,
                                   ErrorOnSendAuditLog)

# Standards
from http import HTTPStatus

# Third party
from flask import request
from etria_logger import Gladsheim


def create_user():
    raw_params = request.json
    try:
        user_params = UserParams(**raw_params).dict()
        user_service = UserService(user_params=user_params)
        user_service.verify_email_alredy_exists()
        success = user_service.register()
        response = ResponseModel(success=success, code=InternalCode.SUCCESS).build_http_response(
            status=HTTPStatus.OK)
        return response

    except EmailAlredyExists:
        response = ResponseModel(success=True, code=InternalCode.DATA_ALREDY_EXISTS).build_http_response(
            status=HTTPStatus.CONFLICT)
        return response

    except ErrorOnRegisterUserSocial:
        response = ResponseModel(success=False, code=InternalCode.PARTNERS_ERROR).build_http_response(
            status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnSendAuditLog:
        response = ResponseModel(success=False, code=InternalCode.PARTNERS_ERROR).build_http_response(
            status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except InvalidEmail:
        response = ResponseModel(success=False, code=InternalCode.INVALID_PARAMS).build_http_response(
            status=HTTPStatus.BAD_REQUEST)
        return response

    except ValueError:
        response = ResponseModel(success=False, code=InternalCode.INVALID_PARAMS).build_http_response(
            status=HTTPStatus.BAD_REQUEST
        )
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message="Unexpected error occurred")
        response = ResponseModel(success=False, code=InternalCode.INTERNAL_SERVER_ERROR).build_http_response(
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return response
