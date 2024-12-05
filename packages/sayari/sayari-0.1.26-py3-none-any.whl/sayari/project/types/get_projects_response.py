# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .project_with_members import ProjectWithMembers
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class GetProjectsResponse(UniversalBaseModel):
    """
    Examples
    --------
    from sayari.project import (
        GetProjectsResponse,
        ProjectCounts,
        ProjectWithMembers,
        RoleMember,
    )

    GetProjectsResponse(
        prev="MjAyMy0xMC0yNSAxNDo0NDowNi4zMjIxMTcrMDB8VjAzTU5Z",
        next="MjAyMy0wOS0xNSAxODoyNDozOC45ODEwMjMrMDB8OFlWQjZZ",
        limit=8,
        data=[
            ProjectWithMembers(
                id="V03MNY",
                label="Project 1",
                archived=False,
                created="2023-10-25 14:44:06.322117+00",
                updated="2023-10-25 14:44:06.322117+00",
                counts=ProjectCounts(),
                members=[
                    RoleMember(
                        type="user",
                        id="auth0|7a8f3e2b91d476c5b2e04a87",
                        role="admin",
                        created="2023-10-25T14:44:06.322117+00:00",
                        updated="2023-10-25T14:44:06.322117+00:00",
                    )
                ],
            ),
            ProjectWithMembers(
                id="eYDDmY",
                label="Project 2",
                archived=False,
                created="2023-10-24 20:41:21.235451+00",
                updated="2023-10-24 20:41:21.235451+00",
                counts=ProjectCounts(
                    graph=1,
                    entity=2530,
                ),
                members=[
                    RoleMember(
                        type="user",
                        id="auth0|f0bc63a9e72d18ef4c5702d6",
                        role="admin",
                        created="2023-10-24T20:41:21.235451+00:00",
                        updated="2023-10-24T20:41:21.235451+00:00",
                    ),
                    RoleMember(
                        type="group",
                        id="org_VdFgkL2qNpweRZAs",
                        role="viewer",
                        created="2023-11-04T18:40:30.942863+00:00",
                        updated="2023-11-04T18:40:30.942863+00:00",
                    ),
                ],
            ),
        ],
    )
    """

    next: typing.Optional[str] = None
    prev: typing.Optional[str] = None
    first: typing.Optional[bool] = None
    last: typing.Optional[bool] = None
    limit: int
    data: typing.List[ProjectWithMembers]

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
