import time

from midjourney_sdk_py_multiple import Midjourney
import os
from dotenv import load_dotenv

load_dotenv()

discord_channel_id = os.getenv('DISCORD_CHANNEL_ID')
discord_user_token = os.getenv('DISCORD_USER_TOKEN')

midjourney = Midjourney(discord_channel_id, discord_user_token)

prompt = "A bright dream world with a child flying with balloons, meeting friendly animals, and playing with toys.." +\
         " Pixar style, 3D rendered, bright colors, expressive emotions, smooth textures, detailed lighting, cinematic composition"
options = {
    #"ar": "16:9",
    "ar": "1:1",
    "v": "6.1",
}

message = midjourney.generate(prompt, options, upscale_index=0)

print(f"index 0 : {message['upscaled_photo_url']}")

if 'imagine' in message:
    imagine = message['imagine']
    upscaled_photo_url = midjourney.upscale(imagine, 3)
    print(f'index 1 : {upscaled_photo_url}')
