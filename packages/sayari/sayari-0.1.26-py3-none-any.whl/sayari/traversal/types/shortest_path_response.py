# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ...core.pydantic_utilities import UniversalBaseModel
from ...shared_types.types.entity_details import EntityDetails
from ...shared_types.types.entity_relationships import EntityRelationships
from ...shared_types.types.relationship_data import RelationshipData
import typing
from .shortest_path_data import ShortestPathData
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from ...core.pydantic_utilities import update_forward_refs


class ShortestPathResponse(UniversalBaseModel):
    """
    OK

    Examples
    --------
    from sayari.shared_types import (
        EntityDetails,
        Identifier,
        RelationshipInfo,
        RiskData,
        SourceCountInfo,
    )
    from sayari.traversal import (
        ShortestPathData,
        ShortestPathResponse,
        TraversalPath,
        TraversalRelationshipData,
    )

    ShortestPathResponse(
        entities=["H1y25N5ymnFyZ-q9Lpwm_g", "1nOeH5G2EhmRVtmeVqO2Lw"],
        data=[
            ShortestPathData(
                source="H1y25N5ymnFyZ-q9Lpwm_g",
                target=EntityDetails(
                    id="1nOeH5G2EhmRVtmeVqO2Lw",
                    label="Mr Thomas Bangalter",
                    degree=1,
                    entity_url="/v1/entity/1nOeH5G2EhmRVtmeVqO2Lw",
                    pep=False,
                    psa_count=0,
                    sanctioned=False,
                    closed=False,
                    trade_count={"sent": 0, "received": 0},
                    type="person",
                    identifiers=[
                        Identifier(
                            value="053673450003",
                            type="uk_person_number",
                            label="Uk Person Number",
                        ),
                        Identifier(
                            value="053673450002",
                            type="uk_person_number",
                            label="Uk Person Number",
                        ),
                    ],
                    addresses=[
                        "5TH FLOOR 104 OXFORD STREET, W1D 1LP, LONDON, UNITED KINGDOM",
                        "Oxford Street, London, W1D 1LP",
                        "8 AVENUE RACHEL, 75018, FRANCE",
                    ],
                    date_of_birth="1975-01",
                    countries=["FRA", "GBR"],
                    relationship_count={
                        "registered_agent_of": 1,
                        "shareholder_of": 1,
                        "director_of": 1,
                    },
                    source_count={
                        "4ea8bac1bed868e1510ffd21842e9551": SourceCountInfo(
                            count=28,
                            label="UK Persons with Significant Control",
                        ),
                        "ecdfb3f2ecc8c3797e77d5795a8066ef": SourceCountInfo(
                            count=17,
                            label="UK Corporate Registry",
                        ),
                    },
                    risk={
                        "basel_aml": RiskData(
                            value=3.67,
                            metadata={"country": ["GBR"]},
                            level="relevant",
                        ),
                        "cpi_score": RiskData(
                            value=71.0,
                            metadata={"country": ["FRA"]},
                            level="relevant",
                        ),
                    },
                    user_attribute_count={},
                    user_record_count=0,
                    user_related_entities_count=0,
                    user_relationship_count={},
                    related_entities_count=1,
                    attribute_count={
                        "name": 1,
                        "identifier": 2,
                        "additional_information": 2,
                        "country": 4,
                        "date_of_birth": 1,
                        "address": 5,
                    },
                    reference_id="ecdfb3f2ecc8c3797e77d5795a8066ef/03389614/1540252800000:9030330caf25555c42c0bc0d84ea4aa1",
                ),
                path=[
                    TraversalPath(
                        field="has_lawyer",
                        entity=EntityDetails(
                            id="xthsA_jQuKn3GW8-9ILQqg",
                            label="LAWRENCE E. APOLZON",
                            degree=179,
                            entity_url="/v1/entity/xthsA_jQuKn3GW8-9ILQqg",
                            pep=False,
                            psa_count=0,
                            sanctioned=False,
                            closed=False,
                            trade_count={"sent": 0, "received": 0},
                            type="person",
                            identifiers=[],
                            addresses=[
                                "Fross Zelnick Lehrman & Zissu, P.C., 866 United Nations Plaza, New York NY 10017",
                                "FROSS ZELNICK LEHRMAN & ZISSU, P.C., 4 TIMES SQUARE, 17TH FLOOR, NEW YORK, NY 10036",
                                "Fross Zelnick Lehrman & Zissu, P.C., 151 West 42nd Street, 17th Floor, New York, NY 10036",
                            ],
                            countries=["USA"],
                            relationship_count={"lawyer_of": 179},
                            source_count={
                                "ac1fa195f9cd4ccf657bca3c6db0bb19": SourceCountInfo(
                                    count=199,
                                    label="USA Patents and Trademark Office Trademark Applications",
                                )
                            },
                            risk={},
                            user_attribute_count={},
                            user_record_count=0,
                            user_related_entities_count=0,
                            user_relationship_count={},
                            related_entities_count=179,
                            attribute_count={"country": 1, "address": 5, "name": 1},
                            reference_id="ac1fa195f9cd4ccf657bca3c6db0bb19/76232419/1717632000000:6d0f0edbd065319df4be58c3bc7909f5",
                        ),
                        relationships={
                            "has_lawyer": TraversalRelationshipData(
                                values=[
                                    RelationshipInfo(
                                        record="ac1fa195f9cd4ccf657bca3c6db0bb19/76082348/1717632000000",
                                        acquisition_date="2024-06-06",
                                        attributes={},
                                    )
                                ],
                            )
                        },
                    )
                ],
            )
        ],
    )
    """

    entities: typing.List[str]
    data: typing.List[ShortestPathData]

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


update_forward_refs(EntityDetails, ShortestPathResponse=ShortestPathResponse)
update_forward_refs(EntityRelationships, ShortestPathResponse=ShortestPathResponse)
update_forward_refs(RelationshipData, ShortestPathResponse=ShortestPathResponse)
