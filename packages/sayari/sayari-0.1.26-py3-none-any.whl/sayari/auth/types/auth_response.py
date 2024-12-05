# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class AuthResponse(UniversalBaseModel):
    access_token: str = pydantic.Field()
    """
    The bearer token you will pass in to subsequent API calls to authenticate.
    """

    expires_in: int = pydantic.Field()
    """
    Tells you how long (in seconds) until your bearer token expires.
    """

    token_type: str = pydantic.Field()
    """
    Will always be "Bearer"
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
