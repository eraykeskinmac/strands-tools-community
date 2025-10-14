# Strands Tools Community

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/strands-tools-community.svg)](https://pypi.org/project/strands-tools-community/)
[![Downloads](https://img.shields.io/pypi/dm/strands-tools-community.svg)](https://pypi.org/project/strands-tools-community/)

Community-built production-ready tools for [Strands Agents SDK](https://github.com/strands-agents/strands). Build powerful AI agents with seamless integrations for speech processing, CRM operations, and team notifications.

## 📦 Installation Options

This is a **meta-package** that bundles three Strands community tools for convenience. For new projects following Strands conventions, consider using individual packages:

```bash
# Individual packages (recommended for new projects)
pip install strands-deepgram  # Speech processing
pip install strands-hubspot   # CRM operations
pip install strands-teams     # Teams notifications

# Or install all three via meta-package
pip install strands-tools-community
```

**Individual Package Links:**

- 🎤 [strands-deepgram](https://github.com/eraykeskinmac/strands-deepgram) - Speech & audio processing
- 🏢 [strands-hubspot](https://github.com/eraykeskinmac/strands-hubspot) - HubSpot CRM operations
- 📢 [strands-teams](https://github.com/eraykeskinmac/strands-teams) - Microsoft Teams notifications

## 🚀 Features

This package provides three production-ready tools that extend the capabilities of Strands agents:

| Tool                | Description               | Key Features                                                                           |
| ------------------- | ------------------------- | -------------------------------------------------------------------------------------- |
| **Deepgram**        | Speech & Audio Processing | Speech-to-text, text-to-speech, audio intelligence, 30+ languages, speaker diarization |
| **HubSpot**         | CRM Operations            | Universal CRM access, smart search, CRUD operations, associations, batch processing    |
| **Microsoft Teams** | Notifications & Alerts    | Adaptive cards, pre-built templates, custom notifications, rich formatting             |

## 📦 Installation

```bash
# Install the community tools
pip install strands-tools-community

# Install Strands SDK with your preferred model provider
pip install 'strands-agents[anthropic]'  # For Anthropic Claude (recommended)
# OR
pip install 'strands-agents[openai]'     # For OpenAI GPT
# OR
pip install 'strands-agents[bedrock]'    # For AWS Bedrock
```

## 🎯 Quick Start

```python
from strands import Agent
from strands_tools_community import deepgram, hubspot, teams

# Create an agent with all tools
agent = Agent(tools=[deepgram, hubspot, teams])

# Use natural language to interact
agent("transcribe this audio file: recording.mp3")
agent("search for contacts in HubSpot with email containing '@example.com'")
agent("send a Teams notification about new leads")
```

## 🛠️ Tools Overview

### Deepgram - Speech & Audio Processing

Powerful speech processing capabilities powered by Deepgram's API.

**Key Features:**

- **Speech-to-Text**: Transcribe audio with 30+ language support
- **Text-to-Speech**: Generate natural-sounding speech in multiple voices
- **Audio Intelligence**: Sentiment analysis, topic detection, intent recognition
- **Speaker Diarization**: Identify and separate different speakers
- **Multi-format Support**: WAV, MP3, M4A, FLAC, and more

**Usage Example:**

```python
from strands import Agent
from strands_tools_community import deepgram

agent = Agent(tools=[deepgram])

# Transcribe audio with speaker identification
agent("transcribe audio from https://example.com/call.mp3 in Turkish with speaker diarization")

# Text-to-speech
agent("convert this text to speech and save as output.mp3: Hello world")

# Audio intelligence
agent("analyze sentiment and topics in recording.wav")
```

**Configuration:**

```bash
DEEPGRAM_API_KEY=your_deepgram_api_key  # Required
DEEPGRAM_DEFAULT_MODEL=nova-3            # Optional
DEEPGRAM_DEFAULT_LANGUAGE=en             # Optional
```

Get your API key at: [console.deepgram.com](https://console.deepgram.com/)

---

### HubSpot - CRM Operations

Complete CRM integration for managing contacts, deals, companies, and more.

**Key Features:**

- **Universal CRM Access**: Works with ANY HubSpot object type
- **Smart Search**: Advanced filtering with property-based queries
- **CRUD Operations**: Create, read, update, and delete records
- **Property Discovery**: Automatic field detection and validation
- **Association Management**: Link related objects (contacts, deals, companies)
- **Rich Console Output**: Beautiful table displays with Rich library

**Usage Example:**

```python
from strands import Agent
from strands_tools_community import hubspot

agent = Agent(tools=[hubspot])

# Search contacts
agent("find all contacts created in the last 30 days")

# Create a deal
agent("create a deal called 'Acme Corp Q4' with amount 50000")

# Update records
agent("update contact 12345 with lifecycle stage 'customer'")

# Get company details
agent("get company information for ID 67890")
```

**Configuration:**

```bash
HUBSPOT_API_KEY=your_hubspot_api_key  # Required
HUBSPOT_DEFAULT_LIMIT=100              # Optional
```

Get your API key at: [app.hubspot.com/private-apps](https://app.hubspot.com/private-apps)

---

### Microsoft Teams - Notifications & Alerts

Send rich, interactive notifications to Microsoft Teams channels.

**Key Features:**

- **Adaptive Cards**: Rich, interactive message cards
- **Pre-built Templates**: Notifications, approvals, status updates
- **Custom Cards**: Full adaptive card schema support
- **Action Buttons**: Add interactive elements to messages
- **Rich Formatting**: Markdown support, images, and media

**Usage Example:**

```python
from strands import Agent
from strands_tools_community import teams

agent = Agent(tools=[teams])

# Simple notification
agent("send a Teams message: New lead from Acme Corp")

# Use pre-built templates
agent("send an approval request to Teams for the Q4 budget")

# Status updates
agent("send a status update to Teams: website redesign is 75% complete")
```

**Configuration:**

```bash
TEAMS_WEBHOOK_URL=your_webhook_url  # Optional - can be provided per call
```

Setup webhook: Teams Channel → Connectors → Incoming Webhook

## 🌟 Real-World Examples

### Call Analytics Workflow

```python
from strands import Agent
from strands_tools_community import deepgram, hubspot, teams

agent = Agent(tools=[deepgram, hubspot, teams])

# Automated call processing
agent("""
1. Transcribe the call recording at: call_recording.mp3
2. Search HubSpot for the contact with phone number from the call
3. Create a call activity in HubSpot with the transcript
4. Send a Teams notification about the call summary
""")
```

### Lead Qualification Pipeline

```python
# Qualify and notify about new leads
agent("""
Search HubSpot for all leads with:
- Lifecycle stage: Marketing Qualified Lead
- Created in the last 7 days
- Company size: 50+ employees

Then send a summary to Teams with the count and top 5 leads
""")
```

### Daily Sales Digest

```python
# Automated daily reporting
agent("""
1. Get all deals closed today from HubSpot
2. Get all new contacts created today
3. Calculate total revenue
4. Send a formatted digest to Teams with the results
""")
```

## ⚙️ Configuration

All tools support environment variables for API keys and default settings. You can also pass configuration directly when calling tools through the agent.

### Environment Variables

```bash
# Deepgram Configuration
DEEPGRAM_API_KEY=your_deepgram_api_key
DEEPGRAM_DEFAULT_MODEL=nova-3
DEEPGRAM_DEFAULT_LANGUAGE=en

# HubSpot Configuration
HUBSPOT_API_KEY=your_hubspot_api_key
HUBSPOT_DEFAULT_LIMIT=100

# Microsoft Teams Configuration
TEAMS_WEBHOOK_URL=your_teams_webhook_url
```

### API Key Resources

- **Deepgram**: [console.deepgram.com](https://console.deepgram.com/)
- **HubSpot**: [app.hubspot.com/private-apps](https://app.hubspot.com/private-apps)
- **Teams Webhook**: Teams Channel → Connectors → Incoming Webhook

## 📚 Documentation

For more information about the Strands Agent SDK:

- [Strands Agent SDK](https://github.com/strands-agents/strands)
- [Deepgram Documentation](https://developers.deepgram.com/)
- [HubSpot API Reference](https://developers.hubspot.com/)
- [Adaptive Cards](https://adaptivecards.io/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for the [Strands Agent SDK](https://github.com/strands-agents/strands)
- Powered by [Deepgram](https://deepgram.com/), [HubSpot](https://www.hubspot.com/), and [Microsoft Teams](https://www.microsoft.com/microsoft-teams)

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/eraykeskinmac/strands-tools-community/issues)
- **Discussions**: [GitHub Discussions](https://github.com/eraykeskinmac/strands-tools-community/discussions)

---

**Made with ❤️ by the community**
