import json
import requests
import threading
import base64
from datetime import datetime, timedelta
from axesdnSDK.ados.ados_request import *
from axesdnSDK.ados.exception import *
from axesdnSDK.ados.const import *


def create_client(api_access_key=None, api_access_secret=None, endpoint_url=DEFAULT_CLIENT_ENDPOINT_URL, verify=True,
                  timeout=DEFAULT_CLIENT_TIMEOUT_SECONDS, retries=DEFAULT_CLIENT_RETRIES):
    """
    creator of ADOS client

    :param api_access_key: string, ADOS API access key
    :param api_access_secret: string, ADOS API access secret
    :param endpoint_url: string, ADOS API endpoint
    :param verify: bool, verify the certificate if https is used in endpoint
    :param timeout: int, timeout for request in second
    :param retries: int, times of retry if request fail with certain reason
    :return: Client
    """
    if api_access_key is None:
        raise AdosParameterError("'api_access_key' can't be empty")
    if api_access_secret is None:
        raise AdosParameterError("'api_access_secret' can't be empty")
    # disable warning if there is no verify
    if not verify:
        requests.packages.urllib3.disable_warnings()

    return Client(api_access_key, api_access_secret, endpoint_url, timeout, verify, retries)


def _calculate_expired_time(token):
    token_parts = token.split(".")
    if len(token_parts) != 3:
        raise AdosParseError("token " + token + " is illegal")

    claim_bytes = base64.urlsafe_b64decode(token_parts[1]+"="*divmod(len(token_parts[1]), 4)[1])
    claims = json.loads(claim_bytes)
    expired_time = datetime.now() + timedelta(seconds=(claims["exp"] - claims["iat"]))

    return expired_time


class Client(object):
    """
    Client for calling request to ADOS
    """
    def __init__(self, api_access_key, api_access_secret, endpoint_url, timeout, verify, retries):
        self.lock = threading.Lock()
        self._key = api_access_key
        self._secret = api_access_secret
        self._endpoint = endpoint_url
        self._timeout = timeout
        self._verify = verify
        self._retries = retries
        self._access_token = None
        self._access_token_expired_time = None
        self._refresh_token = None
        self._refresh_token_expired_time = None

    def _login(self):
        """
        Login ADOS with credential and store tokens
        """
        url = self._endpoint + "/api/v1/login"
        headers = {
            "Content-Type": "application/json"
        }
        credential = {
            "api_access_key": self._key,
            "api_access_secret": self._secret
        }
        loops = 1 + self._retries
        for loop in range(loops):
            try:
                resp = requests.post(url=url, headers=headers, json=credential, verify=self._verify,
                                     timeout=self._timeout)
            except Exception as e:
                if INTERNAL_SERVER_ERROR in str(e) and loop < loops - 1:
                    continue
                else:
                    raise AdosLoginError(str(e))
            break

        if resp.status_code != 200:
            raise AdosLoginError(resp.text)
        try:
            resp_json = resp.json()
            self._access_token = resp_json["access_token"]
            self._access_token_expired_time = _calculate_expired_time(self._access_token)
            self._refresh_token = resp_json["refresh_token"]
            self._refresh_token_expired_time = _calculate_expired_time(self._refresh_token)
        except Exception as e:
            raise AdosLoginError(str(e))

    def _refresh(self):
        """
        Refresh access token when it's expired, if refresh token is also expired, try to re-login
        """
        url = self._endpoint + "/api/v1/refresh"
        headers = {
            "Authorization": "Bearer "+self._refresh_token,
            "Accept": "application/json"
        }

        try:
            resp = requests.post(url=url, headers=headers, verify=self._verify, timeout=self._timeout)
        except Exception as e:
            if TOKEN_HAS_EXPIRED in str(e):
                # re-login refresh token is expired
                self._login()
                return
            else:
                raise AdosRefreshError(str(e))

        if resp.status_code != 200:
            raise AdosRefreshError(resp.text)
        try:
            resp_json = resp.json()
            self._access_token = resp_json["access_token"]
            self._access_token_expired_time = _calculate_expired_time(self._access_token)
        except Exception as e:
            raise AdosRefreshError(str(e))

    def _get_url(self, ados_request):
        """
        Get request URL based on ados request

        :param ados_request: AdosRquest
        :return: url: string
        :rtype: string
        """
        url = self._endpoint + "/" + ados_request.get_uri()
        params = ""
        params_dict = ados_request.get_params()
        for param in params_dict:
            params += param + "=" + params_dict[param] + "&"
        if params:
            # remove last &
            url += "?" + params[:-1]
        return url

    def _get_access_token(self):
        """
        Get access token for doing request, if it's expired, then try to refresh access token, if refresh token is also
        expired, then try to re-login

        :return: access_token: string
        :rtype: string
        """
        self.lock.acquire()
        try:
            if self._access_token is None or self._refresh_token is None:
                # no any token, just login in first
                self._login()
                return self._access_token
            time_now = datetime.now()
            # if access token is expired
            if time_now >= self._access_token_expired_time:
                # if refresh token is expired
                if time_now >= self._refresh_token_expired_time:
                    self._login()
                else:
                    self._refresh()
        finally:
            self.lock.release()
        return self._access_token

    def _do_get_request(self, ados_request):
        """
        Implement GET request

        :param ados_request: AdosRequest
        :return: Response
        :rtype: dict
        """
        url = self._get_url(ados_request)
        loops = 1 + self._retries
        for loop in range(loops):
            access_token = self._get_access_token()
            headers = {
                "Authorization": "Bearer " + access_token,
                "Accept": "application/json",
            }
            try:
                resp = requests.get(url=url, headers=headers, verify=self._verify, timeout=self._timeout)
            except Exception as e:
                if TOKEN_HAS_EXPIRED in str(e) and loop < loops - 1:
                    continue
                else:
                    raise AdosServerError(str(e))
            break

        if resp.status_code != 200:
            raise AdosServerError(resp.text)
        try:
            resp_json = resp.json()
        except Exception as e:
            raise AdosServerError("parse json with error: " + str(e))

        return resp_json

    def do_request(self, ados_request):
        """
        Execute ADOS request

        :param ados_request: AdosRequest
        :return: Response
        :rtype: dict
        """
        if not isinstance(ados_request, AdosRequest):
            raise AdosDataTypeError("The request type is not correct")
        if ados_request.get_method() == "GET":
            return self._do_get_request(ados_request)
        else:
            raise AdosClientError("Unsupported method for ados request")



