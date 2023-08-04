import json
import threading
import swagger_server.services.audio_service as audio_service
import swagger_server.services.gpt3_service as gpt3_service
from swagger_server.services.stable_diffusion_service import save_images_array

from swagger_server.services.rpc_client import Receiver
from swagger_server.services.rpc_client import send_message


def thread_target(routing_key, callback_fn):
    print(f"starting thread for:{routing_key}. - Thread number: {threading.get_ident()}.")
    receiver = Receiver(routing_key, callback_fn)
    receiver.start_consuming()


def send_gpt3_request(prompt: str, prompt_enhanced_id: str):
    print("send_gpt3_request - rabbitmq_service.py")
    """
    Send a request to RabbitMQ to call the GPT-3 model.
    :param prompt: the prompt to enhance
    :param prompt_enhanced_id: the id of the enhanced prompt
    """

    dict_data = {
        "prompt": prompt,
        "prompt_enhanced_id": prompt_enhanced_id,
    }
    print(dict_data)
    payload = json.dumps(dict_data)
    send_message('gpt3_request', payload)


def gpt3_callback(body: json):
    print(
        "gpt3_callback called - rabbitmq_service.py - The function that is called as soon as RabbitMQ receives a "
        "response from the GPT-3 model.")
    """
    The function that is called as soon as RabbitMQ receives a response from the GPT-3 model.
    :return:
    """
    body = json.loads(body)  # Maybe do this for each callback!?
    print("gpt3_callback - body: ", body)
    gpt3_service.save_enhanced_prompt(body['prompt_enhanced_id'], body['enhanced_prompt'], body['status'])


def send_audio_transcription_request(transcription_id: str, audio_language: str, data: str):
    print("send_audio_transcription_request called")
    """
    Send a request to RabbitMQ to call the audio transcription model.
    :param transcription_id: the id of the transcription
    :param audio_language: the audio language
    :param data: the audio data

    """

    dict_data = {
        "transcription_id": transcription_id,
        "audio_language": audio_language,
    }
    payload = bytearray(json.dumps(dict_data).encode("utf-8"))
    payload.extend(data)
    send_message('audio_request', payload)


def audio_callback(body: json):
    print("audio_callback called")
    """
    The function that is called as soon as RabbitMQ receives a response from the audio transcription model.
    :return:
    """

    body = json.loads(body)
    audio_service.save_transcription(body['transcription_id'], body['transcript_content'],
                                     body['transcript_content_translated'], body['status'], body['error'])


def sends_images_generation_request(prompt: str, number_of_images: int, number_of_inference_steps: int, height: int,
                                    width: int, images_array_id: str):
    print("sends_images_generation_request called")
    """
    Send a request to RabbitMQ to call the image generation model.

    :param prompt: Prompt to generate images from
    :param number_of_images: Number of images to generate
    :param number_of_inference_steps: Number of inference steps
    :param height: Height of the images
    :param width: Width of the images
    :param images_array_id: Image array id
    :return:
    """

    dict_data = {
        "prompt": prompt,
        "number_of_images": number_of_images,
        "number_of_inference_steps": number_of_inference_steps,
        "height": height,
        "width": width,
        "images_array_id": images_array_id,
    }
    print("sends_images_generation_request")
    payload = json.dumps(dict_data)
    send_message('stable_diffusion_request', payload)


def stable_diffusion_callback(body: json):
    """
    The function that is called as soon as RabbitMQ receives a response from the stable diffusion model
    :return:
    """

    body = json.loads(body)

    if "images_array_id" in body:
        print("stable_diffusion_callback")
        body['images_array'] = [img.encode('latin1') for img in body['images_array']]
        save_images_array(body['images_array_id'], body['images_array'], body['status'], body['images_progress'])


gpt3ProcessThread = threading.Thread(target=thread_target, args=('gpt3_response', gpt3_callback))
audioProcessThread = threading.Thread(target=thread_target, args=('audio_response', audio_callback))
imageProcessThread = threading.Thread(target=thread_target,
                                      args=('stable_diffusion_response', stable_diffusion_callback))
gpt3ProcessThread.start()
audioProcessThread.start()
imageProcessThread.start()
