from paymob import http


class CreateResourceMixin(object):
    @classmethod
    def create(cls, secret_key=None, path=None, **kwargs):
        """
        Create resource

        :param secret_key: Paymob's secret key
        :param kwargs: dict
        """
        request = http.HTTPRequest(
            resource=cls,
            method="post",
            secret_key=secret_key,
        )
        request = request.request(payload=kwargs)
        return request


class UpdateResourceMixin(object):
    @classmethod
    def update(cls, secret_key=None, **kwargs):
        """
        Update resource

        :param secret_key: Paymob's secret key
        :param kwargs: dict
        """
        request = http.HTTPRequest(
            resource=cls,
            method="put",
            secret_key=secret_key,
        )
        request = request.request(payload=kwargs)
        return request


class PatchResourceMixin(object):
    @classmethod
    def patch(cls, secret_key=None, **kwargs):
        """
        Patch resource

        :param secret_key: Paymob's secret key
        :param kwargs: dict
        """
        request = http.HTTPRequest(
            resource=cls,
            method="patch",
            secret_key=secret_key,
        )
        request = request.request(payload=kwargs)
        return request


class DeleteResourceMixin(object):
    @classmethod
    def delete(cls, reference, secret_key=None, **kwargs):
        """
        Delete resource

        :param secret_key: Paymob's secret key
        :param kwargs: dict
        """
        request = http.HTTPRequest(
            resource=cls,
            method="delete",
            secret_key=secret_key,
        )
        request = request.request(reference=reference)
        return request


class RetrieveResourceMixin(object):
    @classmethod
    def retrieve(cls, reference ,secret_key=None, **kwargs):
        """
        Retrieve resource

        :param secret_key: Paymob's secret key
        :param kwargs: dict
        """
        request = http.HTTPRequest(
            resource=cls,
            method="get",
            secret_key=secret_key,
        )
        request = request.request(reference=reference)
        return request


class ListResourceMixin(object):
    @classmethod
    def list(cls, secret_key=None, **kwargs):
        """
        List resource

        :param secret_key: Paymob's secret key
        :param kwargs: dict
        """
        request = http.HTTPRequest(
            resource=cls,
            method="get",
            secret_key=secret_key,
        )
        request = request.request(querystr=kwargs)
        return request


class GenericResourceMixin(
    CreateResourceMixin,
    UpdateResourceMixin,
    DeleteResourceMixin,
    RetrieveResourceMixin,
    ListResourceMixin,
):
    """
    Generic Create, Update, Delete, List resource

    :param secret_key: Paymob's secret key
    :param kwargs: dict
    """

    pass
