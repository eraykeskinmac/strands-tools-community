"""Meta-package wrapper for Strands community tools.

IMPORTANT: For new projects, consider using individual packages:
- pip install strands-deepgram
- pip install strands-hubspot  
- pip install strands-teams

This meta-package provides all three tools for convenience, but individual
packages offer better dependency management and are the recommended approach
for new projects following Strands community conventions.

Example usage:
    ```python
    from strands import Agent
    from strands_tools_community import deepgram, hubspot, teams

    agent = Agent(tools=[deepgram, hubspot, teams])
    ```

Or use individual packages:
    ```python
    from strands import Agent
    from strands_deepgram import deepgram
    from strands_hubspot import hubspot
    from strands_teams import teams

    agent = Agent(tools=[deepgram, hubspot, teams])
    ```
"""

# Try importing from individual packages first, fall back to bundled versions
try:
    from strands_deepgram import deepgram
except ImportError:
    from .deepgram import deepgram

try:
    from strands_hubspot import hubspot
except ImportError:
    from .hubspot import hubspot

try:
    from strands_teams import teams
except ImportError:
    from .teams import teams

__version__ = "0.2.0"
__all__ = ["deepgram", "hubspot", "teams"]

