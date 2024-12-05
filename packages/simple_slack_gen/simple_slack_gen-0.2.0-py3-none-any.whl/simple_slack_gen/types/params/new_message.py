import typing
import typing_extensions
import pydantic


class NewMessage(typing_extensions.TypedDict):
    """
    NewMessage
    """

    as_user: typing_extensions.NotRequired[str]
    """
    Pass true to post the message as the authed user, instead of as a bot. Defaults to false. See [authorship](#authorship) below.
    """

    attachments: typing_extensions.NotRequired[str]
    """
    A JSON-based array of structured attachments, presented as a URL-encoded string.
    """

    blocks: typing_extensions.NotRequired[str]
    """
    A JSON-based array of structured blocks, presented as a URL-encoded string.
    """

    channel: typing_extensions.Required[str]
    """
    Channel, private group, or IM channel to send message to. Can be an encoded ID, or a name. See [below](#channels) for more details.
    """

    icon_emoji: typing_extensions.NotRequired[str]
    """
    Emoji to use as the icon for this message. Overrides `icon_url`. Must be used in conjunction with `as_user` set to `false`, otherwise ignored. See [authorship](#authorship) below.
    """

    icon_url: typing_extensions.NotRequired[str]
    """
    URL to an image to use as the icon for this message. Must be used in conjunction with `as_user` set to false, otherwise ignored. See [authorship](#authorship) below.
    """

    link_names: typing_extensions.NotRequired[bool]
    """
    Find and link channel names and usernames.
    """

    mrkdwn: typing_extensions.NotRequired[bool]
    """
    Disable Slack markup parsing by setting to `false`. Enabled by default.
    """

    parse: typing_extensions.NotRequired[str]
    """
    Change how messages are treated. Defaults to `none`. See [below](#formatting).
    """

    reply_broadcast: typing_extensions.NotRequired[bool]
    """
    Used in conjunction with `thread_ts` and indicates whether reply should be made visible to everyone in the channel or conversation. Defaults to `false`.
    """

    text: typing_extensions.Required[str]
    """
    How this field works and whether it is required depends on other fields you use in your API call. [See below](#text_usage) for more detail.
    """

    thread_ts: typing_extensions.NotRequired[str]
    """
    Provide another message's `ts` value to make this message a reply. Avoid using a reply's `ts` value; use its parent instead.
    """

    unfurl_links: typing_extensions.NotRequired[bool]
    """
    Pass true to enable unfurling of primarily text-based content.
    """

    unfurl_media: typing_extensions.NotRequired[bool]
    """
    Pass false to disable unfurling of media content.
    """

    username: typing_extensions.NotRequired[str]
    """
    Set your bot's user name. Must be used in conjunction with `as_user` set to false, otherwise ignored. See [authorship](#authorship) below.
    """


class _SerializerNewMessage(pydantic.BaseModel):
    """
    Serializer for NewMessage handling case conversions
    and file omissions as dictated by the API
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
