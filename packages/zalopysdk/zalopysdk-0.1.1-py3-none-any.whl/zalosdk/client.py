import os
import requests
from typing import Optional
from pkce import get_code_challenge
from zalosdk.endpoint import Endpoint
from zalosdk.template import ZNSTplListRequest
from zalosdk.message import ZNSMessage


class AccessToken:
    __access_token: str
    __refresh_token: str
    __expires_in: int

    def __init__(self, access_token: str = "", refresh_token: str = "", expires_in: int = 0):
        """
        Initialize an AccessToken object.

        Parameters
        ----------
        access_token : str
            Access token.
        refresh_token : str
            Refresh token.
        expires_in : int
            Seconds until the access token expires.
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in

    @property
    def access_token(self) -> str:
        return self.__access_token

    @access_token.setter
    def access_token(self, value: any):
        if value is None:
            value = ""
        self.__access_token = str(value)

    @property
    def refresh_token(self) -> str:
        return self.__refresh_token

    @refresh_token.setter
    def refresh_token(self, value: any):
        if value is None:
            value = ""
        self.__refresh_token = str(value)

    @property
    def expires_in(self) -> int:
        return self.__expires_in

    @expires_in.setter
    def expires_in(self, value: any):
        if value is None:
            value = 0
        self.__expires_in = int(value)


class ZaloClient:
    __app_id: str
    __app_secret: str
    __code_verifier: str
    __code_challenge: str
    __access_token: AccessToken
    __http_proxy: Optional[str]
    __https_proxy: Optional[str]

    def __init__(self, app_id: str = None, app_secret: str = None, code_verifier: str = None, http_proxy: Optional[str] = None, https_proxy: Optional[str] = None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.code_verifier = code_verifier
        self.code_challenge = get_code_challenge(self.code_verifier)
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy

    @property
    def app_id(self) -> Optional[str]:
        return self.__app_id

    @app_id.setter
    def app_id(self, value: Optional[str]):
        if value is None:
            value = os.getenv("ZALO_APP_ID")
        self.__app_id = value

    @property
    def app_secret(self) -> Optional[str]:
        return self.__app_secret

    @app_secret.setter
    def app_secret(self, value: Optional[str]):
        if value is None:
            value = os.getenv("ZALO_APP_SECRET")
        self.__app_secret = value

    @property
    def code_verifier(self) -> Optional[str]:
        return self.__code_verifier

    @code_verifier.setter
    def code_verifier(self, value: Optional[str]):
        if value is None:
            value = os.getenv("ZALO_CODE_VERIFIER")
        self.__code_verifier = value

    @property
    def code_challenge(self) -> str:
        return self.__code_challenge

    @code_challenge.setter
    def code_challenge(self, value: str):
        self.__code_challenge = value

    @property
    def access_token(self) -> AccessToken:
        return self.__access_token

    @access_token.setter
    def access_token(self, value: AccessToken):
        self.__access_token = value

    @property
    def http_proxy(self) -> Optional[str]:
        return self.__http_proxy

    @http_proxy.setter
    def http_proxy(self, value: Optional[str]):
        if value == "" or not isinstance(value, str):
            value = None
        self.__http_proxy = value

    @property
    def https_proxy(self) -> Optional[str]:
        return self.__https_proxy

    @https_proxy.setter
    def https_proxy(self, value: Optional[str]):
        if value == "" or not isinstance(value, str):
            value = None
        self.__https_proxy = value

    def get_access_token(self, code: str) -> AccessToken:
        """
        Get access token from Zalo OAuth server.

        Parameters
        ----------
        code : str
            Authorization code received from OAuth flow

        Returns
        -------
        AccessToken
            Access token object containing access_token, refresh_token, and expires_in
        """
        response = requests.post(
            Endpoint.access_token(),
            data={
                'code': code,
                'app_id': self.app_id,
                'grant_type': 'authorization_code',
                'code_verifier': self.code_verifier
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'secret_key': self.app_secret
            },
            proxies={
                'http': self.http_proxy,
                'https': self.https_proxy
            },
        )

        data = response.json()
        return AccessToken(
            access_token=data.get('access_token'),
            refresh_token=data.get('refresh_token'),
            expires_in=data.get('expires_in')
        )

    def refresh_access_token(self, refresh_token: str) -> AccessToken:
        """
        Refresh access token using refresh token.

        Parameters
        ----------
        refresh_token : str
            Refresh token received from previous access token request

        Returns
        -------
        AccessToken
            Access token object containing access_token, refresh_token, and expires_in
        """
        response = requests.post(
            Endpoint.access_token(),
            data={
                'refresh_token': refresh_token,
                'app_id': self.app_id,
                'grant_type': 'refresh_token',
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'secret_key': self.app_secret
            },
            proxies={
                'http': self.http_proxy,
                'https': self.https_proxy
            },
        )

        data = response.json()
        return AccessToken(
            access_token=data.get('access_token'),
            refresh_token=data.get('refresh_token'),
            expires_in=data.get('expires_in')
        )

    def get_template_list(self, request: ZNSTplListRequest) -> dict:
        """
        Get list of templates with pagination and status filter.

        Parameters
        ----------
        request : ZNSTplListRequest
            Request object containing offset, limit and status parameters

        Returns
        -------
        dict
            Response containing template list and metadata
        """
        params = {
            'offset': max(0, request.offset),
            'limit': min(10, request.limit)
        }

        if request.status is not None:
            params['status'] = request.status.value

        response = requests.get(
            Endpoint.template_list(),
            params=params,
            headers={
                'access_token': self.access_token.access_token,
                'Content-Type': 'application/json'
            },
            proxies={
                'http': self.http_proxy,
                'https': self.https_proxy
            },
        )

        return response.json()

    def get_template_detail(self, template_id: str) -> dict:
        """
        Get template detail by template ID.
        """
        params = {
            'template_id': template_id
        }

        response = requests.get(
            Endpoint.template_detail(),
            params=params,
            headers={
                'access_token': self.access_token.access_token,
                'Content-Type': 'application/json'
            },
            proxies={
                'http': self.http_proxy,
                'https': self.https_proxy
            },
        )

        return response.json()

    def send_message(self, message: ZNSMessage) -> dict:
        """
        Send message to ZNS.
        """
        response = requests.post(
            Endpoint.message_send(),
            json=dict(message),
            headers={
                'access_token': self.access_token.access_token,
                'Content-Type': 'application/json'
            },
            proxies={
                'http': self.http_proxy,
                'https': self.https_proxy
            },
        )

        return response.json()
