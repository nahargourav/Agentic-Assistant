# Voice to text conversion logic
# Speech-to-Text integration using OpenAI Whisper.
import os
import logging
from typing import Any, Dict, Optional
from pydub import AudioSegment

# For external services, we assume OpenAI Whisper here (modify as needed)
import openai

# Set up logging for debug and observability
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("speech_to_text")

class SpeechToTextError(Exception):
    """Custom exception for speech-to-text errors."""
    pass

class SpeechToText:
    """
    Handles voice-to-text conversion using third-party libraries like OpenAI Whisper.
    The audio file is transcoded (if needed) and then sent to the ASR service for transcription.
    """

    SUPPORTED_FORMATS = ["wav", "mp3", "m4a", "flac", "ogg"]  # Supported input formats

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Speech-to-Text engine with optional API key.
        Args:
            api_key (Optional[str]): API key for OpenAI Whisper or similar service.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")  # Retrieve from env variables as fallback
        if not self.api_key:
            raise ValueError("API Key for Speech-to-Text service is required.")

        openai.api_key = self.api_key

    def transcribe(self, audio_file_path: str, language: Optional[str] = "en") -> Dict[str, Any]:
        """
        Transcribes an audio file to text using OpenAI Whisper or similar ASR services.
        Args:
            audio_file_path (str): Path to the audio file to transcribe.
            language (Optional[str]): Explicit language hint (default: "en").

        Returns:
            Dict[str, Any]: A dictionary containing transcription text and metadata.
        """
        # Check the file's format
        file_ext = audio_file_path.split(".")[-1].lower()
        if file_ext not in self.SUPPORTED_FORMATS:
            raise SpeechToTextError(f"Unsupported audio format: {file_ext}")

        try:
            logger.info(f"Transcoding audio file if needed: {audio_file_path}")
            normalized_audio_path = self._convert_audio_to_wav(audio_file_path)

            logger.info(f"Sending transcoded audio file to ASR service: {normalized_audio_path}")
            # Send audio to Whisper API for transcription
            with open(normalized_audio_path, "rb") as audio_file:
                response = openai.Audio.transcribe("whisper-1", audio_file, language=language)

            logger.info(f"Transcription successful for file: {audio_file_path}")
            return {
                "text": response.get("text", ""),
                "language": response.get("language", language),
                "duration": self._get_audio_duration(normalized_audio_path)  # Duration in seconds
            }

        except Exception as e:
            logger.error(f"Error during speech-to-text processing: {str(e)}")
            raise SpeechToTextError(f"Speech-to-text failed for file {audio_file_path}: {str(e)}")

    def _convert_audio_to_wav(self, audio_file_path: str) -> str:
        """
        Converts audio files to WAV format for ASR compatibility (if required).
        Args:
            audio_file_path (str): Path to the original audio file.
        Returns:
            str: Path to the converted WAV file.
        """
        file_ext = audio_file_path.split(".")[-1].lower()
        if file_ext == "wav":
            # Already in WAV format, no need to convert
            return audio_file_path

        # Load audio file and convert to WAV format
        try:
            audio = AudioSegment.from_file(audio_file_path, format=file_ext)
            wav_file_path = audio_file_path.rsplit(".", 1)[0] + ".wav"
            audio.export(wav_file_path, format="wav")
            logger.info(f"Audio file converted to WAV: {wav_file_path}")
            return wav_file_path
        except Exception as e:
            logger.error(f"Audio conversion failed for file {audio_file_path}: {str(e)}")
            raise SpeechToTextError(f"Audio conversion failed: {str(e)}")

    def _get_audio_duration(self, audio_file_path: str) -> float:
        """
        Measures the duration of the audio file.
        Args:
            audio_file_path (str): Path to the audio file.
        Returns:
            float: Duration in seconds.
        """
        try:
            audio = AudioSegment.from_file(audio_file_path)
            duration = len(audio) / 1000.0  # Milliseconds to seconds
            logger.info(f"Audio duration: {duration} seconds")
            return duration
        except Exception as e:
            logger.error(f"Failed to measure duration of audio: {str(e)}")
            raise SpeechToTextError(f"Audio duration measurement failed: {str(e)}")