import connexion

from swagger_server.models.image_generator import ImageGenerator  # noqa: E501
from swagger_server.services.stable_diffusion_service import handle_images_post, handle_images_get

def stable_diffusion_generate_images_images_array_id_get(images_array_id):  # noqa: E501
    """stable_diffusion_generate_images_images_array_id_get

     # noqa: E501

    :param images_array_id: imagesArrayId
    :type images_array_id: str

    :rtype: Images
    """
    print("stable_diffusion_generate_images_images_array_id_get")
    return handle_images_get(images_array_id)


def stable_diffusion_generate_images_post(body):  # noqa: E501
    """stable_diffusion_generate_images_post

     # noqa: E501

    :param body: Sending the prompt to generate images
    :type body: dict | bytes

    :rtype: Images
    """
    print("stable_diffusion_generate_images_post")
    print(body)
    if connexion.request.is_json:
        body = ImageGenerator.from_dict(connexion.request.get_json())  # noqa: E50
    print("body after stable_diffusion_generate_images_post ")
    print(body)
    return handle_images_post(body)



