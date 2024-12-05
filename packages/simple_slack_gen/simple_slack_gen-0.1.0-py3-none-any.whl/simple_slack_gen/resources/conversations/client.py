import typing

from simple_slack_gen.core import (
    AsyncBaseClient,
    QueryParams,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    encode_param,
)
from simple_slack_gen.types import models


class ConversationsClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client
        # register sync resources (keep comment for code generation)

    # register sync api methods (keep comment for code generation)
    def list(
        self,
        *,
        cursor: typing.Optional[str] = None,
        exclude_archived: typing.Optional[bool] = None,
        limit: typing.Optional[int] = None,
        team_id: typing.Optional[str] = None,
        types_query: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ListConversationsResponse:
        """
        Lists channels in the workspace.

        GET /conversations.list
        """

        # start -- build request data (keep comment for code generation)
        _query: QueryParams = {}
        if cursor is not None:
            _query["cursor"] = encode_param(cursor, False)
        if exclude_archived is not None:
            _query["exclude_archived"] = encode_param(exclude_archived, False)
        if limit is not None:
            _query["limit"] = encode_param(limit, False)
        if team_id is not None:
            _query["team_id"] = encode_param(team_id, False)
        if types_query is not None:
            _query["types"] = encode_param(types_query, False)
        # end -- build request data (keep comment for code generation)

        # start -- send sync request (keep comment for code generation)
        return self._base_client.request(
            method="GET",
            path="/conversations.list",
            auth_names=["auth"],
            query_params=_query,
            cast_to=models.ListConversationsResponse,
            request_options=request_options or default_request_options(),
        )
        # end -- send sync request (keep comment for code generation)


class AsyncConversationsClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client
        # register async resources (keep comment for code generation)

    # register async api methods (keep comment for code generation)
    async def list(
        self,
        *,
        cursor: typing.Optional[str] = None,
        exclude_archived: typing.Optional[bool] = None,
        limit: typing.Optional[int] = None,
        team_id: typing.Optional[str] = None,
        types_query: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.ListConversationsResponse:
        """
        Lists channels in the workspace.

        GET /conversations.list
        """

        # start -- build request data (keep comment for code generation)
        _query: QueryParams = {}
        if cursor is not None:
            _query["cursor"] = encode_param(cursor, False)
        if exclude_archived is not None:
            _query["exclude_archived"] = encode_param(exclude_archived, False)
        if limit is not None:
            _query["limit"] = encode_param(limit, False)
        if team_id is not None:
            _query["team_id"] = encode_param(team_id, False)
        if types_query is not None:
            _query["types"] = encode_param(types_query, False)
        # end -- build request data (keep comment for code generation)

        # start -- send async request (keep comment for code generation)
        return await self._base_client.request(
            method="GET",
            path="/conversations.list",
            auth_names=["auth"],
            query_params=_query,
            cast_to=models.ListConversationsResponse,
            request_options=request_options or default_request_options(),
        )
        # end -- send async request (keep comment for code generation)
