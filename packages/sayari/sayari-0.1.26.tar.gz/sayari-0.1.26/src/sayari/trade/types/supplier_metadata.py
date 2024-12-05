# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing_extensions
import typing
from ...core.serialization import FieldMetadata
from .hs_code import HsCode
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class SupplierMetadata(UniversalBaseModel):
    latest_shipment_date: typing_extensions.Annotated[
        typing.Optional[str], FieldMetadata(alias="latestShipmentDate")
    ] = None
    shipments: int
    hs_codes: typing_extensions.Annotated[typing.List[HsCode], FieldMetadata(alias="hsCodes")]

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
