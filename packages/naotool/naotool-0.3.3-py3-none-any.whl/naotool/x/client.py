import base64
import datetime
from typing import TypeVar

import httpx
from httpx_auth import OAuth2AuthorizationCode, OAuth2AuthorizationCodePKCE

from ..httpn import AutoCloseAsyncClient

__all__ = ["AsyncClient"]


PKCE = TypeVar("PKCE")
APP_ONLY = TypeVar("App-only")
AuthType = PKCE | APP_ONLY | list[PKCE, APP_ONLY]


class AsyncBaseClient:
    _client: AutoCloseAsyncClient
    uri: str
    proxy: str
    headers: dict
    bearer_token: str
    PKCE: OAuth2AuthorizationCodePKCE
    client_id: str
    client_secret: str

    def __init__(
        self,
        bearer_token: str = None,
        *,
        consumer_key: str = None,
        consumer_secret: str = None,
        access_token: str = None,
        access_token_secret: str = None,
        client_id: str = "",
        client_secret: str = "",
        client: AutoCloseAsyncClient = None,
        uri: str = "https://api.x.com",
        proxy: str = "http://127.0.0.1:7890",
        wait_on_rate_limit=False,
    ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.client_id = client_id
        self.client_secret = client_secret

        self._client = client
        self.uri = uri
        self.proxy = proxy
        self.wait_on_rate_limit = wait_on_rate_limit

        self.PKCE = OAuth2AuthorizationCode(
            "https://www.x.com/oauth2/authorize",
            "https://www.x.com/oauth2/token",
            client_id=client_id,
            client_secret=client_secret,
        )
        self.bearer_token = bearer_token

        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/130.0.0.0 Safari/537.36"
            ),
        }
        self._client = AutoCloseAsyncClient(proxy="http://127.0.0.1:7890")

    async def get_bearer_token(self):
        basic = f"{self.consumer_key}:{self.consumer_secret}"
        basic = base64.b64encode(basic.encode("utf-8")).decode("utf-8")
        # 获取 Bearer Token
        url = "https://api.x.com/oauth2/token"
        headers = {
            "Host": "api.x.com",
            "User-Agent": "tomorinao bot v1.0.23",
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Content-Length": "29",
            "Accept-Encoding": "gzip",
        }
        data = {"grant_type": "client_credentials"}
        async with AutoCloseAsyncClient(proxy=self.proxy) as client:
            response = await client.post(
                url,
                headers=headers,
                data=data,
            )
            if response.is_error:
                print(response.text)
        # response.raise_for_status()
        self.bearer_token = response.json().get("access_token")
        return self.bearer_token

    async def request(
        self,
        method: str = "GET",
        route: str = None,
        url: str = None,
        auth_type=APP_ONLY,
        *,
        content=None,
        data=None,
        files=None,
        json=None,
        params=None,
        headers=None,
        **kwargs,
    ) -> httpx.Response:
        if not url:
            url = f"{self.uri}{route}"
        headers = self.headers
        if auth_type == "PKCE":
            kwargs["auth"] = self.PKCE
        elif not self.bearer_token:
            self.bearer_token = await self.get_bearer_token()
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        response = await self._client.request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            **kwargs,
        )
        response.raise_for_status()
        return response

    async def _request(
        self,
        method: str,
        route: str,
        url: str = None,
        auth_type: AuthType = APP_ONLY,
        **kwargs,
    ) -> httpx.Response:
        kwargs["params"] = self._process_params(
            kwargs["params"],
            kwargs["endpoint_parameters"],
        )
        del kwargs["endpoint_parameters"]
        return await self.request(
            method,
            route,
            url,
            auth_type,
            **kwargs,
        )

    def _process_params(self, params, endpoint_parameters):
        endpoint_parameters = {
            endpoint_parameter.replace(".", "_"): endpoint_parameter
            for endpoint_parameter in endpoint_parameters
        }

        res_params = {}
        for k, v in params.items():
            try:
                k = endpoint_parameters[k]
            except KeyError:
                print(f"Unexpected parameter: {k}")

            if isinstance(v, list):
                res_params[k] = ",".join(map(str, v))
            elif isinstance(v, datetime.datetime):
                if v.tzinfo is not None:
                    v = v.astimezone(datetime.timezone.utc)
                res_params[k] = v.strftime("%Y-%m-%dT%H:%M:%SZ")
                # TODO: Constant datetime format string?
            elif v is not None:
                res_params[k] = v

        return res_params


class AsyncClient(AsyncBaseClient):

    async def users_id_tweets(self, id: str, **params):
        """https://developer.x.com/en/docs/x-api/tweets/timelines/api-reference/get-users-id-tweets

        Endpoint URL:
            https://api.x.com/2/users/:id/tweets
        OAuth 2.0 scopes required by this endpoint:
            tweet.read
            users.read

        Args:
            id (str): Required
            end_time (str): "YYYY-MM-DDTHH:mm:ssZ".
                .strftime("%Y-%m-%dT%H:%M:%SZ")
        Returns:
            httpx.Response: Response
        """
        return await self._request(
            route=f"/2/users/{id}/tweets",
            method="GET",
            auth_type=list[PKCE, APP_ONLY],
            params=params,
            endpoint_parameters=(
                "end_time",
                "exclude",
                "expansions",
                "max_results",
                "media.fields",
                "pagination_token",
                "place.fields",
                "poll.fields",
                "since_id",
                "start_time",
                "tweet.fields",
                "until_id",
                "user.fields",
            ),
        )
