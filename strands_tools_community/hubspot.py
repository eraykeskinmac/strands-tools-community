"""HubSpot CRM READ-ONLY integration tool for Strands Agents.

This module provides a safe, read-only interface to HubSpot's CRM API,
allowing agents to search and retrieve CRM data without the ability to modify it.
The tool handles authentication, parameter validation, response formatting, and
provides user-friendly error messages with Rich console output.

Key Features:

1. Read-Only CRM Operations:
   • Search across ANY HubSpot object type (contacts, deals, companies, tickets, etc.)
   • Get specific objects by ID
   • List available properties for any object type
   • Get detailed property information
   • Get user/owner details
   • Support for custom object types

2. Safe Design:
   • NO CREATE, UPDATE, or DELETE operations
   • Agents can only READ data
   • Perfect for analytics, reporting, and research
   • Prevents accidental data modification

3. Rich Features:
   • Beautiful table output for search results
   • Advanced search with filters and sorting
   • Pagination support
   • Property discovery
   • Rate limiting awareness

4. Safety Features:
   • Parameter validation with helpful error messages
   • Proper exception handling
   • Detailed logging for debugging
   • Rich console output for better UX

Usage Example:
```python
from strands import Agent
from strands_tools_community import hubspot

agent = Agent(tools=[hubspot])

# Search contacts
result = agent("search for contacts with email containing '@example.com'")

# Get company details
result = agent("get company with id 12345")

# List contact properties
result = agent("show me all available contact properties")

# Get user details
result = agent("get details for user/owner ID 123")
```

See the hubspot function docstring for more details on parameters and usage.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from strands import tool

logger = logging.getLogger(__name__)


def create_console() -> Console:
    """Create a Rich console instance."""
    return Console()


def load_config() -> Dict[str, Any]:
    """Load optional configuration from JSON file.

    Returns:
        Configuration dictionary or empty dict if file doesn't exist
    """
    config_paths = [
        "strands_tools_config.json",
        os.path.expanduser("~/.strands_tools_config.json"),
    ]

    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")

    return {}


class HubSpotClient:
    """Read-only client for HubSpot API operations"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.config = load_config().get("hubspot", {})

    def search_objects(
        self,
        object_type: str,
        filters: Optional[List[Dict]] = None,
        properties: Optional[List[str]] = None,
        limit: int = 10,
        sorts: Optional[List[Dict]] = None,
    ) -> Dict:
        """Search for CRM objects with filters"""
        search_body = {"limit": limit}

        if filters:
            search_body["filterGroups"] = [{"filters": filters}]

        if properties:
            search_body["properties"] = properties

        if sorts:
            search_body["sorts"] = sorts

        response = requests.post(
            f"{self.base_url}/crm/v3/objects/{object_type}/search",
            headers=self.headers,
            json=search_body,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    def get_object(self, object_type: str, object_id: str, properties: Optional[List[str]] = None) -> Dict:
        """Get a specific CRM object by ID"""
        params = {}
        if properties:
            params["properties"] = ",".join(properties)

        response = requests.get(
            f"{self.base_url}/crm/v3/objects/{object_type}/{object_id}",
            headers=self.headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    def list_properties(self, object_type: str) -> Dict:
        """List all properties for an object type"""
        response = requests.get(
            f"{self.base_url}/crm/v3/properties/{object_type}",
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    def get_property(self, object_type: str, property_name: str) -> Dict:
        """Get details of a specific property"""
        response = requests.get(
            f"{self.base_url}/crm/v3/properties/{object_type}/{property_name}",
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    def get_user_details(self, user_id: Optional[str] = None) -> Dict:
        """Get HubSpot user/owner details"""
        if user_id:
            url = f"{self.base_url}/crm/v3/owners/{user_id}"
        else:
            url = f"{self.base_url}/crm/v3/owners"

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()


def format_search_results(results: Dict, console: Console) -> str:
    """Format search results as a Rich table"""
    if not results.get("results"):
        return "No results found"

    table = Table(title="Search Results", show_header=True, header_style="bold magenta")

    # Get all unique property keys from results
    all_properties = set()
    for result in results["results"]:
        if "properties" in result:
            all_properties.update(result["properties"].keys())

    # Add ID column
    table.add_column("ID", style="cyan")

    # Add property columns (limit to first 5 for readability)
    property_columns = list(all_properties)[:5]
    for prop in property_columns:
        table.add_column(prop, style="white", overflow="fold")

    # Add rows
    for result in results["results"][:10]:  # Limit to 10 rows for console display
        row = [result.get("id", "N/A")]
        properties = result.get("properties", {})
        for prop in property_columns:
            value = properties.get(prop, "")
            # Truncate long values
            row.append(str(value)[:50] + "..." if len(str(value)) > 50 else str(value))
        table.add_row(*row)

    # Render table to string
    with console.capture() as capture:
        console.print(table)

    return capture.get()


@tool
def hubspot(
    action: str,
    object_type: str,
    properties: Optional[Dict[str, Any]] = None,
    filters: Optional[List[Dict]] = None,
    object_id: Optional[str] = None,
    limit: Optional[int] = None,
    property_names: Optional[List[str]] = None,
    user_id: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute READ-ONLY HubSpot CRM operations with comprehensive error handling.

    This tool provides a safe, read-only interface to HubSpot's CRM API. Agents can search
    and retrieve CRM data but CANNOT create, update, or delete records. Perfect for analytics,
    reporting, research, and data exploration without risk of modifying production data.

    How It Works:
    ------------
    1. The tool validates the HubSpot API key from environment variables
    2. Based on the action, it prepares the appropriate READ-ONLY API request
    3. It executes the operation against HubSpot's CRM API
    4. Responses are processed and formatted with proper error handling
    5. Results are displayed with Rich console formatting

    Supported READ-ONLY Actions:
    ---------------------------
    1. "search" - Search for CRM objects with filters
       • Supports any object type (contacts, deals, companies, tickets, etc.)
       • Advanced filtering by property values
       • Sorting and pagination
       • Example: Search for contacts with email containing "@example.com"

    2. "get" - Get a specific CRM object by ID
       • Retrieve full details of any object
       • Specify which properties to return
       • Example: Get contact ID 12345

    3. "list_properties" - List all available properties for an object type
       • Discover what fields are available
       • Useful for understanding data structure
       • Example: List all contact properties

    4. "get_property" - Get detailed information about a specific property
       • Property metadata, type, options
       • Example: Get details of "email" property

    5. "get_user_details" - Get HubSpot user/owner information
       • User profile and permissions
       • Owner assignment information
       • Example: Get user ID 123 details

    Args:
        action: Type of READ-ONLY operation ("search", "get", "list_properties", "get_property", "get_user_details")
        object_type: HubSpot object type (contacts, companies, deals, tickets, etc.)
        properties: (Optional) For search: list of properties to return
        filters: (Optional) For search: list of filter objects with propertyName, operator, value
        object_id: (Optional) For get: the ID of the object to retrieve
        limit: (Optional) For search: maximum number of results (default from env or 10)
        property_names: (Optional) For get_property: list of property names to get details for
        user_id: (Optional) For get_user_details: specific user ID (omit to list all)
        api_key: (Optional) HubSpot API key (will use HUBSPOT_API_KEY env var if not provided)

    Returns:
        Dict containing status and response content:
        {
            "status": "success|error",
            "content": [{"text": "Response message"}]
        }

    Examples:
        Search contacts:
        ```
        hubspot(
            action="search",
            object_type="contacts",
            filters=[{
                "propertyName": "email",
                "operator": "CONTAINS_TOKEN",
                "value": "@example.com"
            }],
            limit=10
        )
        ```

        Get specific deal:
        ```
        hubspot(
            action="get",
            object_type="deals",
            object_id="12345",
            properties=["dealname", "amount", "closedate"]
        )
        ```

        List contact properties:
        ```
        hubspot(
            action="list_properties",
            object_type="contacts"
        )
        ```

        Get user details:
        ```
        hubspot(
            action="get_user_details",
            user_id="123"
        )
        ```

    Environment Variables:
        HUBSPOT_API_KEY: Your HubSpot private app access token (required)
        HUBSPOT_DEFAULT_LIMIT: Default search result limit (optional, defaults to 10)

    Safety Note:
        This tool is READ-ONLY by design. It cannot create, update, or delete any HubSpot data.
        This prevents agents from accidentally modifying production CRM records while still
        allowing full read access for analytics, reporting, and research purposes.
    """
    console = create_console()

    # Display operation details
    operation_details = f"[cyan]Action:[/cyan] {action}\n"
    operation_details += f"[cyan]Object Type:[/cyan] {object_type}\n"

    console.print(Panel(operation_details, title="🏢 HubSpot CRM Operation", expand=False))

    # Check for API key
    if not api_key:
        api_key = os.environ.get("HUBSPOT_API_KEY")

    if not api_key:
        return {
            "status": "error",
            "content": [
                {
                    "text": "HubSpot API key not found. Please set the HUBSPOT_API_KEY environment variable.\n"
                    "Get your key at: https://app.hubspot.com/l/private-apps"
                }
            ],
        }

    # Get default limit from environment if not provided
    if limit is None:
        limit = int(os.environ.get("HUBSPOT_DEFAULT_LIMIT", "10"))

    try:
        client = HubSpotClient(api_key)

        if action == "search":
            console.print(f"🔍 Searching {object_type}...", style="yellow")

            result = client.search_objects(
                object_type=object_type,
                filters=filters,
                properties=properties,
                limit=limit,
            )

            table_output = format_search_results(result, console)

            return {
                "status": "success",
                "content": [
                    {"text": f"Found {len(result.get('results', []))} {object_type}"},
                    {"text": table_output},
                ],
            }

        elif action == "get":
            if not object_id:
                return {
                    "status": "error",
                    "content": [{"text": "object_id is required for get action"}],
                }

            console.print(f"📄 Getting {object_type} ID: {object_id}...", style="yellow")

            result = client.get_object(
                object_type=object_type,
                object_id=object_id,
                properties=properties,
            )

            console.print(f"✅ Retrieved {object_type}", style="green")

            return {
                "status": "success",
                "content": [
                    {"text": f"Retrieved {object_type} ID: {object_id}"},
                    {"json": result},
                ],
            }

        elif action == "list_properties":
            console.print(f"📋 Listing properties for {object_type}...", style="yellow")

            result = client.list_properties(object_type=object_type)

            console.print(f"✅ Found {len(result.get('results', []))} properties", style="green")

            return {
                "status": "success",
                "content": [
                    {"text": f"Found {len(result.get('results', []))} properties for {object_type}"},
                    {"json": result},
                ],
            }

        elif action == "get_property":
            if not property_names or len(property_names) == 0:
                return {
                    "status": "error",
                    "content": [{"text": "property_names is required for get_property action"}],
                }

            console.print(f"🔍 Getting property details for {object_type}...", style="yellow")

            properties_result = []
            for prop_name in property_names:
                result = client.get_property(object_type=object_type, property_name=prop_name)
                properties_result.append(result)

            console.print(f"✅ Retrieved {len(properties_result)} property details", style="green")

            return {
                "status": "success",
                "content": [
                    {"text": f"Retrieved details for {len(properties_result)} properties"},
                    {"json": properties_result},
                ],
            }

        elif action == "get_user_details":
            console.print(f"👤 Getting user details...", style="yellow")

            result = client.get_user_details(user_id=user_id)

            console.print(f"✅ Retrieved user details", style="green")

            return {
                "status": "success",
                "content": [
                    {"text": "Retrieved user/owner details"},
                    {"json": result},
                ],
            }

        else:
            return {
                "status": "error",
                "content": [
                    {
                        "text": f"Unknown action: {action}. Supported READ-ONLY actions: "
                        f"search, get, list_properties, get_property, get_user_details"
                    }
                ],
            }

    except requests.exceptions.HTTPError as e:
        console.print(f"❌ HubSpot API error: {e}", style="red")
        return {
            "status": "error",
            "content": [{"text": f"HubSpot API error: {str(e)}"}],
        }
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        logger.exception("HubSpot operation failed")
        return {
            "status": "error",
            "content": [{"text": f"HubSpot operation failed: {str(e)}"}],
        }
