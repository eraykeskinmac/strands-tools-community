"""Pre-built Microsoft Teams Adaptive Card templates.

This module provides ready-to-use adaptive card templates for common Microsoft Teams notification scenarios.
All templates follow the Adaptive Cards 1.3 schema and are optimized for Teams rendering.

Templates:
- notification: General-purpose notification with color coding
- approval_card: Approval request with action buttons
- status_update: Project/system status updates
- simple_message: Basic text message card
"""

from typing import Dict, Any


def notification(title: str, message: str, color: str = "default") -> Dict[str, Any]:
    """Create a notification adaptive card.

    Args:
        title: Card title/heading
        message: Main message content (supports markdown)
        color: Color scheme ("default", "good", "attention", "warning", "accent")

    Returns:
        Adaptive card JSON dictionary
    """
    # Map color names to Teams container styles
    color_mapping = {
        "default": "default",
        "good": "good",
        "attention": "attention",
        "warning": "warning",
        "accent": "accent",
    }

    container_style = color_mapping.get(color.lower(), "default")

    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "Container",
                "style": container_style,
                "items": [
                    {
                        "type": "TextBlock",
                        "text": title,
                        "weight": "Bolder",
                        "size": "Large",
                        "wrap": True
                    }
                ]
            },
            {
                "type": "TextBlock",
                "text": message,
                "wrap": True,
                "spacing": "Medium"
            }
        ],
        "msteams": {
            "width": "Full"
        }
    }


def approval_card(title: str, details: str, approve_url: str, reject_url: str) -> Dict[str, Any]:
    """Create an approval request adaptive card with action buttons.

    Args:
        title: Approval request title
        details: Detailed description of what needs approval
        approve_url: URL to navigate to when approve is clicked
        reject_url: URL to navigate to when reject is clicked

    Returns:
        Adaptive card JSON dictionary
    """
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "Container",
                "style": "attention",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "⚠️ Approval Required",
                        "weight": "Bolder",
                        "size": "Medium",
                        "color": "Attention"
                    }
                ]
            },
            {
                "type": "TextBlock",
                "text": title,
                "weight": "Bolder",
                "size": "Large",
                "wrap": True,
                "spacing": "Medium"
            },
            {
                "type": "TextBlock",
                "text": details,
                "wrap": True,
                "spacing": "Small"
            }
        ],
        "actions": [
            {
                "type": "Action.OpenUrl",
                "title": "✅ Approve",
                "url": approve_url,
                "style": "positive"
            },
            {
                "type": "Action.OpenUrl",
                "title": "❌ Reject",
                "url": reject_url,
                "style": "destructive"
            }
        ],
        "msteams": {
            "width": "Full"
        }
    }


def status_update(project: str, status: str, details: str, color: str = "default") -> Dict[str, Any]:
    """Create a status update adaptive card.

    Args:
        project: Project or system name
        status: Current status (e.g., "In Progress", "Completed", "On Hold")
        details: Detailed status information
        color: Color scheme based on status

    Returns:
        Adaptive card JSON dictionary
    """
    # Map color names to Teams container styles
    color_mapping = {
        "default": "default",
        "good": "good",
        "attention": "attention",
        "warning": "warning",
        "accent": "accent",
    }

    container_style = color_mapping.get(color.lower(), "accent")

    # Status emoji mapping
    status_emojis = {
        "completed": "✅",
        "in progress": "🔄",
        "on hold": "⏸️",
        "blocked": "🚫",
        "cancelled": "❌",
    }

    status_emoji = status_emojis.get(status.lower(), "📊")

    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "TextBlock",
                "text": f"{status_emoji} Status Update",
                "weight": "Bolder",
                "size": "Large",
                "wrap": True
            },
            {
                "type": "FactSet",
                "facts": [
                    {
                        "title": "Project:",
                        "value": project
                    },
                    {
                        "title": "Status:",
                        "value": status
                    }
                ],
                "spacing": "Medium"
            },
            {
                "type": "Container",
                "style": container_style,
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "Details",
                        "weight": "Bolder",
                        "spacing": "Small"
                    },
                    {
                        "type": "TextBlock",
                        "text": details,
                        "wrap": True,
                        "spacing": "Small"
                    }
                ],
                "spacing": "Medium"
            }
        ],
        "msteams": {
            "width": "Full"
        }
    }


def simple_message(title: str, message: str) -> Dict[str, Any]:
    """Create a simple text message adaptive card.

    Args:
        title: Message title
        message: Message content (supports markdown)

    Returns:
        Adaptive card JSON dictionary
    """
    return {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "TextBlock",
                "text": title,
                "weight": "Bolder",
                "size": "Medium",
                "wrap": True
            },
            {
                "type": "TextBlock",
                "text": message,
                "wrap": True,
                "spacing": "Medium"
            }
        ],
        "msteams": {
            "width": "Full"
        }
    }

