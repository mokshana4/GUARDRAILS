from langchain.agents import middleware as agent_middleware
from langchain.agents.middleware import (
    PIIMiddleware,
    HumanInTheLoopMiddleware,
)

ContentFilterMiddleware = getattr(agent_middleware, "ContentFilterMiddleware", None)
SafetyGuardrailMiddleware = getattr(agent_middleware, "SafetyGuardrailMiddleware", None)


def build_middleware_stack():
    middleware_stack = [
        *(
            [ContentFilterMiddleware(banned_keywords=["hack", "exploit", "malware"])]
            if ContentFilterMiddleware is not None
            else []
        ),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email_tool": True,
                "search_tool": False,
            }
        ),
        PIIMiddleware("email", strategy="redact", apply_to_output=True),
        *(
            [SafetyGuardrailMiddleware()]
            if SafetyGuardrailMiddleware is not None
            else []
        ),
    ]
    return middleware_stack
