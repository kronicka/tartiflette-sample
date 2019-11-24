from typing import Any, Callable, Dict, Optional, Union
from tartiflette import Directive


@Directive("rateLimiting")
class RateLimiting:
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
