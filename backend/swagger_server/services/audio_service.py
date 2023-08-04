import base64
import io
import os
import uuid

import soundfile
from werkzeug.utils import secure_filename

import swagger_server.services.rabbitmq_service as rabbitmq_service
from swagger_server.database.mongo_client import audio_collection
from swagger_server.models import TextFromAudio
from swagger_server.models.audio import Audio
from swagger_server.services.config import CONFIG
from swagger_server.services.services_utils import create_id, save_action_audio


def handle_post(audio: Audio) -> TextFromAudio:
    """
    Handle a POST request to the audio endpoint.

    :param audio: The audio file to transcript
    :return: TextFromAudio instance
    """
    transcription_id = create_id()
    filepath_wav = save_audio_blob(audio)
    audio_language = audio.audio_language
    rabbitmq_service.send_audio_transcription_request(transcription_id, audio_language, open(filepath_wav, "rb").read())
    save_post_request(audio, transcription_id, filepath_wav, "in progress")
    return TextFromAudio(audio_id=transcription_id, audio_content=None)


def save_post_request(audio: Audio, audio_id: str, filepath_wav: str, database_status: str):
    """
    Save the POST request to the database.
    :param audio: The audio data
    :param audio_id: The id of the transcription
    :param filepath_wav: The path to the audio file
    :param database_status: Status of the database
    """
    save_action_audio({
        'audio_id': audio_id,
        'session_id': audio.session_id,
        'action_id': audio.action_id,
        'transcript_str': None,
        'transcript_translated': None,
        'audioo_file': filepath_wav,
        'audio_lang': audio.audio_language,
        'action_type': 'audio_transcription',
        'status': database_status
    })


def save_audio_blob(audio: Audio) -> str:
    """
    Save the audio blob to the filesystem
    :param audio: The audio data
    :return: filepath to the audio file
    """
    filename = secure_filename(f'{audio.session_id}_{audio.action_id}_{uuid.uuid4()}')
    filename = os.path.join(CONFIG['openai']['audio_path'], filename)

    with open(f"{filename}.mp4", 'wb') as f:
        f.write(io.BytesIO(base64.b64decode(str(audio.blob_data.split(",")[1:]))).getbuffer())
    os.system(f"ffmpeg -i {filename}.mp4 -acodec pcm_s16le -ar 16000 {filename}.wav")

    return f"{filename}.wav"


def handle_get(audio_id: str) -> TextFromAudio:
    print("Handling get request for audio")
    print(f"Audio id: {audio_id}")
    """
    Handle a GET request to the audio endpoint.
    :param audio_id: The id of the audio transcription
    :return: TextFromAudio instance
    """
    transcript_translated = get_transcription_from_db(audio_id)
    return TextFromAudio(audio_id=audio_id, audio_content=transcript_translated)


def get_transcription_from_db(audio_id: str) -> str:
    """
    Get the audio from the database.
    :param audio_id: the id of the audio transcription
    :return: the audio transcription
    """
    audio = audio_collection.find_one(
        {"audio_id": audio_id}
    )
    if audio is None:
        raise ValueError(f'No audio with id {audio_id} found.')
    return audio['transcript_translated']


def save_transcription(audio_id: str, transcript_str: str, transcript_translated: str, status: str, error: str):
    """
    Save the audio transcription to the database.
    :param audio_id: the id of the audio transcription
    :param transcript_str: the audio transcription
    :param transcript_translated: the translated audio transcription
    :param status: status of the request
    :param error: error
    """
    print(f"Saving transcription {audio_id} to database", transcript_str, transcript_translated, status, error)
    audio_collection.update_one(
        {"audio_id": audio_id},
        {"$set": {"transcript_str": transcript_str, "transcript_translated": transcript_translated, "status": status,
                  "error": error}},
    )
