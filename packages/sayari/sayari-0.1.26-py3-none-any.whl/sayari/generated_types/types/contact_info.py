# This file was auto-generated by Fern from our API Definition.

from ...base_types.types.paginated_response import PaginatedResponse
import typing
from .contact_data import ContactData
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ContactInfo(PaginatedResponse):
    """
    Contact information for an entity
    """

    data: typing.List[ContactData]
    next: typing.Optional[typing.Optional[typing.Any]] = None
    offset: typing.Optional[int] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
