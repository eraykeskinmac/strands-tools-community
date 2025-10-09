"""Community tools for Strands Agent SDK.

This package provides production-ready tools for common integrations:
- Deepgram: Speech-to-text, text-to-speech, and audio intelligence
- HubSpot: CRM operations for contacts, deals, companies, and more
- Microsoft Teams: Adaptive card notifications and messaging

Example usage:
    ```python
    from strands import Agent
    from strands_tools_community import deepgram, hubspot, teams

    agent = Agent(tools=[deepgram, hubspot, teams])
    ```
"""

from .deepgram import deepgram
from .hubspot import hubspot
from .teams import teams

__version__ = "0.1.0"
__all__ = ["deepgram", "hubspot", "teams"]

