import httpx
import typing

from simple_slack_gen.core import AsyncBaseClient, AuthBearer, SyncBaseClient
from simple_slack_gen.environment import Environment
from simple_slack_gen.resources.conversations import (
    AsyncConversationsClient,
    ConversationsClient,
)
from simple_slack_gen.resources.chat import AsyncChatClient, ChatClient


class Client:
    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.Client] = None,
        environment: Environment = Environment.LIVE,
        oauth_token: typing.Optional[str] = None,
    ):
        self._base_client = SyncBaseClient(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            httpx_client=(
                httpx.Client(timeout=timeout) if httpx_client is None else httpx_client
            ),
        )

        # register auth methods (keep comment for code generation)
        self._base_client.register_auth("auth", AuthBearer(val=oauth_token))

        # register sync resources (keep comment for code generation)
        self.conversations = ConversationsClient(base_client=self._base_client)
        self.chat = ChatClient(base_client=self._base_client)

    # register sync api methods (keep comment for code generation)


class AsyncClient:
    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
        environment: Environment = Environment.LIVE,
        oauth_token: typing.Optional[str] = None,
    ):
        self._base_client = AsyncBaseClient(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            httpx_client=(
                httpx.AsyncClient(timeout=timeout)
                if httpx_client is None
                else httpx_client
            ),
        )

        # register auth methods (keep comment for code generation)
        self._base_client.register_auth("auth", AuthBearer(val=oauth_token))

        # register async resources (keep comment for code generation)
        self.conversations = AsyncConversationsClient(base_client=self._base_client)
        self.chat = AsyncChatClient(base_client=self._base_client)

    # register async api methods (keep comment for code generation)


def _get_base_url(
    *, base_url: typing.Optional[str] = None, environment: Environment
) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Must include a base_url or environment arguments")
