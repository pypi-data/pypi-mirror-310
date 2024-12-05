import typing
import pydantic


class Message(pydantic.BaseModel):
    """
    Message
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    app_id: typing.Optional[str] = pydantic.Field(alias="app_id", default=None)

    attachments: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = (
        pydantic.Field(alias="attachments", default=None)
    )

    blocks: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = pydantic.Field(
        alias="blocks", default=None
    )

    bot_id: typing.Optional[str] = pydantic.Field(alias="bot_id", default=None)

    bot_profile: typing.Optional[typing.Dict[str, typing.Any]] = pydantic.Field(
        alias="bot_profile", default=None
    )

    team: typing.Optional[str] = pydantic.Field(alias="team", default=None)

    text: str = pydantic.Field(alias="text")

    ts: str = pydantic.Field(alias="ts")

    type_field: str = pydantic.Field(alias="type")

    user: typing.Optional[str] = pydantic.Field(alias="user", default=None)
