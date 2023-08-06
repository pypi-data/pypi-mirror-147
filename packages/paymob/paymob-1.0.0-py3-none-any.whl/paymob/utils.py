import paymob


def next_api_version():
    """
    Next API version handler.
    :return: str
    """
    if paymob.next_version is not None:
        return paymob.next_version

    return "v1"


def resource_to_url(resource):
    """
    Convert any Resource's classes name to a valid API URL.
    :param resource: str
    :return: str
    """
    return "/{next_api_version}/{resource}/".format(
        next_api_version=next_api_version(), resource=resource
    )


def api_base_url():
    """

    :return: str api_next_url
    """
    api_next_url = "https://flashapi.paymob.com"

    if paymob.base_url is not None:
        return paymob.base_url

    return api_next_url

