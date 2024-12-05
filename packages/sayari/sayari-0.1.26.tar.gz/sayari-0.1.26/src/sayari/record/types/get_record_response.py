# This file was auto-generated by Fern from our API Definition.

from ...shared_types.types.record_details import RecordDetails
from .record_references import RecordReferences
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic


class GetRecordResponse(RecordDetails):
    """
    OK

    Examples
    --------
    from sayari.base_types import QualifiedCount
    from sayari.record import GetRecordResponse, RecordReferences

    GetRecordResponse(
        id="74cf0fc2a62f9c8f4e88f8a0b3ffcca4%2FF0000110%2F1682970471254",
        label="Company Record from Hong Kong Companies Registry",
        source="74cf0fc2a62f9c8f4e88f8a0b3ffcca4",
        publication_date="2023-05-01",
        acquisition_date="2023-05-01",
        references_count=1,
        record_url="/v1/record/74cf0fc2a62f9c8f4e88f8a0b3ffcca4%2FF0000110%2F1682970471254",
        source_url="https://data.gov.hk/en-data/dataset/hk-cr-crdata-list-addr",
        document_urls=[
            "/document/74cf0fc2a62f9c8f4e88f8a0b3ffcca4%2FF0000110%2F1682970471254/file/json%2FF0000110.json"
        ],
        references=RecordReferences(
            next=False,
            offset=0,
            limit=100,
            size=QualifiedCount(
                count=1,
                qualifier="eq",
            ),
            data=[
                {
                    "entity": {
                        "id": "YUc8LtKFCpAbUIBGK8nQpw",
                        "label": "Bank of China Ltd.",
                        "degree": 22179,
                        "entity_url": "/v1/entity/YUc8LtKFCpAbUIBGK8nQpw",
                        "pep": False,
                        "psa_id": "81201",
                        "psa_count": 2,
                        "sanctioned": False,
                        "closed": False,
                        "translated_label": "Bank Of China Limited",
                        "company_type": "上榜投资机构",
                        "registration_date": "Registered 2015-08-18",
                        "latest_status": {"status": "active", "date": "2019-05-20"},
                        "trade_count": {"sent": 1, "received": 1806},
                        "type": "company",
                        "identifiers": [
                            {
                                "value": "54930053HGCFWVHYZX42",
                                "type": "lei",
                                "label": "Lei",
                            },
                            {
                                "value": "0001378999",
                                "type": "usa_sec_cik_number",
                                "label": "Usa Sec Cik Number",
                            },
                            {
                                "value": "03988",
                                "type": "hkg_stock_code",
                                "label": "Hkg Stock Code",
                            },
                            {
                                "value": "92751",
                                "type": "xxx_edi_global_issuer_id",
                                "label": "Xxx Edi Global Issuer Id",
                            },
                            {
                                "value": "C320201",
                                "type": "xxx_acuris_id",
                                "label": "Xxx Acuris Id",
                            },
                        ],
                        "addresses": [
                            "No. 1 Fuxingmen Nei Dajie, Beijing 100818, China",
                            "CHN",
                            "No. 1 Fuxingmen Nei Dajie, Beijing 100818, China China",
                        ],
                        "countries": [
                            "USA",
                            "JPN",
                            "CHN",
                            "FRA",
                            "PHL",
                            "HKG",
                            "KOR",
                            "NZL",
                            "GBR",
                            "LKA",
                        ],
                        "relationship_count": {
                            "receiver_of": 1806,
                            "linked_to": 68,
                            "branch_of": 161,
                            "has_branch": 11624,
                            "beneficial_owner_of": 1,
                            "has_beneficial_owner": 3,
                            "party_to": 1,
                            "has_officer": 35,
                            "has_manager": 21,
                            "shareholder_of": 289,
                            "has_shareholder": 244,
                            "notify_party_of": 2,
                            "shipper_of": 1,
                            "has_director": 187,
                            "has_member_of_the_board": 17,
                            "has_supervisor": 34,
                            "owner_of": 1443,
                            "ships_to": 1,
                            "receives_from": 114,
                            "has_subsidiary": 103,
                            "has_legal_representative": 12,
                            "issuer_of": 6350,
                        },
                        "source_count": {
                            "eb361ba33d05a9d15b2d28aea739362a": {
                                "count": 11,
                                "label": "USA SEC Central Index Key Database",
                            },
                            "2b618f1996252fe537a6d998ae14c9b2": {
                                "count": 1,
                                "label": "UK Corporate Registry Confirmation Statements",
                            },
                            "a8c6ee1cd4dfc952105ee8c0e4836f08": {
                                "count": 151,
                                "label": "Acuris Risk Intelligence KYC6 (3rd Party Data)",
                            },
                            "1fbdc8f3abdf32274f4c7657c048294a": {
                                "count": 4,
                                "label": "China CNinfo Shanghai/Shenzhen Stock Exchange Database",
                            },
                            "e458b3b7bc1392d0723f6aa5a9fe4df1": {
                                "count": 5,
                                "label": "Japan METI gBizINFO Database",
                            },
                            "fcfa3d1c6b5f9744188fc01d0999fb76": {
                                "count": 405,
                                "label": "China SAIC",
                            },
                            "bf68c3a9a482c02f1f76342feb79af8d": {
                                "count": 1,
                                "label": "China Company Directory (Xin Gongshang Minglu)(Web Crawled Data)",
                            },
                            "a025b3503797a9cd1e1964dec6943594": {
                                "count": 3054,
                                "label": "Hong Kong Stock Exchange - Shareholding Disclosures",
                            },
                            "e0a238bcfc2f81ed9e5f345c0c7068f7": {
                                "count": 6,
                                "label": "USA Department of Labor Form 5500 Filings Database",
                            },
                            "5789a1459548517db4d61679a507be1a": {
                                "count": 1549,
                                "label": "USA SEC Securities Issuers",
                            },
                            "78586b6984ecb00e81563ae3d31c9227": {
                                "count": 1,
                                "label": "Myanmar DICA",
                            },
                            "9615bab28dddcc89548c928ab192ee7c": {
                                "count": 3,
                                "label": "Sri Lanka Imports & Exports (January 2023 - Present)",
                            },
                            "be720fea19724defd6aa652dfd5c35ed": {
                                "count": 1,
                                "label": "China Company Directory (Lanjing Zhengxin) (Web Crawled Data)",
                            },
                            "e85d865943ee6d8369307569d2ad9de0": {
                                "count": 68,
                                "label": "Acuris Risk Intelligence Adverse Media Data",
                            },
                            "b6382672c6741fe1bca28d2668c1732b": {
                                "count": 216,
                                "label": "China LHNB MOFCOM Foreign Investment Directory",
                            },
                            "48c4f3b0f7fcc732c9d075893ad004d2": {
                                "count": 10,
                                "label": "Hong Kong Stock Exchange - Listed Company Directors",
                            },
                            "db3416894cd5f0c4d2d6ecc79bdaf366": {
                                "count": 1065,
                                "label": "EDI Publicly-Listed Global Security Issuers (3rd Party Data)",
                            },
                            "faa9caafcfabcee04ef2f0b21dd9197a": {
                                "count": 155,
                                "label": "South Korea Imports & Exports (2021 - Present)",
                            },
                            "b812677c0a32a1746b3ac741c7b97ae0": {
                                "count": 71620,
                                "label": "Legal Entity Identifier (LEI) Registry (3rd Party Data)",
                            },
                            "0ff02c63234d4447c803acd7748b9afc": {
                                "count": 28,
                                "label": "China Company Directory (Shuidi)(Web Crawled Data)",
                            },
                            "de2a65257042beae5373354223cbd55b": {
                                "count": 3,
                                "label": "Japan Houjin National Tax Agency Corporation Number Publication Site",
                            },
                            "2cd05c04774a433ce4d79e61ee105d08": {
                                "count": 9,
                                "label": "Hong Kong Judiciary Judgments",
                            },
                            "ce462e9deea545cce35df38c48512a0c": {
                                "count": 1636,
                                "label": "India Imports & Exports (January 2023 - Present)",
                            },
                            "8de630b7a702183da138321ae0f1c4b0": {
                                "count": 1,
                                "label": "China Imports & Exports (2022 - Present)",
                            },
                            "ecdfb3f2ecc8c3797e77d5795a8066ef": {
                                "count": 5,
                                "label": "UK Corporate Registry",
                            },
                            "eaa2c4801c4acde073decdfae533bd0e": {
                                "count": 4,
                                "label": "France BODACC",
                            },
                            "8f50655ba1d1552ab4b89d119bd9c318": {
                                "count": 3822,
                                "label": "China Trademarks & Intellectual Property System",
                            },
                            "441b8bd29977208d312f2192675b05d9": {
                                "count": 1,
                                "label": "China Company Directory (Shunqiwang) (Web Crawled Data)",
                            },
                            "0cf0044442daf17258e27a6ddd49770f": {
                                "count": 225,
                                "label": "China NECIPS",
                            },
                            "93f0d99bcf2cc0b9f09cacc92640e54c": {
                                "count": 1,
                                "label": "Zimbabwe Imports & Exports (January 2023 - June 2023)",
                            },
                            "ddbf93a5c5d568ccdb0c2455f7ecbfc8": {
                                "count": 9,
                                "label": "USA CorpWatch SEC 10-K Exhibit 21 Database (3rd Party Data)",
                            },
                            "148946e7e3e5b2ba031bfcefa28e4d83": {
                                "count": 33,
                                "label": "China Company Directory (Aiqicha)(Web Crawled Data)",
                            },
                            "e85f886caf11a16c40512647def393e0": {
                                "count": 20,
                                "label": "New Zealand Corporate Registry",
                            },
                            "16a4cc2d0f467fa993b28587d542a25d": {
                                "count": 11,
                                "label": "USA Imports (2021 - Present)",
                            },
                            "546a239179eb5ba24177e29e308005bf": {
                                "count": 2,
                                "label": "Pakistan Imports (2011-2021)",
                            },
                            "7e0b45866bdcca61b2cfd455e5403dc2": {
                                "count": 9,
                                "label": "China Central Government Procurement Center Enterprise Database",
                            },
                            "b67ab545f3ddc960d272d11ec5952665": {
                                "count": 6,
                                "label": "France Sirene/Infogreffe Commercial Registries",
                            },
                            "74cf0fc2a62f9c8f4e88f8a0b3ffcca4": {
                                "count": 2,
                                "label": "Hong Kong Companies Registry",
                            },
                            "4ea8bac1bed868e1510ffd21842e9551": {
                                "count": 39,
                                "label": "UK Persons with Significant Control",
                            },
                            "8f21460f1cc54773b9672cb5efdb01cf": {
                                "count": 7,
                                "label": "China Ministry of Finance Government Procurement Announcements",
                            },
                        },
                        "risk": {
                            "regulatory_action": {
                                "value": True,
                                "metadata": {},
                                "level": "high",
                            },
                            "eu_high_risk_third": {
                                "value": True,
                                "metadata": {"country": ["PHL", "AFG"]},
                                "level": "relevant",
                            },
                            "reputational_risk_financial_crime": {
                                "value": True,
                                "metadata": {},
                                "level": "elevated",
                            },
                            "owner_of_sanctioned_entity": {
                                "value": 3,
                                "metadata": {},
                                "level": "high",
                            },
                            "basel_aml": {
                                "value": 8.45,
                                "metadata": {"country": ["AFG"]},
                                "level": "relevant",
                            },
                            "state_owned": {
                                "value": True,
                                "metadata": {},
                                "level": "high",
                            },
                            "owner_of_export_controls_entity": {
                                "value": 3,
                                "metadata": {},
                                "level": "high",
                            },
                            "meu_list_contractors": {
                                "value": True,
                                "metadata": {
                                    "sources": [
                                        "China Central Government Procurement Center Enterprise Database",
                                        "China Ministry of Finance Government Procurement Announcements",
                                    ]
                                },
                                "level": "high",
                            },
                            "reputational_risk_other": {
                                "value": True,
                                "metadata": {},
                                "level": "elevated",
                            },
                            "owner_of_sheffield_hallam_university_reports_forced_labor_entity": {
                                "value": 3,
                                "metadata": {},
                                "level": "high",
                            },
                            "cpi_score": {
                                "value": 16,
                                "metadata": {"country": ["AFG"]},
                                "level": "relevant",
                            },
                            "pep_adjacent": {
                                "value": True,
                                "metadata": {},
                                "level": "elevated",
                            },
                            "owner_of_forced_labor_xinjiang_entity": {
                                "value": 1,
                                "metadata": {},
                                "level": "high",
                            },
                            "law_enforcement_action": {
                                "value": True,
                                "metadata": {},
                                "level": "elevated",
                            },
                        },
                        "user_attribute_counts": {},
                        "user_attribute_count": {},
                        "user_record_count": 0,
                        "user_related_entities_count": 0,
                        "user_relationship_count": {},
                        "related_entities_count": 22179,
                        "attribute_counts": {
                            "company_type": 20,
                            "name": 25,
                            "business_purpose": 41,
                            "identifier": 33,
                            "additional_information": 29,
                            "country": 35,
                            "contact": 49,
                            "shares": 11,
                            "status": 6,
                            "address": 91,
                            "financials": 7,
                        },
                        "attribute_count": {
                            "company_type": 20,
                            "name": 25,
                            "business_purpose": 41,
                            "identifier": 33,
                            "additional_information": 29,
                            "country": 35,
                            "contact": 49,
                            "shares": 11,
                            "status": 6,
                            "address": 91,
                            "financials": 7,
                        },
                        "reference_id": "bc5bfbbd56e094337aa743fa721a48cc/firm_fffe1851b4a2a8c09c822409757dd675.html/1553604848901:20b21074f749bb4124997622fe6f3808",
                    },
                    "type": "about",
                }
            ],
        ),
    )
    """

    references: RecordReferences

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
