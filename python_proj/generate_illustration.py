import time

from midjourney_sdk_py_multiple import Midjourney
import os
from dotenv import load_dotenv
import requests


class MidjourneyBot:

    def __init__(self, discord_channel_id, discord_user_token):
        self.midjourney = Midjourney(discord_channel_id, discord_user_token)

    def save_images(self, question_id, script_seq, image_urls):
        formatted_question_id = f'{question_id:04d}'
        formatted_script_seq = f'{script_seq:02d}'
        image_style = "3d"  # 2d, reality
        for i, image_url in enumerate(image_urls):
            response = requests.get(image_url)
            formatted_img_index = f'{i:01d}'
            image_path = f'{image_style}/{formatted_question_id}_{formatted_script_seq}_{image_style}_{formatted_img_index}.png'
            with open(image_path, 'wb') as file:
                file.write(response.content)

    def generate_illustration_list(self, question_id, prompt_list):
        for index, prompt in enumerate(prompt_list):
            image_urls = self.generate_illustration_by_prompt(prompt)
            self.save_images(question_id, index, image_urls)

    def generate_illustration_by_prompt(self, prompt):
        image_urls = []
        options = {
            #"ar": "16:9",
            "ar": "1:1",
            "v": "6.1",
        }

        prompt = f'{prompt}' +\
                 ' Pixar style, 3D rendered, bright colors, expressive emotions, smooth textures, detailed lighting, cinematic composition'
        message = self.midjourney.generate(prompt, options, upscale_index=0)
        image_urls.append(message['upscaled_photo_url'])

        if 'imagine' in message:
            imagine = message['imagine']
            upscaled_photo_url = self.midjourney.upscale(imagine, 3)
            image_urls.append(upscaled_photo_url)

        return image_urls

    def test(self):
        prompt = "A fun and whimsical scene with strange, colorful creatures and unusual landscapes." +\
                 " Pixar style, 3D rendered, bright colors, expressive emotions, smooth textures, detailed lighting, cinematic composition"
        options = {
            #"ar": "16:9",
            "ar": "1:1",
            "v": "6.1",
        }

        image_urls = []

        for index, url in enumerate(image_urls):
            response = requests.get(url)
            if response.status_code == 200:
                with open(f'test_{index}.png', 'wb') as file:
                    file.write(response.content)
                print(f"Image saved as test_{index}.png")
            else:
                print(f"Failed to download image from {url}")

        # message = midjourney.generate(prompt, options, upscale_index=0)
        #
        # print(f"index 0 : {message['upscaled_photo_url']}")
        #
        # if 'imagine' in message:
        #     imagine = message['imagine']
        #     upscaled_photo_url = midjourney.upscale(imagine, 3)
        #     print(f'index 3 : {upscaled_photo_url}')

        # prompt_list = [prompt]
        #
        # for prompt in prompt_list:
        #     print(prompt)
