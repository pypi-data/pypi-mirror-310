# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class MethodNotAllowedResponse(UniversalBaseModel):
    """
    Resource not found or does not exist.
    """

    status: int
    message: typing.List[str]
    success: bool

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
