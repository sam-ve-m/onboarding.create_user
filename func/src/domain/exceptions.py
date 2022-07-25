class InvalidEmail(Exception):
    msg = "Invalid email address"


class EmailAlreadyExists(Exception):
    msg = "Email already exists"


class ErrorOnSendAuditLog(Exception):
    msg = "Error when trying to send log audit on Persephone"
