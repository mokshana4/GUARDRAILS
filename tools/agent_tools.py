from langchain_core.tools import tool


@tool
def search_tool(query: str) -> str:
    """Search for information."""
    return f"Search results: {query}"


@tool
def send_email_tool(to: str, body: str) -> str:
    """Send an email."""
    return f"Email sent to {to}"
