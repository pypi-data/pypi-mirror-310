# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
from .notification_type import NotificationType
from ...generated_types.types.risk import Risk
from ...shared_types.types.risk_value import RiskValue
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class ResourceNotificationData(UniversalBaseModel):
    saved_resource_id: str = pydantic.Field()
    """
    The ID of the saved resource
    """

    project_id: str = pydantic.Field()
    """
    The ID of the project the entity is saved to
    """

    entity_id: str = pydantic.Field()
    """
    The ID of the entity
    """

    type: NotificationType = pydantic.Field()
    """
    The type of notification, currently limited to 'risk'
    """

    field: Risk = pydantic.Field()
    """
    The field that the notification is for
    """

    value: RiskValue = pydantic.Field()
    """
    The previous value of the field
    """

    date: str = pydantic.Field()
    """
    The date the notification was created
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
