import pydantic


class Channel(pydantic.BaseModel):
    """
    Channel
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )

    created: int = pydantic.Field(alias="created")

    id: str = pydantic.Field(alias="id")

    is_channel: bool = pydantic.Field(alias="is_channel")

    is_group: bool = pydantic.Field(alias="is_group")

    is_private: bool = pydantic.Field(alias="is_private")

    name: str = pydantic.Field(alias="name")
