import connexion

from swagger_server.models.audio import Audio
from swagger_server.services.audio_service import handle_post, handle_get


def audio_audio_id_get(audio_id):  # noqa: E501
    """audio_audio_id_get

     # noqa: E501

    :param audio_id: audioId
    :type audio_id: str

    :rtype: TextFromAudio
    """
    print("audio_audio_id_get")
    return handle_get(audio_id)


def audio_post(body):  # noqa: E501
    """audio_post

     # noqa: E501

    :param body: Sending the parameters to transform the audio into text
    :type body: dict | bytes

    :rtype: TextFromAudio
    """
    print("audio_post")
    if connexion.request.is_json:
        body = Audio.from_dict(connexion.request.get_json())  # noqa: E501
    return handle_post(body)
