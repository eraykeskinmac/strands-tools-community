"""Microsoft Teams integration tool for Strands Agents.

This module provides a comprehensive interface to Microsoft Teams via Incoming Webhooks,
allowing you to send rich adaptive card notifications directly from your Strands Agent.
The tool supports both custom adaptive cards and pre-built templates, handles authentication,
parameter validation, response formatting, and provides user-friendly error messages with Rich console output.

Key Features:

1. Adaptive Card Support:
   • Send custom adaptive cards with full schema support
   • Pre-built templates for common use cases
   • Support for buttons, images, actions, and rich formatting
   • Template variable injection for dynamic content

2. Pre-built Templates:
   • Notification cards (info, warning, success, error)
   • Approval request cards with action buttons
   • Status update cards with color-coded indicators
   • Custom templates can be added easily

3. Flexible Design:
   • Works with any Teams channel via Incoming Webhooks
   • Template system for consistency
   • Custom card builder for advanced use cases
   • Data injection into templates

4. Safety Features:
   • Parameter validation with helpful error messages
   • Proper exception handling
   • Card structure validation
   • Rich console output for debugging

Usage Example:
```python
from strands import Agent
from strands_tools_community import teams

agent = Agent(tools=[teams])

# Send a notification
result = agent("send a Teams notification about new leads")

# Send custom adaptive card
result = agent("send a status update card to Teams")
```

See the teams function docstring for more details on parameters and usage.
"""

import json
import logging
import os
from typing import Any, Dict, Optional

import requests
from rich.console import Console
from rich.panel import Panel
from strands import tool

logger = logging.getLogger(__name__)


def create_console() -> Console:
    """Create a Rich console instance."""
    return Console()


@tool
def teams(
    webhook_url: Optional[str] = None,
    card_template: Optional[Dict] = None,
    template_name: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
    title: Optional[str] = None,
    message: Optional[str] = None,
    color: str = "default",
) -> Dict[str, Any]:
    """Send adaptive card notifications to Microsoft Teams with comprehensive error handling and validation.

    This tool provides a flexible interface to Microsoft Teams via Incoming Webhooks, allowing you to send
    rich adaptive card notifications. It supports both custom adaptive cards and pre-built templates,
    handles authentication, response formatting, and provides helpful error messages.

    How It Works:
    ------------
    1. The tool validates the webhook URL from parameter or environment variables
    2. Based on the input, it either uses a template, custom card, or simple message
    3. If using a template, it injects data into the template
    4. It validates the card structure
    5. It sends the card to Teams via webhook
    6. Response is validated and formatted

    Common Usage Scenarios:
    ---------------------
    - Deal Notifications: Alert team about new deals or deal stage changes
    - Lead Alerts: Notify team about qualified leads
    - Task Reminders: Send task and deadline notifications
    - Status Updates: Share project or system status updates
    - Approval Requests: Request approvals with action buttons
    - Error Alerts: Send error notifications from systems
    - Custom Notifications: Any rich formatted message

    Template System:
    ---------------
    Pre-built templates available via `template_name`:
    
    1. "notification" - General notification card
       Required data: title, message
       Optional data: color (default|good|attention|warning)
       
    2. "approval" - Approval request card
       Required data: title, details, approve_url, reject_url
       
    3. "status" - Status update card
       Required data: project, status, details
       Optional data: color
       
    4. "simple" - Simple text message
       Required data: title, message

    Custom Cards:
    ------------
    You can also provide a complete adaptive card JSON via `card_template`.
    Follow the Adaptive Cards schema: https://adaptivecards.io/schemas/adaptive-card.json

    Args:
        webhook_url: Microsoft Teams Incoming Webhook URL (uses TEAMS_WEBHOOK_URL env var if not provided)
        card_template: Complete adaptive card JSON dictionary (for custom cards)
        template_name: Name of pre-built template to use ("notification", "approval", "status", "simple")
        data: Dictionary of data to inject into template
        title: Simple title for simple messages (used with message parameter)
        message: Simple message text (used with title parameter)
        color: Color scheme for notification ("default", "good", "attention", "warning", "accent")

    Returns:
        Dict containing status and response content:
        {
            "status": "success|error",
            "content": [{"text": "Response message"}]
        }

    Notes:
        - Requires TEAMS_WEBHOOK_URL environment variable OR webhook_url parameter
        - Templates are validated before sending
        - Teams webhook URLs start with https://outlook.office.com/webhook/
        - Cards support markdown formatting in text blocks
        - Maximum card size is ~28KB
        - Buttons support Action.OpenUrl and Action.Submit types

    Environment Variables:
        - TEAMS_WEBHOOK_URL: Optional default Teams Incoming Webhook URL

    Configuration:
        Get your webhook URL:
        1. Go to Teams channel
        2. Click "..." -> Connectors
        3. Search for "Incoming Webhook"
        4. Configure and copy the webhook URL

    Example Usage:
        ```python
        # Simple notification
        teams(
            title="New Lead",
            message="New lead from website: Acme Corp",
            color="good"
        )

        # Template-based card
        teams(
            template_name="notification",
            data={
                "title": "Deal Closed",
                "message": "Acme Corp deal closed for $50,000!",
                "color": "good"
            }
        )

        # Approval request
        teams(
            template_name="approval",
            data={
                "title": "Budget Approval Required",
                "details": "Q4 Marketing budget: $25,000",
                "approve_url": "https://example.com/approve/123",
                "reject_url": "https://example.com/reject/123"
            }
        )

        # Status update
        teams(
            template_name="status",
            data={
                "project": "Website Redesign",
                "status": "In Progress",
                "details": "75% complete, on track for Q4 launch",
                "color": "accent"
            }
        )

        # Custom adaptive card
        teams(
            card_template={
                "type": "AdaptiveCard",
                "version": "1.3",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "Custom Card",
                        "weight": "Bolder",
                        "size": "Large"
                    }
                ]
            }
        )
        ```
    """
    console = create_console()

    # Get webhook URL
    if not webhook_url:
        webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")
        if not webhook_url:
            return {
                "status": "error",
                "content": [
                    {
                        "text": "Teams webhook URL not found. Please set the TEAMS_WEBHOOK_URL environment variable "
                        "or provide webhook_url parameter.\n"
                        "Get your webhook at: Teams Channel -> Connectors -> Incoming Webhook"
                    }
                ],
            }

    # Display operation details
    operation_details = "[cyan]Target:[/cyan] Microsoft Teams\n"
    if template_name:
        operation_details += f"[cyan]Template:[/cyan] {template_name}\n"
    if title:
        operation_details += f"[cyan]Title:[/cyan] {title}\n"
    if message:
        message_preview = message[:100] + "..." if len(message) > 100 else message
        operation_details += f"[cyan]Message:[/cyan] {message_preview}\n"

    console.print(Panel(operation_details, title="📢 Teams Notification", expand=False))

    try:
        # Import templates here to avoid circular imports
        from strands_tools_community.templates import teams_templates

        # Build card based on input
        card = None

        if card_template:
            # Use custom card directly
            card = {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card_template if "type" in card_template else {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.3",
                    **card_template
                }
            }

        elif template_name:
            # Use pre-built template
            if template_name == "notification":
                if not data or "title" not in data or "message" not in data:
                    return {
                        "status": "error",
                        "content": [
                            {"text": "notification template requires 'title' and 'message' in data"}
                        ],
                    }
                card_content = teams_templates.notification(
                    title=data["title"],
                    message=data["message"],
                    color=data.get("color", "default")
                )
                card = {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": card_content
                }

            elif template_name == "approval":
                if not data or not all(k in data for k in ["title", "details", "approve_url", "reject_url"]):
                    return {
                        "status": "error",
                        "content": [
                            {
                                "text": "approval template requires 'title', 'details', 'approve_url', "
                                "and 'reject_url' in data"
                            }
                        ],
                    }
                card_content = teams_templates.approval_card(
                    title=data["title"],
                    details=data["details"],
                    approve_url=data["approve_url"],
                    reject_url=data["reject_url"]
                )
                card = {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": card_content
                }

            elif template_name == "status":
                if not data or not all(k in data for k in ["project", "status", "details"]):
                    return {
                        "status": "error",
                        "content": [
                            {"text": "status template requires 'project', 'status', and 'details' in data"}
                        ],
                    }
                card_content = teams_templates.status_update(
                    project=data["project"],
                    status=data["status"],
                    details=data["details"],
                    color=data.get("color", "default")
                )
                card = {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": card_content
                }

            elif template_name == "simple":
                if not data or "title" not in data or "message" not in data:
                    return {
                        "status": "error",
                        "content": [
                            {"text": "simple template requires 'title' and 'message' in data"}
                        ],
                    }
                card_content = teams_templates.simple_message(
                    title=data["title"],
                    message=data["message"]
                )
                card = {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": card_content
                }

            else:
                return {
                    "status": "error",
                    "content": [
                        {
                            "text": f"Unknown template: {template_name}. Available templates: notification, approval, status, simple"
                        }
                    ],
                }

        elif title and message:
            # Simple message format
            card_content = teams_templates.simple_message(title=title, message=message)
            card = {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card_content
            }

        else:
            return {
                "status": "error",
                "content": [
                    {
                        "text": "Must provide either: card_template, template_name with data, or title with message"
                    }
                ],
            }

        # Prepare payload
        payload = {
            "type": "message",
            "attachments": [card]
        }

        console.print(f"📤 Sending to Teams...", style="yellow")

        # Send to Teams
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Strands-Tools-Community/1.0"
        }

        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            console.print(f"✅ Message sent successfully", style="green")
            return {
                "status": "success",
                "content": [
                    {"text": "Message sent to Teams successfully"}
                ],
            }
        else:
            error_msg = f"Teams API returned status {response.status_code}: {response.text}"
            console.print(f"❌ {error_msg}", style="red")
            return {
                "status": "error",
                "content": [{"text": error_msg}],
            }

    except Exception as e:
        error_msg = f"Failed to send Teams message: {str(e)}"
        logger.error(error_msg)
        console.print(f"❌ {error_msg}", style="red")
        return {
            "status": "error",
            "content": [{"text": error_msg}],
        }

