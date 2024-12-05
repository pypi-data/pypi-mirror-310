# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...generated_types.types.currency import Currency
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class MonetaryValue(UniversalBaseModel):
    value: float
    currency: typing.Optional[Currency] = None
    context: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
