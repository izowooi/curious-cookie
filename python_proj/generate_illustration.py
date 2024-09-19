import time

from midjourney_sdk_py_multiple import Midjourney
import os
from dotenv import load_dotenv
import requests


class MidjourneyBot:

    def __init__(self, discord_channel_id, discord_user_token):
        self.midjourney = Midjourney(discord_channel_id, discord_user_token)

    def save_images(self, script_id, image_urls, paint_style):
        formatted_script_id = f'{script_id:06d}'

        for i, image_url in enumerate(image_urls[paint_style]):
            response = requests.get(image_url)
            formatted_img_index = f'{i:01d}'
            image_path = f'origin_png/{paint_style}/{formatted_script_id}_{paint_style}_{formatted_img_index}.png'
            with open(image_path, 'wb') as file:
                file.write(response.content)

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
