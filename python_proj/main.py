from midjourney_sdk_py import Midjourney

discord_channel_id = ""
discord_user_token = ""

midjourney = Midjourney(discord_channel_id, discord_user_token)

prompt = "Modern interior design, a billiard hall with pool tables and a seating area with sofas, dark gray walls, green felt on the table cloth, industrial-style architecture, photorealistic, high-resolution photography."
options = {
    "ar": "16:9",
    "v": "6.0",
}

message = midjourney.generate(prompt, options)

print(message['upscaled_photo_url'])