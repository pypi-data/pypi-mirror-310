import typing
import pydantic

from .message import Message


class MessageResponse(pydantic.BaseModel):
    """
    Schema for successful response of chat.postMessage method
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    channel: str = pydantic.Field(alias="channel")

    message: Message = pydantic.Field(alias="message")

    ok: bool = pydantic.Field(alias="ok")

    response_metadata: typing.Optional[typing.Dict[str, typing.Any]] = pydantic.Field(
        alias="response_metadata", default=None
    )

    ts: str = pydantic.Field(alias="ts")

    warning: typing.Optional[str] = pydantic.Field(alias="warning", default=None)
