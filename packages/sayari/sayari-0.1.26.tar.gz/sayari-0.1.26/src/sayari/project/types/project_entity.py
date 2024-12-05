# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from .trade_count import TradeCount
from .project_entity_upstream import ProjectEntityUpstream
from ...shared_types.types.core_entity import CoreEntity
from .psa_summary import PsaSummary
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ProjectEntity(UniversalBaseModel):
    id: str
    project: str
    label: str = pydantic.Field()
    """
    Entity label (display name).
    """

    created: str
    updated: str
    updated_by: str
    version: int = pydantic.Field()
    """
    Will be 0.
    """

    type: typing.Literal["entity"] = "entity"
    entity_id: str = pydantic.Field()
    """
    Entity ID.
    """

    tag_ids: typing.List[str]
    case_status: str
    custom_fields: typing.Optional[typing.Optional[typing.Any]] = pydantic.Field(default=None)
    """
    <Warning>This property is in beta and is subject to change. It is provided for early access and testing purposes only.</Warning> custom user key/value pairs (key must be prefixed with "custom\_" and value must be "string" type)
    """

    match_strength: typing.Optional[typing.Any] = None
    shipped_hs_codes: typing.List[str] = pydantic.Field()
    """
    HS codes shipped by the entity.
    """

    received_hs_codes: typing.List[str] = pydantic.Field()
    """
    HS codes received by the entity.
    """

    combined_hs_codes: typing.List[str] = pydantic.Field()
    """
    HS codes shipped or received by the entity.
    """

    trade_count_incl_mg: TradeCount = pydantic.Field()
    """
    Counts of sent and received shipments for this entity and its match group.
    """

    upstream: ProjectEntityUpstream
    summary: CoreEntity
    psa: typing.Optional[PsaSummary] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
