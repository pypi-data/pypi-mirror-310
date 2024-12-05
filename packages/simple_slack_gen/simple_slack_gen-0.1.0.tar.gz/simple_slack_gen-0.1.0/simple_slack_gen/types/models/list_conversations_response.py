import typing
import pydantic

from .channel import Channel


class ListConversationsResponse(pydantic.BaseModel):
    """
    ListConversationsResponse
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    channels: typing.List[Channel] = pydantic.Field(alias="channels")

    ok: bool = pydantic.Field(alias="ok")
