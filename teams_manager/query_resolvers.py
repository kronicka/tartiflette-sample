from typing import Any, Dict, List, Optional

from tartiflette import Resolver

from teams_manager.data import MEMBERS, TEAMS


@Resolver("Query.teams")
async def resolve_query_teams(
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Dict[str, Any],
        info: "ResolveInfo") -> List[Dict[str, Any]]:
    """
    Resolver for returning all teams.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :return: the list of all teams

    """
    return TEAMS


@Resolver("Query.team")
async def resolver_query_team(
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Dict[str, Any],
        info: "ResolveInfo") -> Optional[Dict[str, Any]]:
    """
    Resolver for returning a specific team with a provided `id`.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :return: the specified team

    """
    for team in TEAMS:
        if team["id"] == args["id"]:
            return team
    return None


@Resolver("Team.members")
async def resolve_team_members(
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Dict[str, Any],
        info: "ResolveInfo") -> Optional[List[Dict[str, Any]]]:
    """
    Resolver for returning the list of members in a team.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :return: the list of team members

    """
    if parent and parent["id"] in MEMBERS:
        return MEMBERS[parent["id"]]
    return None
