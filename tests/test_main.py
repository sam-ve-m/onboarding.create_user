# PROJECT IMPORTS
from http import HTTPStatus

import flask
import pytest
from unittest.mock import patch, MagicMock

from decouple import RepositoryEnv, Config
import logging.config


with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from main import create_user
                from src.domain.enums.response.code import InternalCode
                from src.domain.response.model import ResponseModel
                from src.domain.exceptions.exceptions import (
                    InvalidEmail,
                    EmailAlreadyExists,
                    ErrorOnSendAuditLog,
                    ErrorOnSendIaraMessage,
                )
                from src.domain.validators.validator import UserParams
                from src.services.user_register import UserService


invalid_email_case = (
    InvalidEmail(),
    "Validator::validate_email::Invalid email format",
    InternalCode.INVALID_PARAMS,
    InvalidEmail.msg,
    HTTPStatus.BAD_REQUEST,
)
duplicated_email_case = (
    EmailAlreadyExists(),
    "UserService::verify_email_already_exists:: Email already exists",
    InternalCode.DATA_ALREADY_EXISTS,
    EmailAlreadyExists.msg,
    HTTPStatus.BAD_REQUEST,
)
persephone_case = (
    ErrorOnSendAuditLog(),
    "Audit::register_user_log::Error on trying to register log",
    InternalCode.PARTNERS_ERROR,
    "Audit::register_user_log::Error on trying to register log",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
iara_case = (
    ErrorOnSendIaraMessage(),
    "Audit::register_user_log::Error on trying to register log",
    InternalCode.PARTNERS_ERROR,
    "Audit::register_user_log::Error on trying to register log",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
value_exception_case = (
    ValueError("dummy"),
    "dummy",
    InternalCode.INVALID_PARAMS,
    "Invalid params",
    HTTPStatus.BAD_REQUEST,
)
exception_case = (
    Exception("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception,error_message,internal_status_code,response_message,response_status_code",
    [
        invalid_email_case,
        duplicated_email_case,
        persephone_case,
        iara_case,
        value_exception_case,
        exception_case,
    ],
)
@patch.object(UserParams, "__init__", return_value=None)
@patch.object(UserService, "__init__", return_value=None)
@patch.object(UserService, "verify_email_already_exists")
@patch.object(UserService, "register")
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
async def test_create_user_raising_errors(
    mocked_build_response,
    mocked_response_instance,
    mocked_logger,
    mocked_register,
    mocked_validation,
    mocked_service,
    mocked_model,
    monkeypatch,
    exception,
    error_message,
    internal_status_code,
    response_message,
    response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_service.side_effect = exception
    await create_user()
    mocked_register.assert_not_called()
    mocked_validation.assert_not_called()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False, code=internal_status_code.value, message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(UserParams, "__init__", return_value=None)
@patch.object(UserService, "__init__", return_value=None)
@patch.object(UserService, "verify_email_already_exists")
@patch.object(UserService, "register", return_value=dummy_response)
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
async def test_create_user(
    mocked_build_response,
    mocked_response_instance,
    mocked_logger,
    mocked_register,
    mocked_validation,
    mocked_service,
    mocked_model,
    monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await create_user()
    mocked_service.assert_called()
    mocked_register.assert_called()
    mocked_validation.assert_called()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        success=dummy_response,
        code=InternalCode.SUCCESS.value,
        message="User successfully created",
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
