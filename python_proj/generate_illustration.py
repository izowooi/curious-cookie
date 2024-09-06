from midjourney_sdk_py import Midjourney
import os
from dotenv import load_dotenv

load_dotenv()

discord_channel_id = os.getenv('DISCORD_CHANNEL_ID')
discord_user_token = os.getenv('DISCORD_USER_TOKEN')

midjourney = Midjourney(discord_channel_id, discord_user_token)

prompt = "An illustration showing the seven colors of the rainbow, labeled: red, orange, yellow, green, blue, indigo, violet. a cute 3d style"
options = {
    "ar": "1:1",
    "v": "6.1",
}

message = midjourney.generate(prompt, options)

print(message['upscaled_photo_url'])