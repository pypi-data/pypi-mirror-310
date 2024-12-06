import typing
import typing_extensions
import pydantic


class NewMessage(typing_extensions.TypedDict):
    """ """

    as_user: typing_extensions.NotRequired[str]
    attachments: typing_extensions.NotRequired[str]
    blocks: typing_extensions.NotRequired[str]
    channel: typing_extensions.Required[str]
    icon_emoji: typing_extensions.NotRequired[str]
    icon_url: typing_extensions.NotRequired[str]
    link_names: typing_extensions.NotRequired[bool]
    mrkdwn: typing_extensions.NotRequired[bool]
    parse: typing_extensions.NotRequired[str]
    reply_broadcast: typing_extensions.NotRequired[bool]
    text: typing_extensions.Required[str]
    thread_ts: typing_extensions.NotRequired[str]
    unfurl_links: typing_extensions.NotRequired[bool]
    unfurl_media: typing_extensions.NotRequired[bool]
    username: typing_extensions.NotRequired[str]


class _SerializerNewMessage(pydantic.BaseModel):
    """
    Serializer for NewMessage handling case conversions
    and file omitions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    as_user: typing.Optional[str] = pydantic.Field(alias="as_user", default=None)
    attachments: typing.Optional[str] = pydantic.Field(
        alias="attachments", default=None
    )
    blocks: typing.Optional[str] = pydantic.Field(alias="blocks", default=None)
    channel: str = pydantic.Field(alias="channel")
    icon_emoji: typing.Optional[str] = pydantic.Field(alias="icon_emoji", default=None)
    icon_url: typing.Optional[str] = pydantic.Field(alias="icon_url", default=None)
    link_names: typing.Optional[bool] = pydantic.Field(alias="link_names", default=None)
    mrkdwn: typing.Optional[bool] = pydantic.Field(alias="mrkdwn", default=None)
    parse: typing.Optional[str] = pydantic.Field(alias="parse", default=None)
    reply_broadcast: typing.Optional[bool] = pydantic.Field(
        alias="reply_broadcast", default=None
    )
    text: str = pydantic.Field(alias="text")
    thread_ts: typing.Optional[str] = pydantic.Field(alias="thread_ts", default=None)
    unfurl_links: typing.Optional[bool] = pydantic.Field(
        alias="unfurl_links", default=None
    )
    unfurl_media: typing.Optional[bool] = pydantic.Field(
        alias="unfurl_media", default=None
    )
    username: typing.Optional[str] = pydantic.Field(alias="username", default=None)
