import base64
import os
from typing import List
import io
import PIL
from PIL import Image
from werkzeug.utils import secure_filename

from swagger_server.database.mongo_client import stable_diffusion_collection
from swagger_server.models import ImageGenerator
from swagger_server.models.image import Image
from swagger_server.models.images import Images
import swagger_server.services.rabbitmq_service as rabbitmq_service
from swagger_server.services.services_utils import create_id, save_action_stable_diffusion
from swagger_server.services.config import CONFIG


def handle_images_post(img_generator: ImageGenerator) -> Images:
    print("entered handle_images_post of stable_diffusion_service.py")
    """
    Handle a POST request to the stable diffusion endpoint.
    :param img_generator: The image generator data
    :return: Image instance
    """
    images_array_id = create_id()
    rabbitmq_service.sends_images_generation_request(img_generator.prompt_enhanced, img_generator.number_of_images,
                                                     img_generator.number_of_inference_steps, img_generator.height,
                                                     img_generator.width,
                                                     images_array_id)
    save_post_request_images(img_generator, images_array_id, "in progress", "in progress")
    return Images(images_array_id=images_array_id, image_array_content=None, images_progress=None)


def handle_images_get(images_array_id: str) -> Images:
    print("entered handle_images_get of stable_diffusion_service.py")
    """
    Handle a GET request to the stable diffusion endpoint.
    :param images_array_id: The id of the image array
    :return: Images instance
    """
    image_array_content, images_progress = get_image_array_content(images_array_id)
    return Images(images_array_id=images_array_id, image_array_content=image_array_content,
                  images_progress=images_progress)


def save_post_request_images(img_generator: ImageGenerator, images_array_id: str, database_status: str,
                             images_progress: str):
    """
    Save the POST request to the database.
    :param img_generator: image generator data
    :param images_array_id: id of the image array
    :param database_status: database status
    """
    save_action_stable_diffusion({
        'image_array_id': images_array_id,
        'session_id': img_generator.session_id,
        'action_id': img_generator.action_id,
        'prompt': img_generator.prompt_enhanced,
        'num_inference_steps': img_generator.number_of_inference_steps,
        'n_images': img_generator.number_of_images,
        'height': img_generator.height,
        'width': img_generator.width,
        'image_save_paths': "",
        'action_type': 'generate_batch',
        'status': database_status,
        'images_progress': images_progress,
    })


def get_image_array_content(images_array_id: str) -> List[Image]:
    print("entered get_image_array_content of stable_diffusion_service.py")

    """
    Get the image array content from the database.
    :param images_array_id: id of the image array
    :return: list of images
    """
    action = stable_diffusion_collection.find_one({'image_array_id': images_array_id})
    image_save_paths = action['image_save_paths']
    image_array_content = []
    images_progress = action['images_progress']
    for image_save_path in image_save_paths:
        image_content = pil_img_to_byte(PIL.Image.open(image_save_path))
        image_array_content.append(Image(image_id=None, image_content=image_content, images_progress=images_progress))
    print("image_array_content: ", images_array_id)
    return image_array_content, images_progress


def pil_img_to_byte(pil_img: PIL.Image) -> str:
    """
    Convert a PIL image to a byte array.
    :param pil_img: PIL image
    :return: Byte array
    """
    # Convert the image to a byte buffer
    with io.BytesIO() as buffer:
        pil_img.save(buffer, format="JPEG")
        image_bytes = buffer.getvalue()

    # Convert the byte string to a base64-encoded string
    base64_string = base64.b64encode(image_bytes).decode('utf-8')
    return base64_string


def save_images_array(images_array_id: str, images_array: List[bytes], status: str, images_progress: str):
    """
    Save the images array to the filesystem.
    :param images_array_id: id of the images array
    :param images_array: a list of images
    """

    image_save_paths = []
    img_generator = stable_diffusion_collection.find_one({'image_array_id': images_array_id})
    width = img_generator['width']
    height = img_generator['height']

    for i, img in enumerate(images_array):
        path = secure_filename(f'{img_generator["session_id"]}_{i}_{img_generator["action_id"]}.jpg')
        path = os.path.join(CONFIG['openai']['image_path'], path)
        image_save_paths.append(path)
        img2 = PIL.Image.frombytes("RGB", (width, height), img)
        img2.save(path, 'JPEG', quality=70)
        print("image save at", {path})
        img2.close()

    stable_diffusion_collection.update_one({'image_array_id': images_array_id},
                                           {'$set': {'image_save_paths': image_save_paths,
                                                     'status': status, 'images_progress': images_progress}})
