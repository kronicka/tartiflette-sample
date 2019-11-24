from typing import Any, Callable, Dict, Optional, Union
from tartiflette import Directive
import time


@Directive("rateLimiting")
class RateLimitingDirective:
    """
    Directive to rate limit the access to some fields.
    """
    def __init__(self) -> None:
        self._rate_limit_rules = {}

    def _set_new_rate_limit_rule(
            self, name: str, max_attempts: int, duration: int, attempts_made: int = 0
    ) -> None:
        """
        Registers a new rate limit entry.

        :param name: identifier of the rate limit
        :param max_attempts: maximum allowed attempts during the duration
        :param duration: interval before resetting the rate limiting
        :param attempts_made: number of attempts already made

        """
        self._rate_limit_rules[name] = {
            "max_attempts": max_attempts,
            "duration": duration,
            "start_time": int(time.time()),
            "attempts_made": attempts_made
        }

    def _rate_limit_check_and_bump(
            self,
            name: str,
            max_attempts: int,
            duration: int
    ) -> bool:
        """
        Increments the number of attempts and determines whether or not
        the rate limit has been reached.

        :param name: identifier of the rate limit
        :param max_attempts: maximum allowed attempts during the duration
        :param duration: interval before resetting the rate limiting
        :return: whether or not the rate limit has been reached

        """
        rule = self._rate_limit_rules[name]

        if int(time.time()) > (rule["start_time"] + rule["duration"]):
            self._set_new_rate_limit_rule(
                name,
                max_attempts,
                duration,
                attempts_made=1
            )
            return True

        self._rate_limit_rules[name]["attempts_made"] += 1

        return rule["attempts_made"] <= rule["max_attempts"]

    async def on_field_execution(
            self,
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Dict[str, Any],
            info: "ResolveInfo",
    ) -> Any:
        """
        Checks that the user did not reach the rate limit before proceeding
        with the execution and resolution of the field.

        :param directive_args: computed arguments related to the directive
        :param next_resolver: next resolver to call
        :param parent: initial value filled in to the engine `execute` or
        `subscribe` method or field parent value
        :param args: computed arguments related to the field
        :param ctx: context filled in at engine init
        :param info: info related tot the execution and field resolution

        :return: result of the field resolution
        """
        if directive_args["name"] not in self._rate_limit_rules:
            self._set_new_rate_limit_rule(
                directive_args["name"],
                directive_args["maxAttempts"],
                directive_args["duration"],
            )

        is_valid = self._rate_limit_check_and_bump(
            directive_args["name"],
            directive_args["maxAttempts"],
            directive_args["duration"],
        )

        if not is_valid:
            raise Exception("You reached the limit of the rate limiting.")

        return await next_resolver(parent, args, ctx, info)

    async def on_argument_execution(
            self,
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_node: "ArgumentNode",
            value: Any,
            ctx: Optional[Any],
    ) -> Any:
        """ Placeholder """
        return await next_directive(parent_node, argument_node, value, ctx)

    async def on_post_input_coersion(
            self,
            directive_ags: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["VariableDefinitionNode", "InputValueDefinitionNode"],
            value: Any,
            ctx: Optional[Any],
    ) -> Any:
        return await next_directive(parent_node, value, ctx)
