"""Deepgram integration tool for Strands Agents.

This module provides a comprehensive interface to Deepgram's speech and audio processing services,
allowing you to transcribe audio, generate speech, and analyze audio content directly from your Strands Agent.
The tool handles authentication, parameter validation, response formatting, and provides user-friendly error messages with Rich console output.

Key Features:

1. Speech-to-Text (STT):
   • Support for multiple audio formats (WAV, MP3, M4A, FLAC, etc.)
   • Local file and URL-based transcription
   • 30+ language support
   • Speaker diarization
   • Smart formatting and punctuation
   • Confidence scoring and timing information

2. Text-to-Speech (TTS):
   • Natural-sounding voice synthesis
   • Multiple voice options (Aura voices)
   • Various audio formats
   • Customizable speech parameters

3. Audio Intelligence:
   • Sentiment analysis
   • Topic detection
   • Intent recognition
   • Language detection

4. Safety Features:
   • Parameter validation with helpful error messages
   • Proper exception handling
   • Detailed logging for debugging
   • Rich console output for better UX

Usage Example:
```python
from strands import Agent
from strands_tools_community import deepgram

agent = Agent(tools=[deepgram])

# Transcribe audio
result = agent("transcribe this audio: path/to/audio.wav with Turkish language")

# Text-to-speech
result = agent("convert this text to speech: Hello world")

# Audio analysis
result = agent("analyze sentiment in audio: path/to/call.mp3")
```

See the deepgram function docstring for more details on parameters and usage.
"""

import logging
import os
import subprocess
import tempfile
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import requests
from deepgram import DeepgramClient
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from strands import tool

logger = logging.getLogger(__name__)


def create_console() -> Console:
    """Create a Rich console instance."""
    return Console()


def is_url(source: str) -> bool:
    """Check if source is a URL.

    Args:
        source: Source string to check

    Returns:
        True if source is a URL, False otherwise
    """
    try:
        result = urlparse(source)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def download_audio_from_url(url: str, console: Optional[Console] = None) -> str:
    """Download audio file from URL to temporary location.

    Args:
        url: HTTP/HTTPS URL to audio file
        console: Optional Rich console for progress display

    Returns:
        Path to downloaded temporary file

    Raises:
        Exception: If download fails
    """
    if console is None:
        console = create_console()

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description=f"Downloading audio from {url}...", total=None)

            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()

            # Create temporary file with appropriate extension
            parsed_url = urlparse(url)
            extension = os.path.splitext(parsed_url.path)[1] or ".wav"

            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_path = temp_file.name

            console.print(f"✅ Downloaded audio to temporary location", style="green")
            return temp_path

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise Exception(f"Audio file not found at URL: {url}")
        else:
            raise Exception(f"HTTP error {e.response.status_code}: {str(e)}")

    except Exception as e:
        raise Exception(f"Failed to download audio from URL: {str(e)}")


@tool
def deepgram(
    action: str,
    audio_source: Optional[str] = None,
    text: Optional[str] = None,
    language: str = "en",
    model: str = "nova-3",
    options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Execute Deepgram audio processing operations with comprehensive error handling and validation.

    This tool provides a universal interface to Deepgram's API, allowing you to perform
    speech-to-text transcription, text-to-speech synthesis, and audio intelligence analysis.
    It handles authentication via DEEPGRAM_API_KEY, parameter validation, response formatting,
    and provides helpful error messages with Rich console output.

    How It Works:
    ------------
    1. The tool validates the Deepgram API key from environment variables
    2. Based on the action, it prepares the appropriate API request
    3. For audio operations, it downloads or reads the audio file
    4. It executes the operation against Deepgram's API
    5. Responses are processed and formatted with proper error handling
    6. Results are displayed with Rich console formatting

    Common Usage Scenarios:
    ---------------------
    - Call Transcription: Transcribe customer calls for analysis
    - Meeting Minutes: Convert meetings to text with speaker identification
    - Voice Commands: Process voice input for applications
    - Speech Synthesis: Generate audio from text for IVR systems
    - Sentiment Analysis: Analyze tone and sentiment in conversations
    - Topic Detection: Identify key topics discussed in audio

    Actions:
    -------
    1. "transcribe" - Speech-to-text transcription
       • Multi-format audio support (WAV, MP3, FLAC, etc.)
       • 30+ language support
       • Speaker diarization (identify different speakers)
       • Smart formatting and punctuation
       • Word-level timestamps

    2. "text_to_speech" - Text-to-speech synthesis
       • Natural-sounding voices (Aura series)
       • Multiple audio formats
       • Customizable speech parameters
       • Voice selection

    3. "analyze" - Audio intelligence
       • Sentiment analysis
       • Topic detection
       • Intent recognition
       • Language detection

    Args:
        action: Type of operation ("transcribe", "text_to_speech", or "analyze")
        audio_source: Path to audio file or URL (required for transcribe/analyze)
        text: Text to convert to speech (required for text_to_speech)
        language: Language code (e.g., "en", "es", "tr", "fr")
        model: Deepgram model to use (default: "nova-3" for STT, "aura-asteria-en" for TTS)
        options: Optional dictionary of additional parameters:
            For transcribe:
                - diarize: Enable speaker diarization (default: True)
                - smart_format: Apply smart formatting (default: True)
                - punctuate: Add punctuation (default: True)
                - utterances: Include utterance info (default: True)
                - detect_language: Auto-detect language (default: False)
                - topics: Detect topics (default: False)
                - sentiment: Analyze sentiment (default: False)
                - intents: Detect intents (default: False)
            For text_to_speech:
                - voice: Voice name (default: "aura-asteria-en")
                - encoding: Audio encoding format (default: "mp3")
                - sample_rate: Sample rate in Hz (default: 24000)
                - output_path: Path to save audio file (default: "deepgram_output.mp3")
                - play_audio: Auto-play audio after generation (default: True)
            For analyze:
                - Same as transcribe, but enables sentiment/topics/intents by default

    Returns:
        Dict containing status and response content:
        {
            "status": "success|error",
            "content": [{"text": "Response message"}]
        }

        For successful transcriptions:
        {
            "status": "success",
            "content": [{
                "text": str,  # Full transcript
                "json": {
                    "transcript": str,
                    "confidence": float,
                    "language": str,
                    "duration": float,
                    "word_count": int,
                    "speakers": dict,  # If diarization enabled
                    "words": list,  # Word-level timing
                    "sentiment": dict,  # If sentiment enabled
                    "topics": list,  # If topics enabled
                }
            }]
        }

    Notes:
        - Requires DEEPGRAM_API_KEY environment variable to be set
        - Supports both local files and URLs for audio sources
        - Temporary files are automatically cleaned up after processing
        - All responses use Rich console formatting for better readability
        - Audio files are auto-detected for format (no need to specify encoding)

    Environment Variables:
        - DEEPGRAM_API_KEY: Required Deepgram API key
        - DEEPGRAM_DEFAULT_MODEL: Optional default model (overrides "nova-3")
        - DEEPGRAM_DEFAULT_LANGUAGE: Optional default language (overrides "en")

    Example Usage:
        ```python
        # Transcribe with speaker diarization
        deepgram(
            action="transcribe",
            audio_source="recording.mp3",
            language="en",
            options={"diarize": True, "smart_format": True}
        )

        # Text-to-speech
        deepgram(
            action="text_to_speech",
            text="Hello, this is a test.",
            options={"voice": "aura-asteria-en"}
        )

        # Analyze sentiment and topics
        deepgram(
            action="analyze",
            audio_source="https://example.com/call.mp3",
            language="en",
            options={"sentiment": True, "topics": True}
        )
        ```
    """
    console = create_console()

    # Display operation details
    operation_details = f"[cyan]Action:[/cyan] {action}\n"
    if audio_source:
        operation_details += f"[cyan]Audio Source:[/cyan] {audio_source}\n"
    if text:
        operation_details += f"[cyan]Text:[/cyan] {text[:100]}{'...' if len(text) > 100 else ''}\n"
    operation_details += f"[cyan]Language:[/cyan] {language}\n"
    operation_details += f"[cyan]Model:[/cyan] {model}\n"

    console.print(Panel(operation_details, title="🎤 Deepgram Operation", expand=False))

    # Check for API key
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "content": [
                {
                    "text": "Deepgram API key not found. Please set the DEEPGRAM_API_KEY environment variable.\n"
                    "Get your key at: https://console.deepgram.com/"
                }
            ],
        }

    # Use environment defaults if available
    model = os.environ.get("DEEPGRAM_DEFAULT_MODEL", model)
    language = os.environ.get("DEEPGRAM_DEFAULT_LANGUAGE", language)

    # Set default options
    if options is None:
        options = {}

    temp_file_path = None

    try:
        # Initialize Deepgram client (SDK 5.0.0+ requires keyword argument)
        deepgram_client = DeepgramClient(api_key=api_key)

        # Handle different actions
        if action == "transcribe":
            # Validate audio source
            if not audio_source:
                return {
                    "status": "error",
                    "content": [
                        {"text": "audio_source parameter is required for transcribe action"}
                    ],
                }

            # Handle URL vs local file
            if is_url(audio_source):
                logger.info(f"Downloading audio from URL: {audio_source}")
                audio_file_path = download_audio_from_url(audio_source, console)
                temp_file_path = audio_file_path
            else:
                audio_file_path = audio_source
                if not os.path.exists(audio_file_path):
                    return {
                        "status": "error",
                        "content": [{"text": f"Audio file not found: {audio_file_path}"}],
                    }

            console.print(f"🎵 Starting transcription...", style="yellow")

            # Configure transcription options
            transcribe_options = {
                "model": model,
                "language": language,
                "smart_format": options.get("smart_format", True),
                "punctuate": options.get("punctuate", True),
                "utterances": options.get("utterances", True),
                "diarize": options.get("diarize", True),
                "detect_language": options.get("detect_language", False),
                "topics": options.get("topics", False),
                "sentiment": options.get("sentiment", False),
                "intents": options.get("intents", False),
            }

            # Read and transcribe audio file
            with open(audio_file_path, "rb") as audio_file:
                buffer_data = audio_file.read()

            # Deepgram REST API - Use direct HTTP request (like TTS)
            # Docs: https://developers.deepgram.com/reference/pre-recorded
            url = "https://api.deepgram.com/v1/listen"
            
            # Query parameters
            params = {
                "model": model,
                "language": language,
            }
            # Add optional features
            if transcribe_options.get("diarize"):
                params["diarize"] = "true"
            if transcribe_options.get("smart_format"):
                params["smart_format"] = "true"
            if transcribe_options.get("punctuate"):
                params["punctuate"] = "true"
            if transcribe_options.get("utterances"):
                params["utterances"] = "true"
            if transcribe_options.get("detect_language"):
                params["detect_language"] = "true"
            if transcribe_options.get("topics"):
                params["topics"] = "true"
            if transcribe_options.get("sentiment"):
                params["sentiment"] = "true"
            if transcribe_options.get("intents"):
                params["intents"] = "true"
            
            # Headers
            headers = {
                "Authorization": f"Token {api_key}",
                "Content-Type": "audio/mpeg" if audio_file_path.endswith(".mp3") else "application/octet-stream"
            }
            
            # Make REST API call with audio data
            response = requests.post(url, data=buffer_data, headers=headers, params=params)
            
            if response.status_code != 200:
                return {
                    "status": "error",
                    "content": [
                        {
                            "text": f"Deepgram transcription failed: {response.status_code} - {response.text}"
                        }
                    ],
                }
            
            # Parse JSON response
            response_json = response.json()
            
            # Extract results safely
            if not response_json.get("results") or not response_json["results"].get("channels"):
                return {
                    "status": "error",
                    "content": [
                        {"text": "No transcription results received from Deepgram"}
                    ],
                }

            channel = response_json["results"]["channels"][0]
            if not channel.get("alternatives"):
                return {
                    "status": "error",
                    "content": [{"text": "No transcription alternatives found"}],
                }

            alternative = channel["alternatives"][0]
            metadata = response_json.get("metadata", {})

            # Build comprehensive result
            result = {
                "transcript": alternative.get("transcript", ""),
                "confidence": alternative.get("confidence", 0.0),
                "language": language,
                "model": model,
                "duration": metadata.get("duration", 0.0),
                "word_count": len(alternative.get("words", [])),
                "features_used": {
                    "diarization": options.get("diarize", True),
                    "smart_format": options.get("smart_format", True),
                    "punctuation": options.get("punctuate", True),
                    "utterances": options.get("utterances", True),
                },
            }

            # Add speaker information if diarization is enabled
            if options.get("diarize", True) and channel.get("utterances"):
                speakers = {}
                for utterance in channel["utterances"]:
                    speaker_id = f"Speaker {utterance.get('speaker', 0)}"
                    if speaker_id not in speakers:
                        speakers[speaker_id] = {
                            "segments": [],
                            "total_duration": 0.0,
                        }
                    speakers[speaker_id]["segments"].append(
                        {
                            "text": utterance.get("transcript", ""),
                            "confidence": utterance.get("confidence", 0.0),
                            "start": utterance.get("start", 0.0),
                            "end": utterance.get("end", 0.0),
                        }
                    )
                    speakers[speaker_id]["total_duration"] += utterance.get("end", 0.0) - utterance.get("start", 0.0)

                result["speakers"] = speakers
                result["speaker_count"] = len(speakers)

            # Add word-level timing if available
            if alternative.get("words"):
                result["words"] = [
                    {
                        "word": word.get("word", ""),
                        "confidence": word.get("confidence", 0.0),
                        "start": word.get("start", 0.0),
                        "end": word.get("end", 0.0),
                    }
                    for word in alternative["words"]
                ]

            # Add sentiment if enabled
            if options.get("sentiment") and response_json["results"].get("sentiments"):
                result["sentiment"] = response_json["results"]["sentiments"]

            # Add topics if enabled
            if options.get("topics") and response_json["results"].get("topics"):
                result["topics"] = response_json["results"]["topics"]

            # Add intents if enabled
            if options.get("intents") and response_json["results"].get("intents"):
                result["intents"] = response_json["results"]["intents"]

            console.print(
                f"✅ Transcription completed: {len(result['transcript'])} chars, "
                f"{result['confidence']:.2%} confidence",
                style="green",
            )

            return {
                "status": "success",
                "content": [
                    {"text": result["transcript"]},
                    {"json": result},
                ],
            }

        elif action == "text_to_speech":
            # Validate text
            if not text:
                return {
                    "status": "error",
                    "content": [
                        {"text": "text parameter is required for text_to_speech action"}
                    ],
                }

            console.print(f"🎙️ Generating speech...", style="yellow")

            # Configure TTS options
            voice = options.get("voice", "aura-asteria-en")
            encoding = options.get("encoding", "mp3")
            sample_rate = options.get("sample_rate", 24000)

            # Deepgram REST API - Use direct HTTP request (not SDK client)
            # Docs: https://developers.deepgram.com/reference/text-to-speech/generate
            url = "https://api.deepgram.com/v1/speak"
            
            # Query parameters
            params = {
                "model": voice,
                "encoding": encoding,
            }
            # MP3 encoding doesn't support sample_rate parameter
            # Docs: https://developers.deepgram.com/docs/tts-encoding
            if sample_rate and encoding not in ["mp3", "opus", "aac"]:
                params["sample_rate"] = sample_rate
            
            # Headers
            headers = {
                "Authorization": f"Token {api_key}",
                "Content-Type": "application/json"
            }
            
            # Request body
            payload = {"text": text}
            
            # Make REST API call
            response = requests.post(url, json=payload, headers=headers, params=params)
            
            if response.status_code != 200:
                return {
                    "status": "error",
                    "content": [
                        {
                            "text": f"Deepgram TTS failed: {response.status_code} - {response.text}"
                        }
                    ],
                }

            # Get output path from options or use default
            output_path = options.get("output_path", "deepgram_output.mp3")
            output_path = os.path.expanduser(output_path)
            
            # Determine file extension based on encoding
            if not output_path.endswith(f".{encoding}"):
                base_path = output_path.rsplit(".", 1)[0] if "." in output_path else output_path
                output_path = f"{base_path}.{encoding}"
            
            # Save audio to file
            with open(output_path, "wb") as audio_file:
                audio_file.write(response.content)
            
            console.print(f"✅ Speech generated: {output_path}", style="green")
            
            # Auto-play if requested (default: True)
            play_audio = options.get("play_audio", True)
            if play_audio:
                try:
                    console.print("🔊 Playing audio...", style="yellow")
                    # Try macOS afplay first, then Linux aplay/mpg123
                    import platform
                    system = platform.system()
                    
                    if system == "Darwin":  # macOS
                        subprocess.run(["afplay", output_path], check=True)
                    elif system == "Linux":
                        # Try mpg123 for MP3, aplay for WAV/linear16
                        if encoding == "mp3":
                            subprocess.run(["mpg123", output_path], check=True)
                        else:
                            subprocess.run(["aplay", output_path], check=True)
                    else:
                        console.print("⚠️ Auto-play not supported on this OS", style="yellow")
                    
                    console.print("✅ Audio playback complete", style="green")
                except Exception as play_error:
                    console.print(f"⚠️ Playback failed: {play_error}", style="yellow")

            return {
                "status": "success",
                "content": [
                    {
                        "text": f"Speech generated successfully. Audio saved to: {output_path}\n"
                        f"Voice: {voice}, Encoding: {encoding}, Sample Rate: {sample_rate} Hz\n"
                        f"Play Audio: {'Played' if play_audio else 'Saved only'}"
                    }
                ],
            }

        elif action == "analyze":
            # Analyze is same as transcribe but with intelligence features enabled
            if not audio_source:
                return {
                    "status": "error",
                    "content": [
                        {
                            "text": "audio_source parameter is required for analyze action"
                        }
                    ],
                }

            # Enable intelligence features by default
            analysis_options = {
                **options,
                "sentiment": options.get("sentiment", True),
                "topics": options.get("topics", True),
                "intents": options.get("intents", True),
                "diarize": options.get("diarize", True),
            }

            # Recursive call with transcribe action and enhanced options
            return deepgram(
                action="transcribe",
                audio_source=audio_source,
                language=language,
                model=model,
                options=analysis_options,
            )

        else:
            return {
                "status": "error",
                "content": [
                    {
                        "text": f"Unknown action: {action}. Supported actions: transcribe, text_to_speech, analyze"
                    }
                ],
            }

    except Exception as e:
        logger.error(f"Deepgram operation failed: {str(e)}")
        console.print(f"❌ Deepgram operation failed: {str(e)}", style="red")
        return {
            "status": "error",
            "content": [{"text": f"Deepgram operation failed: {str(e)}"}],
        }

    finally:
        # Clean up temporary file if created
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temporary file: {cleanup_error}")

