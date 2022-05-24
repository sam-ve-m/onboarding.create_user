class InvalidEmail(Exception):
    msg = "Invalid email address"


class EmailAlreadyExists(Exception):
    msg = "Email alredy exists"


class ErrorOnSendAuditLog(Exception):
    msg = "Error when trying to send log audit on Persephone"


class ErrorOnRegisterUserSocial(Exception):
    msg = "Error when trying to register user on Social"
