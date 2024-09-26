from midjourney_sdk_py_multiple import Midjourney
import requests
from PIL import Image
from io import BytesIO
import os

class MidjourneyBot:

    def __init__(self, discord_channel_id, discord_user_token):
        self.midjourney = Midjourney(discord_channel_id, discord_user_token)

    def save_images(self, script_id, image_urls, paint_style):
        formatted_script_id = f'{script_id:06d}'

        for i, image_url in enumerate(image_urls[paint_style]):
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            self.split_image(img, formatted_script_id, paint_style)

    def split_image(self, img, script_id, paint_style):
        width, height = img.size

        piece_width = width // 2
        piece_height = height // 2

        base_name = f'origin_png/{paint_style}/{script_id}_{paint_style}'
        directory = os.path.dirname(base_name)

        # 폴더가 없을 경우 생성
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory {directory}")

        for i in range(2):
            for j in range(2):
                left = j * piece_width
                upper = i * piece_height
                right = (j + 1) * piece_width
                lower = (i + 1) * piece_height
                box = (left, upper, right, lower)
                piece = img.crop(box)
                piece_path = f"{base_name}_{i * 2 + j}.png"
                piece.save(piece_path)
                print(f"Saved {piece_path}")


    def generate_and_save_illustrations_list(self, script_id_list, prompt_list):
        for script_id, prompt in zip(script_id_list, prompt_list):
            image_urls = self.generate_illustration_by_prompt(prompt)
            self.save_images(script_id, image_urls)

    def generate_and_save_illustrations(self, script_id, prompt, paint_style, prompt_suffix):
        image_urls = self.generate_illustration_by_prompt(prompt, paint_style, prompt_suffix)
        self.save_images(script_id, image_urls, paint_style)

    def generate_illustration_by_prompt(self, prompt, paint_style, prompt_suffix):
        image_urls = {paint_style: []}
        options = {
            "ar": "16:9",
            "v": "6.1"
        }
        # illustration_styles = [' Early Clean, minimalist design. vector illustration japanese --p om8joos',
        #                  ' Pixar style, 3D rendered, bright colors, expressive emotions, smooth textures, detailed lighting, cinematic composition',
        #                  ' vector illustration japanese --p om8joos']

        img_prompt = f'{prompt}' + prompt_suffix
        message = self.midjourney.generate(img_prompt, options, upscale=False)
        imagine = message['imagine']

        image_url = imagine['raw_message']['attachments'][0]['url']
        image_urls[paint_style].append(image_url)

        return image_urls
