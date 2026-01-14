import os
import logging
from typing import Dict, Optional
import openai

# Setup logging for monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("whisper")

class WhisperError(Exception):
    """Custom exception for Whisper-related errors."""
    pass

class Whisper:
    """
    Wrapper for OpenAI's Whisper API for speech-to-text transcription.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the Whisper wrapper with API key.
        Args:
            api_key (Optional[str]): API key for accessing the OpenAI Whisper API.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key for OpenAI Whisper is required.")
        openai.api_key = self.api_key
        logger.info("Whisper API wrapper initialized.")

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> Dict[str, str]:
        """
        Transcribes an audio file to text using OpenAI Whisper.
        Args:
            audio_path (str): The path to the audio file to transcribe.
            language (Optional[str]): The language of the audio, if known (e.g., "en" for English).

        Returns:
            Dict[str, str]: Transcription result including text.
        """
        try:
            logger.info(f"Transcribing audio file: {audio_path}")
            with open(audio_path, "rb") as audio_file:
                response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
            transcription = response.get("text", "")
            logger.info("Transcription successful.")
            return {"text": transcription}
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise WhisperError(f"Transcription failed for file {audio_path}: {str(e)}")