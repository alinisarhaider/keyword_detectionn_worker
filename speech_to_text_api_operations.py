import io
import os

from google.cloud.speech import enums
from google.cloud import speech
from google.cloud.speech import types
from google.oauth2 import service_account
from pydub import AudioSegment


def transcribe_audio(audio_data: AudioSegment, language: str):
    """Transcribe the given audio file."""

    # Checking credentials
    service_account_info = eval(os.environ.get('account_info'))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    client = speech.SpeechClient(credentials=credentials)

    start = 0
    end = 60000
    step = 60000
    response_list: list = list()
    time_offset_list: list = list()

    while start < len(audio_data):
        if end < len(audio_data):
            trimmed_data = audio_data[start:end]
        else:
            trimmed_data = audio_data[start:]

        buf = io.BytesIO()
        trimmed_data.export(buf, format='flac')

        audio = types.RecognitionAudio(content=buf.getvalue())

        # Setting configurations
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            language_code=language,
            audio_channel_count=audio_data.channels,
            enable_word_time_offsets=True)

        # Requesting Speech-to-text Google API
        response = client.recognize(config, audio)

        response_list.append(response)
        time_offset_list.append(int(start / 1000))
        start += step
        end += step

    return response_list, time_offset_list
