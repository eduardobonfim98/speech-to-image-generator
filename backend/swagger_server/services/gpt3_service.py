from swagger_server.models import PromptEnhanced, Prompt
from swagger_server.database.mongo_client import gpt3_collection
import swagger_server.services.rabbitmq_service as rabbitmq_service
from swagger_server.services.services_utils import create_id, save_action_gpt3


def handle_post(prompt: Prompt) -> PromptEnhanced:
    """
    Handle a POST request to the GPT3 endpoint.
    :param prompt: the prompt to enhance
    :return: the enhanced prompt
    """
    print("entered handle_post of gpt3")
    prompt_enhanced_id = create_id()
    print("prompt_enhanced_id: " + prompt_enhanced_id)
    rabbitmq_service.send_gpt3_request(prompt.prompt, prompt_enhanced_id)
    save_post_request(prompt, prompt_enhanced_id, "in progress")
    return PromptEnhanced(prompt_enhanced_id=prompt_enhanced_id, prompt_enhanced_content=None)


def handle_get(prompt_enhanced_id: str) -> PromptEnhanced:
    """
    Handle a GET request to the GPT3 endpoint.
    :param prompt_enhanced_id: The id of the enhanced prompt
    :return: the enhanced prompt
    """
    prompt_enhanced_content = get_enhanced_prompt(prompt_enhanced_id)
    print("entered handle_get of gpt3")
    print(f"prompt_enhanced_content: {prompt_enhanced_content} \n prompt_enhanced_id: {prompt_enhanced_id}")
    return PromptEnhanced(prompt_enhanced_id=prompt_enhanced_id, prompt_enhanced_content=prompt_enhanced_content)


def save_enhanced_prompt(prompt_enhanced_id: str, enhanced_prompt: str, status: str):
    """
    Save the enhanced prompt to the database.
    :param prompt_enhanced_id: the id of the enhanced prompt
    :param enhanced_prompt: the enhanced prompt
    :param status: status of the request
    """
    gpt3_collection.update_one(
        {"prompt_enhanced_id": prompt_enhanced_id},
        {"$set": {"enhanced_prompt": enhanced_prompt, "status": status}}
    )


def save_post_request(prompt: Prompt, prompt_enhanced_id: str, database_status: str):
    """
    Save the POST request to the database.
    :param prompt: the prompt to enhance
    :param prompt_enhanced_id: prompt id
    :param database_status: status of the database
    """
    save_action_gpt3({
        'prompt_enhanced_id': prompt_enhanced_id,
        'session_id': prompt.session_id,
        'action_id': int(prompt.action_id),
        'prompt': prompt.prompt,
        'enhanced_prompt': "None",
        'action_type': 'enhance_prompt',
        'status': database_status
    })


def get_enhanced_prompt(prompt_enhanced_id: str) -> str:
    """
    Get the enhanced prompt from the database.
    :param prompt_enhanced_id: the id of the enhanced prompt
    :return: the enhanced prompt
    """
    action = gpt3_collection.find_one({'prompt_enhanced_id': prompt_enhanced_id})
    if action is None:
        raise ValueError(f'No prompt with id {prompt_enhanced_id} found.')
    return action['enhanced_prompt']
