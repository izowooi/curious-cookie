from upload_script import FBManger
from generate_scripts import OpenAIChatbot
from generate_illustration import MidjourneyBot
import os
from dotenv import load_dotenv


load_dotenv()

open_ai_api_key = os.getenv('OPEN_AI_API_KEY')
firebase_admin_key = os.getenv('FIREBASE_ADMIN_KEY')
firebase_db_url = os.getenv('FIREBASE_DB_URL')
discord_channel_id = os.getenv('DISCORD_CHANNEL_ID')
discord_user_token = os.getenv('DISCORD_USER_TOKEN')

fb_manager = FBManger(firebase_admin_key, firebase_db_url)
openai_chat_bot = OpenAIChatbot(open_ai_api_key)
midjourney_bot = MidjourneyBot(discord_channel_id, discord_user_token)


def main():
    pre_question = '공룡은 왜 멸종했나요?'#todo: 미리 정의된 DB 에서 처리되지 않은 질문을 리스트로 가져와서 요청해야함.
    question_id = 0
    script_list, prompt_list, category = openai_chat_bot.generate_script(pre_question)

    fb_manager.append_script_list_to_db(question_id, script_list, prompt_list)

    midjourney_bot.generate_illustration_list(question_id, prompt_list)


def test_gen_script():
    pre_question = '공룡은 왜 멸종했나요?'  # todo: 미리 정의된 DB 에서 처리되지 않은 질문을 리스트로 가져와서 요청해야함.
    question_id = 0
    script_list, prompt_list, category = openai_chat_bot.generate_script(pre_question)

    fb_manager.append_script_list_to_db(question_id, script_list, prompt_list)


def test_gen_illustration():
    question_id = 0
    
    prompt_list = ['A scene with diverse children lying down, each with unique dream bubbles showing different themes.',
                   'A cheerful sun shining over a child smiling, with a dark cloud representing a bad dream far away.']

    midjourney_bot.generate_illustration_list(question_id, prompt_list)
