# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...generated_types.types.risk import Risk
import pydantic
from .upstream_tiers import UpstreamTiers
from ...generated_types.types.country import Country
import typing_extensions
from ...core.serialization import FieldMetadata
from ...generated_types.types.company_status import CompanyStatus
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ProjectEntitiesFilter(UniversalBaseModel):
    risk: typing.Optional[typing.List[Risk]] = pydantic.Field(default=None)
    """
    Filter by [risk factor](/sayari-library/ontology/risk-factors) ID.
    """

    upstream_risk: typing.Optional[typing.List[Risk]] = pydantic.Field(default=None)
    """
    Filter by upstream (supply chain) [risk factor](/sayari-library/ontology/risk-factors) ID.
    """

    upstream_risk_tiers: typing.Optional[typing.List[UpstreamTiers]] = pydantic.Field(default=None)
    """
    Filter by upstream (supply chain) tiers that has one or more risks
    """

    country: typing.Optional[typing.List[Country]] = pydantic.Field(default=None)
    """
    Filter by [country](/sayari-library/ontology/enumerated-types#country).
    """

    upstream_country: typing.Optional[typing.List[Country]] = pydantic.Field(default=None)
    """
    Filter by upstream (supply chain) [country](/sayari-library/ontology/enumerated-types#country).
    """

    upstream_country_tiers: typing.Optional[typing.List[UpstreamTiers]] = pydantic.Field(default=None)
    """
    Filter by upstream (supply chain) tiers that has one or more countries
    """

    business_purpose: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    Filter by HS code, HS code description, or business description.
    """

    label_fuzzy: typing_extensions.Annotated[typing.Optional[typing.List[str]], FieldMetadata(alias="label.fuzzy")] = (
        pydantic.Field(default=None)
    )
    """
    Filter by entity label with fuzzy matching.
    """

    city_fuzzy: typing_extensions.Annotated[typing.Optional[typing.List[str]], FieldMetadata(alias="city.fuzzy")] = (
        pydantic.Field(default=None)
    )
    """
    Filter by entity city with fuzzy matching.
    """

    state_fuzzy: typing_extensions.Annotated[typing.Optional[typing.List[str]], FieldMetadata(alias="state.fuzzy")] = (
        pydantic.Field(default=None)
    )
    """
    Filter by entity address state with fuzzy matching.
    """

    identifier_fuzzy: typing_extensions.Annotated[
        typing.Optional[typing.List[str]], FieldMetadata(alias="identifier.fuzzy")
    ] = pydantic.Field(default=None)
    """
    Filter by entity identifier attributes with fuzzy matching.
    """

    source_exact: typing_extensions.Annotated[
        typing.Optional[typing.List[str]], FieldMetadata(alias="source.exact")
    ] = pydantic.Field(default=None)
    """
    Filter by entity source ID.
    """

    status_exact: typing_extensions.Annotated[
        typing.Optional[typing.List[CompanyStatus]], FieldMetadata(alias="status.exact")
    ] = pydantic.Field(default=None)
    """
    Filter by entity [company status](/sayari-library/ontology/enumerated-types#company-status).
    """

    bounds: typing.Optional[str] = pydantic.Field(default=None)
    """
    Filter by a geographical bounding box. The value is a pipe-delimited set of four values representing the top, left, bottom, and right sides of the bounding box, in that order. The pipes should be URL-encoded as `%7C`. The top coordinate must greater than the bottom coordinate, and the left coordinate must be less than the right coordinate. A sample is `55.680357237879136|-71.53607290158526|41.10876347746233|-40.963927098414736`
    """

    custom_field_name: typing_extensions.Annotated[
        typing.Optional[typing.List[str]], FieldMetadata(alias="custom_{field name}")
    ] = pydantic.Field(default=None)
    """
    <Warning>This property is in beta and is subject to change. It is provided for early access and testing purposes only.</Warning> custom user key/value pairs (key must be prefixed with "custom\_" and value must be "string" type)
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
