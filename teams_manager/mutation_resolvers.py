from typing import Any, Dict, Optional
from tartiflette import Resolver
from teams_manager.data import TEAMS


@Resolver("Mutation.updateTeam")
async def resolve_mutation_update_team(
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Dict[str, Any],
        info: "ResolveInfo") -> Dict[str, Any]:
    """
    Resolver for performing a mutation on a team.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the mutation
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :return: the mutated team

    """
    team_id = args["input"]["id"]
    name = args["input"].get("name")
    motto = args["input"].get("motto")
    
    if not (name or motto):
        raise Exception(
            "Provide at least one value for either name or "
            "motto."
        )
    
    for index, team in enumerate(TEAMS):
        if team["id"] == team_id:
            if name:
                TEAMS[index]["name"] = name
            if motto:
                TEAMS[index]["motto"] = motto
            return TEAMS[index]
    
    raise Exception(f"The team `{team_id}` doesn\'t exist.")
