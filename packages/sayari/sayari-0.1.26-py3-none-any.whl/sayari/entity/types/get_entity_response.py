# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ...shared_types.types.entity_details import EntityDetails
from ...shared_types.types.entity_relationships import EntityRelationships
from ...shared_types.types.relationship_data import RelationshipData
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic
from ...core.pydantic_utilities import update_forward_refs


class GetEntityResponse(EntityDetails):
    """
    OK

    Examples
    --------
    from sayari.base_types import QualifiedCount
    from sayari.entity import GetEntityResponse
    from sayari.generated_types import (
        AdditionalInformationData,
        AdditionalInformationInfo,
        AdditionalInformationProperties,
        AddressData,
        AddressInfo,
        AddressProperties,
        AttributeDetails,
        BusinessPurposeData,
        BusinessPurposeInfo,
        BusinessPurposeProperties,
        CompanyTypeData,
        CompanyTypeInfo,
        CompanyTypeProperties,
        CountryData,
        CountryInfo,
        CountryProperties,
        IdentifierData,
        IdentifierInfo,
        IdentifierProperties,
        NameData,
        NameInfo,
        NameProperties,
        StatusData,
        StatusInfo,
        StatusProperties,
    )
    from sayari.shared_types import (
        EntityDetails,
        EntityRelationships,
        Identifier,
        PossiblySameAs,
        PossiblySameAsData,
        PsaEntity,
        RecordDetails,
        ReferencedBy,
        ReferencedByData,
        RelationshipData,
        RelationshipInfo,
        RiskData,
        SourceCountInfo,
        Status,
    )

    GetEntityResponse(
        id="mGq1lpuqKssNWTjIokuPeA",
        label="VICTORIA BECKHAM LIMITED",
        degree=67,
        entity_url="/v1/entity/mGq1lpuqKssNWTjIokuPeA",
        pep=False,
        psa_id="695785012897",
        psa_count=3,
        sanctioned=False,
        closed=False,
        company_type="Stock Corporation - Out of State - Stock",
        registration_date="Incorporated 2008-02-28",
        latest_status=Status(
            status="active",
            date="2023-08-29",
        ),
        trade_count={"sent": 41, "received": 0},
        type="company",
        identifiers=[
            Identifier(
                value="06517802",
                type="uk_company_number",
                label="Uk Company Number",
            ),
            Identifier(
                value="6517802",
                type="unknown",
                label="Unknown",
            ),
            Identifier(
                value="04781466",
                type="ca_corporate_id_num",
                label="Ca Corporate Id Num",
            ),
        ],
        addresses=[
            "202 HAMMERSMITH ROAD , LONDON , , UNITED KINGDOM , W6 7DN , GB",
            "Unit 33, Ransomes Dock Business Centre, 35-37 Parkgate Road, London SW11 4NP",
            "SAUNDERS BUILDING, 202 HAMMERSMITH ROAD, HAMMERSMITH, LONDON",
        ],
        countries=["GBR", "USA"],
        relationship_count={
            "linked_to": 3,
            "has_officer": 2,
            "shareholder_of": 1,
            "has_shareholder": 2,
            "has_registered_agent": 5,
            "shipper_of": 41,
            "has_director": 11,
            "owner_of": 3,
            "has_founder": 1,
            "ships_to": 1,
        },
        source_count={
            "2b618f1996252fe537a6d998ae14c9b2": SourceCountInfo(
                count=1,
                label="UK Corporate Registry Confirmation Statements",
            ),
            "2b788dbdf9194ed5a5c309386a6516b1": SourceCountInfo(
                count=28,
                label="UK HM Revenue & Customs Traders Database",
            ),
            "a447a7b622c4ead6e1caf94983dc2337": SourceCountInfo(
                count=6,
                label="USA California Secretary of State",
            ),
            "ecdfb3f2ecc8c3797e77d5795a8066ef": SourceCountInfo(
                count=35,
                label="UK Corporate Registry",
            ),
            "e5de7b52cc88ef4cd1a10e201bdf46ee": SourceCountInfo(
                count=41,
                label="Vietnam Imports & Exports (January 2023 - Present)",
            ),
            "2a4fe9a14e332c8f9ded1f8a457c2b89": SourceCountInfo(
                count=36,
                label="UK Land Commercial and Corporate Ownership Data (CCOD)",
            ),
            "4ea8bac1bed868e1510ffd21842e9551": SourceCountInfo(
                count=69,
                label="UK Persons with Significant Control",
            ),
        },
        risk={
            "basel_aml": RiskData(
                value=4.63,
                metadata={"country": ["USA"]},
                level="relevant",
            ),
            "cpi_score": RiskData(
                value=67.0,
                metadata={"country": ["USA"]},
                level="relevant",
            ),
        },
        user_attribute_count={},
        user_record_count=0,
        user_related_entities_count=0,
        user_relationship_count={},
        related_entities_count=67,
        attribute_count={
            "company_type": 2,
            "name": 2,
            "business_purpose": 4,
            "identifier": 3,
            "additional_information": 106,
            "country": 8,
            "status": 5,
            "address": 7,
        },
        reference_id="ecdfb3f2ecc8c3797e77d5795a8066ef/06517802/1540252800000:4a34442eccf1622995130b194a5d50e7",
        attributes=AttributeDetails(
            additional_information=AdditionalInformationInfo(
                limit=1,
                next="_SjfEipa7hytJ93C1IT_sg",
                size=QualifiedCount(
                    count=106,
                    qualifier="eq",
                ),
                data=[
                    AdditionalInformationData(
                        properties=AdditionalInformationProperties(
                            type="Traded Goods",
                        ),
                        record=[
                            "2b788dbdf9194ed5a5c309386a6516b1/22950249e3df0c33ce05bd54850ba9f3/1672444800000"
                        ],
                        record_count=9,
                        editable=False,
                    )
                ],
            ),
            address=AddressInfo(
                limit=1,
                next="5TPSsmsFxea24_QTyk8o1Q",
                size=QualifiedCount(
                    count=7,
                    qualifier="eq",
                ),
                data=[
                    AddressData(
                        properties=AddressProperties(
                            value="202 HAMMERSMITH ROAD UNITED KINGDOM",
                            house_number="202",
                            road="Hammersmith Road",
                            country="United Kingdom",
                            x=-0.22579,
                            y=51.49291,
                            precision_code="G3",
                            normalized="202 HAMMERSMITH KINGDOM RD UNITED",
                        ),
                        record=[
                            "9139b58de1bdb0157a1a1e54e56df6d3/4781466/1678752000000"
                        ],
                        record_count=5,
                        editable=False,
                    )
                ],
            ),
            business_purpose=BusinessPurposeInfo(
                limit=1,
                next="5fZrn5ZbUyo6d_huc6NlAA",
                size=QualifiedCount(
                    count=4,
                    qualifier="eq",
                ),
                data=[
                    BusinessPurposeData(
                        properties=BusinessPurposeProperties(
                            value="Other amusement and recreation activities n.e.c.",
                            code="9329",
                            standard="ISIC4",
                        ),
                        record=[
                            "9aef3a56aa0ea25404b498dbd8bb447f/06517802/1579014552807"
                        ],
                        record_count=18,
                        editable=False,
                    )
                ],
            ),
            company_type=CompanyTypeInfo(
                limit=1,
                next="iuJ_MCygy24sDCcVkbCATA",
                size=QualifiedCount(
                    count=2,
                    qualifier="eq",
                ),
                data=[
                    CompanyTypeData(
                        properties=CompanyTypeProperties(
                            value="Stock Corporation - Out of State - Stock",
                        ),
                        record=[
                            "9139b58de1bdb0157a1a1e54e56df6d3/4781466/1649116800000"
                        ],
                        record_count=6,
                        editable=False,
                    )
                ],
            ),
            country=CountryInfo(
                limit=1,
                next="_ZTsEnhxCbjokYYWu1kMoQ",
                size=QualifiedCount(
                    count=8,
                    qualifier="eq",
                ),
                data=[
                    CountryData(
                        properties=CountryProperties(
                            value="GBR",
                            context="address",
                        ),
                        record=[
                            "9aef3a56aa0ea25404b498dbd8bb447f/06517802/1579014552807"
                        ],
                        record_count=23,
                        editable=False,
                    )
                ],
            ),
            identifier=IdentifierInfo(
                limit=1,
                next="07v3Rsu6x-gDuukFa0jEsw",
                size=QualifiedCount(
                    count=3,
                    qualifier="eq",
                ),
                data=[
                    IdentifierData(
                        properties=IdentifierProperties(
                            value="04781466",
                            type="ca_corporate_id_num",
                        ),
                        record=[
                            "9139b58de1bdb0157a1a1e54e56df6d3/4781466/1649116800000"
                        ],
                        record_count=6,
                        editable=False,
                    )
                ],
            ),
            name=NameInfo(
                limit=1,
                next="5lxpjuZmt31xiCnbDILp0A",
                size=QualifiedCount(
                    count=2,
                    qualifier="eq",
                ),
                data=[
                    NameData(
                        properties=NameProperties(
                            value="BECKHAM VENTURES LIMITED",
                            context="alias",
                            to_date="2014-09-03",
                        ),
                        record=[
                            "2a4fe9a14e332c8f9ded1f8a457c2b89/NGL944625/1560779151522"
                        ],
                        record_count=30,
                        editable=False,
                    )
                ],
            ),
            status=StatusInfo(
                limit=1,
                next="EdC1n7V2lU0oKTokzO_YLw",
                size=QualifiedCount(
                    count=5,
                    qualifier="eq",
                ),
                data=[
                    StatusData(
                        properties=StatusProperties(
                            text="Good",
                        ),
                        record=[
                            "9139b58de1bdb0157a1a1e54e56df6d3/4781466/1649116800000"
                        ],
                        record_count=6,
                        editable=False,
                    )
                ],
            ),
        ),
        relationships=EntityRelationships(
            limit=1,
            next="fzenMMQtpFHx9Cam_2nDndg",
            size=QualifiedCount(
                count=67,
                qualifier="eq",
            ),
            data=[
                RelationshipData(
                    target=EntityDetails(
                        id="zenMMQtpFHx9Cam_2nDndg",
                        label="Victoria Beckham Holdings Limited",
                        degree=17,
                        entity_url="/v1/entity/zenMMQtpFHx9Cam_2nDndg",
                        pep=False,
                        psa_count=0,
                        sanctioned=False,
                        closed=False,
                        company_type="Private Limited Company",
                        registration_date="Incorporated 2017-11-02",
                        latest_status=Status(
                            status="active",
                        ),
                        trade_count={"sent": 0, "received": 0},
                        type="company",
                        identifiers=[
                            Identifier(
                                value="11043864",
                                type="uk_company_number",
                                label="Uk Company Number",
                            )
                        ],
                        addresses=[
                            "35-37 Parkgate Road, London, SW11 4NP",
                            "Hammersmith Road, London",
                            "202 HAMMERSMITH ROAD, LONDON, W6 7DN",
                        ],
                        countries=["GBR"],
                        relationship_count={
                            "shareholder_of": 2,
                            "has_shareholder": 5,
                            "has_registered_agent": 1,
                            "has_director": 9,
                            "linked_to": 7,
                        },
                        source_count={
                            "ecdfb3f2ecc8c3797e77d5795a8066ef": SourceCountInfo(
                                count=34,
                                label="UK Corporate Registry",
                            ),
                            "2b618f1996252fe537a6d998ae14c9b2": SourceCountInfo(
                                count=1,
                                label="UK Corporate Registry Confirmation Statements",
                            ),
                            "4ea8bac1bed868e1510ffd21842e9551": SourceCountInfo(
                                count=147,
                                label="UK Persons with Significant Control",
                            ),
                        },
                        risk={
                            "basel_aml": RiskData(
                                value=3.99,
                                metadata={"country": ["GBR"]},
                                level="relevant",
                            ),
                            "cpi_score": RiskData(
                                value=78.0,
                                metadata={"country": ["GBR"]},
                                level="relevant",
                            ),
                        },
                        user_attribute_count={},
                        user_record_count=0,
                        user_related_entities_count=0,
                        user_relationship_count={},
                        related_entities_count=17,
                        attribute_count={
                            "company_type": 1,
                            "name": 2,
                            "business_purpose": 3,
                            "identifier": 1,
                            "additional_information": 1,
                            "country": 3,
                            "status": 2,
                            "address": 3,
                        },
                        reference_id="ecdfb3f2ecc8c3797e77d5795a8066ef/11043864/1540252800000:40ec7b0310d308ebf9006148b53a2802",
                    ),
                    types={
                        "has_shareholder": [
                            RelationshipInfo(
                                editable=False,
                                record="4ea8bac1bed868e1510ffd21842e9551/56910fae410d43596d5a94fd9405023a/1711843200000",
                                attributes={},
                                acquisition_date="2024-03-31",
                            ),
                            RelationshipInfo(
                                editable=False,
                                record="4ea8bac1bed868e1510ffd21842e9551/06517802/1560176240192",
                                attributes={
                                    "position": [
                                        {
                                            "value": "Has right to appoint and remove directors"
                                        },
                                        {"value": "Owns 75-100% of shares"},
                                        {"value": "Owns 75-100% of voting rights"},
                                    ],
                                    "shares": [{"percentage": 75}],
                                },
                                acquisition_date="2019-06-10",
                            ),
                        ],
                        "linked_to": [
                            RelationshipInfo(
                                editable=False,
                                record="4ea8bac1bed868e1510ffd21842e9551/56910fae410d43596d5a94fd9405023a/1711843200000",
                                attributes={},
                                acquisition_date="2024-03-31",
                            ),
                            RelationshipInfo(
                                editable=False,
                                record="4ea8bac1bed868e1510ffd21842e9551/06517802/1560176240192",
                                attributes={
                                    "position": [
                                        {
                                            "value": "Has right to appoint and remove directors"
                                        },
                                        {"value": "Owns 75-100% of shares"},
                                        {"value": "Owns 75-100% of voting rights"},
                                    ]
                                },
                                acquisition_date="2019-06-10",
                            ),
                        ],
                    },
                    dates=["2017-11-16"],
                    first_observed="2017-11-16",
                    last_observed="2017-11-16",
                )
            ],
        ),
        possibly_same_as=PossiblySameAs(
            limit=1,
            size=QualifiedCount(
                count=3,
                qualifier="eq",
            ),
            next="eyJ0eXBlIjoic2F5YXJpIiwib2Zmc2V0IjoxfQ",
            data=[
                PossiblySameAsData(
                    entity=PsaEntity(
                        id="NGUTEUTI4YZ6R5d56vgNIw",
                        label="BECKHAM VENTURES INC.",
                        degree=3,
                        entity_url="/v1/entity/NGUTEUTI4YZ6R5d56vgNIw",
                        pep=False,
                        psa_id="695785012897",
                        psa_count=3,
                        sanctioned=False,
                        closed=False,
                        company_type="FOREIGN BUSINESS CORPORATION",
                        registration_date=" 2013-01-16",
                        latest_status=Status(
                            status="active",
                            date="2013-01-16",
                        ),
                        trade_count={"sent": 0, "received": 0},
                        type="company",
                        identifiers=[
                            Identifier(
                                value="4346762",
                                type="usa_ny_dos_id",
                                label="Usa Ny Dos Id",
                            )
                        ],
                        addresses=[
                            "99 WASHINGTON AVE., SUITE 805A, ALBANY, NY, 12201",
                            "511 WEST 25TH STREET, SUITE # 701/7TH FLOOR, NEW YORK, NEW YORK, 10001",
                            "80 STATE STREET, ALBANY, NEW YORK, 12207-2543",
                        ],
                        countries=["USA"],
                        relationship_count={
                            "has_officer": 1,
                            "has_registered_agent": 2,
                            "linked_to": 2,
                        },
                        source_count={
                            "b4d06d4b77f51fab3c77c9653aabdda4": SourceCountInfo(
                                count=8,
                                label="USA New York Corporate Registry (Active Entities)",
                            )
                        },
                        risk={
                            "basel_aml": RiskData(
                                value=4.63,
                                metadata={"country": ["USA"]},
                                level="relevant",
                            ),
                            "cpi_score": RiskData(
                                value=67.0,
                                metadata={"country": ["USA"]},
                                level="relevant",
                            ),
                        },
                        user_attribute_count={},
                        user_record_count=0,
                        user_related_entities_count=0,
                        user_relationship_count={},
                        related_entities_count=3,
                        attribute_count={
                            "company_type": 1,
                            "name": 1,
                            "identifier": 1,
                            "country": 3,
                            "status": 1,
                            "address": 3,
                        },
                        reference_id="b4d06d4b77f51fab3c77c9653aabdda4/a80e7f4c-c219-437b-9941-32d89ea5885a/1560542045043:15d813b260619393762864f22d3c5b2d",
                    ),
                    editable=False,
                    matches={},
                )
            ],
        ),
        referenced_by=ReferencedBy(
            limit=1,
            size=QualifiedCount(
                count=216,
                qualifier="eq",
            ),
            next="Vk5NfGdsb2JhbF90cmFkZV90YV92bm18ZnwyMDI0LTAxLTAzfHtENjM0QjlCMS0zOUUyLTQyNzMtOEYzNUFFODExMzBFMThEN318MTcwNDI0MDAwMDAwMA",
            data=[
                ReferencedByData(
                    record=RecordDetails(
                        id="e5de7b52cc88ef4cd1a10e201bdf46ee/{D634B9B1-39E2-4273-8F35AE81130E18D7}/1704240000000",
                        label="Trade Record from Vietnam Imports & Exports (January 2023 - Present)",
                        source="e5de7b52cc88ef4cd1a10e201bdf46ee",
                        publication_date="2024-01-03",
                        acquisition_date="2024-01-03",
                        references_count=3,
                        record_url="/record/e5de7b52cc88ef4cd1a10e201bdf46ee%2F%7BD634B9B1-39E2-4273-8F35AE81130E18D7%7D%2F1704240000000",
                    ),
                    type="mentions",
                )
            ],
        ),
    )
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


update_forward_refs(EntityDetails, GetEntityResponse=GetEntityResponse)
update_forward_refs(EntityRelationships, GetEntityResponse=GetEntityResponse)
update_forward_refs(RelationshipData, GetEntityResponse=GetEntityResponse)
