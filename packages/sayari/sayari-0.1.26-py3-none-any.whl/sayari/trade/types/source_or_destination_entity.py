# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from ...generated_types.types.risk import Risk
from ...generated_types.types.business_purpose_properties import BusinessPurposeProperties
from ...generated_types.types.country import Country
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class SourceOrDestinationEntity(UniversalBaseModel):
    id: str = pydantic.Field()
    """
    Unique identifier of the entity
    """

    type: str
    names: typing.List[str]
    risks: typing.Dict[Risk, typing.Optional[typing.Any]] = pydantic.Field()
    """
    [Risks](/sayari-library/ontology/risk-factors)
    """

    business_purpose: typing.List[BusinessPurposeProperties] = pydantic.Field()
    """
    [Business Purpose](/sayari-library/ontology/attributes#business-purpose)
    """

    address: typing.List[typing.Optional[typing.Any]] = pydantic.Field()
    """
    [Address](/sayari-library/ontology/attributes#address)
    """

    countries: typing.List[Country] = pydantic.Field()
    """
    [Country](/sayari-library/ontology/attributes#country)
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
