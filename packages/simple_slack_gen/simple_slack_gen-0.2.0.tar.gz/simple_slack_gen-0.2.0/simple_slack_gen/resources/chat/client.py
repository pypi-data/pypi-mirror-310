import typing

from simple_slack_gen.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    to_encodable,
)
from simple_slack_gen.types import models, params


class ChatClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client
        # register sync resources (keep comment for code generation)

    # register sync api methods (keep comment for code generation)
    def post_message(
        self,
        *,
        data: params.NewMessage,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.MessageResponse:
        """
        Sends a message to a channel.

        POST /chat.postMessage
        """

        # start -- build request data (keep comment for code generation)
        _json = to_encodable(item=data, dump_with=params._SerializerNewMessage)
        # end -- build request data (keep comment for code generation)

        # start -- send sync request (keep comment for code generation)
        return self._base_client.request(
            method="POST",
            path="/chat.postMessage",
            auth_names=["auth"],
            json=_json,
            cast_to=models.MessageResponse,
            request_options=request_options or default_request_options(),
        )
        # end -- send sync request (keep comment for code generation)


class AsyncChatClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client
        # register async resources (keep comment for code generation)

    # register async api methods (keep comment for code generation)
    async def post_message(
        self,
        *,
        data: params.NewMessage,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.MessageResponse:
        """
        Sends a message to a channel.

        POST /chat.postMessage
        """

        # start -- build request data (keep comment for code generation)
        _json = to_encodable(item=data, dump_with=params._SerializerNewMessage)
        # end -- build request data (keep comment for code generation)

        # start -- send async request (keep comment for code generation)
        return await self._base_client.request(
            method="POST",
            path="/chat.postMessage",
            auth_names=["auth"],
            json=_json,
            cast_to=models.MessageResponse,
            request_options=request_options or default_request_options(),
        )
        # end -- send async request (keep comment for code generation)
