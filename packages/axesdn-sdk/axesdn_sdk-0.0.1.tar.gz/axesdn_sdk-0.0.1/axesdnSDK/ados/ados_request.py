

class AdosRequest(object):

    def __init__(self, name, category, method, uri):
        """
        Base class of ADOS request

        :param name: string, name of request
        :param category: string, category of request
        :param method: string, method of request
        :param uri: string, uri of request
        """
        self._name = name
        self._category = category
        self._method = method
        self._uri = uri
        self._params = {}

    def _set_param(self, param, value):
        self._params[param] = value

    def _get_param(self, param):
        if self._params and self._params.get(param):
            return self._params.get(param)
        return None

    def get_name(self):
        """
        Get name of request

        :return: string
        """
        return self._name

    def get_method(self):
        """
        Get method of request

        :return: string
        """
        return self._method

    def get_category(self):
        """
        Get category of request

        :return: string
        """
        return self._category

    def get_uri(self):
        """
        Get uri of request

        :return: string
        """
        return self._uri

    def get_params(self):
        """
        Get parameters of request

        :return: dict
        """
        return self._params
