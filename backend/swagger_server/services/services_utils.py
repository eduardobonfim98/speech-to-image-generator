import uuid
from swagger_server.database.mongo_client import gpt3_collection, audio_collection, stable_diffusion_collection


def create_id() -> str:
    """
    Create a unique id for a new action.

    :return: a unique id
    """
    return str(uuid.uuid4())


def save_action_gpt3 (action_data: dict):
    """
    Save an action to the database.

    :param action_data: the action data to save
    """
    gpt3_collection.insert_one(action_data)


def save_action_audio(action_data: dict):
    """
    Save an action to the database.

    :param action_data: the action data to save
    """
    audio_collection.insert_one(action_data)


def save_action_stable_diffusion(action_data: dict):
    """
    Save an action to the database.

    :param action_data: the action data to save
    """
    stable_diffusion_collection.insert_one(action_data)
