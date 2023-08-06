import re
import webbrowser

import grpc
from google.protobuf.empty_pb2 import Empty

import featurestore.core.CoreService_pb2 as pb
from featurestore.core.config import ConfigUtils

from .collections.pats import PersonalAccessTokens


class AuthWrapper:
    ACCESS_TOKEN_EXPIRES_SOON_SECS = 60

    def __init__(self, stub):
        self._stub = stub
        self._access_token = None
        self._access_token_expire = None
        self._get_access_token_external = None
        self._props = ConfigUtils.collect_properties()
        self.pats = PersonalAccessTokens(self._stub)

    def get_active_user(self):
        request = Empty()
        return self._stub.GetActiveUser(request).user

    def set_obtain_access_token_method(self, method):
        self._get_access_token_external = method

    def logout(self):
        try:
            self._obtain_token()
            if not AuthWrapper._is_personal_access_token(self._props["token"].data):
                request = pb.LogoutRequest()
                request.refresh_token = self._props["token"].data
                self._stub.Logout(request)
                self._access_token = None
                self._access_token_expire = None
            ConfigUtils.delete_property(self._props, ConfigUtils.TOKEN_KEY)
            print("You have been logged out.")
        except AuthException:
            print("You are not logged in.")

    def login(self):
        for response in self._stub.Login(Empty()):
            if response.HasField("login_url"):
                try:
                    webbrowser.get()
                except webbrowser.Error:
                    print(
                        f"Browser is not supported: Please visit {response.login_url} to continue authentication."
                    )
                print(f"Opening browser to visit: {response.login_url}")
                webbrowser.open(response.login_url)
            elif response.HasField("refresh_token"):
                self.set_auth_token(response.refresh_token)
            else:
                raise AuthException("Incorrect response")

    def set_auth_token(self, token):
        ConfigUtils.store_token(self._props, token)
        if not AuthWrapper._is_personal_access_token(token):
            self._access_token = None
            self._access_token_expire = None
            self._obtain_token()

    @staticmethod
    def _is_personal_access_token(token: str) -> bool:
        return re.match(r"^[a-z0-9]{3}_.*", token)

    def _is_access_token_expired(self):
        return self._access_token is None or (
            self._access_token_expire is not None
            and self._access_token_expire <= AuthWrapper.ACCESS_TOKEN_EXPIRES_SOON_SECS
        )

    def _obtain_token(self):
        if self._get_access_token_external is not None:
            return self._get_access_token_external()
        elif ConfigUtils.TOKEN_KEY not in self._props:
            raise AuthException(
                "You are not authenticated. Set personal access token or execute client.auth.login() method"
            )
        elif AuthWrapper._is_personal_access_token(ConfigUtils.get_token(self._props)):
            return ConfigUtils.get_token(self._props)
        elif self._is_access_token_expired():
            request = pb.RefreshTokenRequest()
            request.refresh_token = ConfigUtils.get_token(self._props)
            try:
                resp = self._stub.GetAccessToken(request)
            except grpc.RpcError as e:
                raise AuthException(
                    f"The authentication token is no longer valid. Please login again. Auth Server response: {str(e)}"
                )

            self._access_token = resp.access_token
            ConfigUtils.store_token(self._props, resp.refresh_token)
            self._access_token_expire = resp.expires_in
            return self._access_token
        else:
            return self._access_token

    def __repr__(self):
        return "This class wraps together methods related to Authentication"


class AuthException(Exception):
    pass
