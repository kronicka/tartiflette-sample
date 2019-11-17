import asyncio
from typing import Any, AsyncGenerator, Dict, Optional
from tartiflette import Subscription
from teams_manager.data import TEAMS


@Subscription("Subscription.launchAndWaitPracticeTimer")
async def subscribe_subscription_launch_and_wait_practice_timer(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo") -> AsyncGenerator[Dict[str, Any], None]:
    """
    Subscription in charge of generating an event stream related to the team
    practice.
    :param parent: initial value filled in to the engine `subscribe` method
    :param args: computed arguments related to the subscription
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution

    :return: an asynchronous generator of the practice state of a team
    :raises Exception: if the team_id doesn't exist

    """
    team = None
    for team_data in TEAMS:
        if team_data["id"] == args["id"]:
            team = team_data

    if not team:
        raise Exception(f"The team `{args['id']}` doesn\'t exist.")

    for i in range(team["practiceTime"]):
        yield {
            "launchAndWaitPracticeTimer": {
                "remainingTime": team["practiceTime"] - i,
                "status": "PRACTICING"
            }
        }
        await asyncio.sleep(1)

    yield {
        "launchAndWaitPracticeTimer": {"remainingTime": 0, "status": "FINISHED"}
    }
