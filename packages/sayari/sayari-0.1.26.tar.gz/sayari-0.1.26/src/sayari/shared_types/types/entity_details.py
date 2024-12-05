# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from .embedded_entity import EmbeddedEntity
import typing
from .entity_registration_date import EntityRegistrationDate
from .entity_translated_label import EntityTranslatedLabel
from .entity_hs_code import EntityHsCode
from .shipment_arrival import ShipmentArrival
from .shipment_departure import ShipmentDeparture
from .company_type import CompanyType
from .status import Status
from .entity_risk import EntityRisk
import pydantic
from ...generated_types.types.attribute_details import AttributeDetails
from .possibly_same_as import PossiblySameAs
from .referenced_by import ReferencedBy
from ...core.pydantic_utilities import IS_PYDANTIC_V2
from ...core.pydantic_utilities import update_forward_refs


class EntityDetails(EmbeddedEntity):
    """
    Additional fields providing more details about an entity
    """

    registration_date: typing.Optional[EntityRegistrationDate] = None
    translated_label: typing.Optional[EntityTranslatedLabel] = None
    hs_code: typing.Optional[EntityHsCode] = None
    shipment_arrival: typing.Optional[ShipmentArrival] = None
    shipment_departure: typing.Optional[ShipmentDeparture] = None
    company_type: typing.Optional[CompanyType] = None
    latest_status: typing.Optional[Status] = None
    risk: EntityRisk = pydantic.Field()
    """
    [Risk factors](/sayari-library/ontology/risk-factors) associated with the entity.
    """

    attributes: typing.Optional[AttributeDetails] = pydantic.Field(default=None)
    """
    Detailed information about the entity's [attributes](/sayari-library/ontology/attributes).
    """

    relationships: typing.Optional["EntityRelationships"] = pydantic.Field(default=None)
    """
    Detailed information about the entity's [relationships](/sayari-library/ontology/relationships).
    """

    possibly_same_as: typing.Optional[PossiblySameAs] = None
    referenced_by: typing.Optional[ReferencedBy] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


from .entity_relationships import EntityRelationships  # noqa: E402
from .relationship_data import RelationshipData  # noqa: E402

update_forward_refs(EntityRelationships, EntityDetails=EntityDetails)
update_forward_refs(RelationshipData, EntityDetails=EntityDetails)
update_forward_refs(EntityDetails)
