import connexion
import six

from swagger_server.models.prompt import Prompt  # noqa: E501
from swagger_server.models.prompt_enhanced import PromptEnhanced  # noqa: E501
from swagger_server.services.gpt3_service import handle_post, handle_get


def gpt3_post(body):  # noqa: E501
    """gpt3_post

     # noqa: E501

    :param body: Sending the text to be enhanced
    :type body: dict | bytes

    :rtype: PromptEnhanced
    """
    print("gpt3_post")
    if connexion.request.is_json:
        body = Prompt.from_dict(connexion.request.get_json())  # noqa: E501
        print(body)
    return handle_post(body)


def gpt3_prompt_enhanced_id_get(prompt_enhanced_id):  # noqa: E501
    """gpt3_prompt_enhanced_id_get

     # noqa: E501

    :param prompt_enhanced_id: promptEnhancedId
    :type prompt_enhanced_id: str

    :rtype: PromptEnhanced
    """
    # Call Service
    return handle_get(str(prompt_enhanced_id))
