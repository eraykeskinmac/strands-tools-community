"""HubSpot usage examples and common patterns.

This module provides example configurations and common usage patterns for the HubSpot tool.
These examples demonstrate typical CRM workflows and can be used as templates for common operations.
"""

from typing import Dict, List, Any


# Common filter examples
FILTER_EXAMPLES = {
    "recent_contacts": [
        {
            "propertyName": "createdate",
            "operator": "GTE",
            "value": "2024-01-01"
        }
    ],
    "email_domain": [
        {
            "propertyName": "email",
            "operator": "CONTAINS",
            "value": "@example.com"
        }
    ],
    "high_value_deals": [
        {
            "propertyName": "amount",
            "operator": "GTE",
            "value": "50000"
        }
    ],
    "open_deals": [
        {
            "propertyName": "dealstage",
            "operator": "NEQ",
            "value": "closedwon"
        },
        {
            "propertyName": "dealstage",
            "operator": "NEQ",
            "value": "closedlost"
        }
    ],
    "specific_lifecycle_stage": [
        {
            "propertyName": "lifecyclestage",
            "operator": "EQ",
            "value": "lead"
        }
    ]
}


# Common property sets for different object types
PROPERTY_SETS = {
    "contacts": {
        "basic": ["firstname", "lastname", "email", "phone"],
        "detailed": [
            "firstname", "lastname", "email", "phone", "company", 
            "jobtitle", "lifecyclestage", "createdate", "lastmodifieddate"
        ],
        "sales": [
            "firstname", "lastname", "email", "phone", "company",
            "hs_lead_status", "hubspot_owner_id", "closedate"
        ]
    },
    "companies": {
        "basic": ["name", "domain", "city", "state", "country"],
        "detailed": [
            "name", "domain", "industry", "numberofemployees",
            "annualrevenue", "city", "state", "country", "createdate"
        ]
    },
    "deals": {
        "basic": ["dealname", "amount", "dealstage", "closedate"],
        "detailed": [
            "dealname", "amount", "dealstage", "pipeline",
            "closedate", "hubspot_owner_id", "createdate", "hs_forecast_probability"
        ]
    }
}


# Common association type IDs
ASSOCIATION_TYPES = {
    "contact_to_company": 1,
    "company_to_contact": 2,
    "deal_to_contact": 3,
    "contact_to_deal": 4,
    "deal_to_company": 5,
    "company_to_deal": 6,
    "contact_to_ticket": 15,
    "ticket_to_contact": 16,
    "deal_to_line_item": 19,
    "line_item_to_deal": 20
}


def create_contact_example() -> Dict[str, Any]:
    """Example: Create a new contact with company association.

    Returns:
        Example parameters for hubspot() function
    """
    return {
        "action": "create",
        "object_type": "contacts",
        "properties": {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "company": "Acme Corp",
            "jobtitle": "VP of Sales"
        }
    }


def search_qualified_leads_example() -> Dict[str, Any]:
    """Example: Search for qualified leads created in the last 30 days.

    Returns:
        Example parameters for hubspot() function
    """
    return {
        "action": "search",
        "object_type": "contacts",
        "filters": [
            {
                "propertyName": "lifecyclestage",
                "operator": "EQ",
                "value": "marketingqualifiedlead"
            },
            {
                "propertyName": "createdate",
                "operator": "GTE",
                "value": "2024-01-01"  # Replace with dynamic date
            }
        ],
        "property_names": PROPERTY_SETS["contacts"]["sales"],
        "limit": 50
    }


def create_deal_with_associations_example() -> Dict[str, Any]:
    """Example: Create a deal and associate it with contact and company.

    Returns:
        Example parameters for hubspot() function
    """
    return {
        "action": "create",
        "object_type": "deals",
        "properties": {
            "dealname": "Acme Corp - Q4 Deal",
            "amount": "50000",
            "dealstage": "qualifiedtobuy",
            "closedate": "2024-12-31"
        },
        "associations": [
            {
                "to": {"id": "12345"},  # Contact ID
                "types": [{
                    "associationCategory": "HUBSPOT_DEFINED",
                    "associationTypeId": ASSOCIATION_TYPES["deal_to_contact"]
                }]
            },
            {
                "to": {"id": "67890"},  # Company ID
                "types": [{
                    "associationCategory": "HUBSPOT_DEFINED",
                    "associationTypeId": ASSOCIATION_TYPES["deal_to_company"]
                }]
            }
        ]
    }


def update_deal_stage_example() -> Dict[str, Any]:
    """Example: Update a deal's stage and amount.

    Returns:
        Example parameters for hubspot() function
    """
    return {
        "action": "update",
        "object_type": "deals",
        "object_id": "12345",
        "properties": {
            "dealstage": "closedwon",
            "amount": "75000",
            "closedate": "2024-10-15"
        }
    }


def search_companies_by_industry_example() -> Dict[str, Any]:
    """Example: Search for companies in a specific industry.

    Returns:
        Example parameters for hubspot() function
    """
    return {
        "action": "search",
        "object_type": "companies",
        "filters": [
            {
                "propertyName": "industry",
                "operator": "EQ",
                "value": "TECHNOLOGY"
            }
        ],
        "property_names": PROPERTY_SETS["companies"]["detailed"],
        "limit": 100
    }


# Common HubSpot API operators
OPERATORS = {
    "EQ": "Equals",
    "NEQ": "Not equals",
    "LT": "Less than",
    "LTE": "Less than or equal to",
    "GT": "Greater than",
    "GTE": "Greater than or equal to",
    "CONTAINS": "Contains (substring match)",
    "NOT_CONTAINS": "Does not contain",
    "STARTS_WITH": "Starts with",
    "ENDS_WITH": "Ends with",
    "IN": "In list",
    "NOT_IN": "Not in list",
    "HAS_PROPERTY": "Has property (not null)",
    "NOT_HAS_PROPERTY": "Does not have property (is null)"
}


# Common deal stages (standard HubSpot pipeline)
DEAL_STAGES = {
    "appointmentscheduled": "Appointment Scheduled",
    "qualifiedtobuy": "Qualified to Buy",
    "presentationscheduled": "Presentation Scheduled",
    "decisionmakerboughtin": "Decision Maker Bought-In",
    "contractsent": "Contract Sent",
    "closedwon": "Closed Won",
    "closedlost": "Closed Lost"
}


# Common lifecycle stages
LIFECYCLE_STAGES = {
    "subscriber": "Subscriber",
    "lead": "Lead",
    "marketingqualifiedlead": "Marketing Qualified Lead",
    "salesqualifiedlead": "Sales Qualified Lead",
    "opportunity": "Opportunity",
    "customer": "Customer",
    "evangelist": "Evangelist",
    "other": "Other"
}

