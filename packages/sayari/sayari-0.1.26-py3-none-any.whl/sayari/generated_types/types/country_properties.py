# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .country_context import CountryContext
import pydantic
from .country import Country
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class CountryProperties(UniversalBaseModel):
    context: typing.Optional[CountryContext] = pydantic.Field(default=None)
    """
    The type of affiliation
    """

    date: typing.Optional[str] = pydantic.Field(default=None)
    """
    as-of date
    """

    from_date: typing.Optional[str] = pydantic.Field(default=None)
    """
    start date
    """

    state: typing.Optional[str] = pydantic.Field(default=None)
    """
    The subnational state, province, region, etc.
    """

    to_date: typing.Optional[str] = pydantic.Field(default=None)
    """
    end date
    """

    value: Country = pydantic.Field()
    """
    The country, ideally normalized to an ISO trigram
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
