from http import HTTPStatus


class UserNotAllowed(Exception):
    """

    Exception handles the requests that a requester is not allowed to perform.
    :returns 403 error code

    """

    status_code = HTTPStatus.FORBIDDEN
    default_detail = "User is not allowed to perform this request"
    default_code = "user_not_allowed"


class TokenAlreadyRegistered(Exception):
    """
    Exception raised when a user try to regenerate secret keys above his limit.
    :returns 429 error code

    """

    status_code = HTTPStatus.TOO_MANY_REQUESTS
    default_detail = (
        "Secret Key already registered, try to revoke it and create new one"
    )
    default_code = "secret_key_already_registered"


class ExistingMerchantDetails(Exception):
    """
    Exception raised when a user try to assign an existing merchant detail to another.
    :returns 409 error code

    """

    status_code = HTTPStatus.CONFLICT
    default_detail = (
        "One of the assigned merchant details was registered to another merchant, "
        "please recheck the submitted details"
    )
    default_code = "existing_merchant_details"


class KeyRevoked(Exception):
    """
    Exception raised when a user successfully revoke secret key/API key.
    :returns 202 error code

    """

    status_code = HTTPStatus.ACCEPTED
    default_detail = "Key was revoked successfully, please create new one"
    default_code = "object_was_revoked"


class NonExistingInstance(Exception):
    """

    Exception raised when a user try get non-existing detail from the service.
    :returns 404 error code

    """

    status_code = HTTPStatus.NOT_FOUND
    default_detail = "Not existing instance"
    default_code = "not_existing_instances"
