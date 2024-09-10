from upload_script import FBManger
from generate_scripts import OpenAIChatbot
from generate_illustration import MidjourneyBot
import os
from dotenv import load_dotenv
import time


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
    # 함수 실행 전 시간 측정
    start_time = time.time()

    pre_question = '공룡은 왜 멸종했나요?'#todo: 미리 정의된 DB 에서 처리되지 않은 질문을 리스트로 가져와서 요청해야함.
    question_id = 0

    script_list, prompt_list, category = openai_chat_bot.generate_script(pre_question)
    gen_script_time = time.time()

    #fb_manager.append_script_list_to_db(question_id, script_list, prompt_list)

    fb_save_time = time.time()
    midjourney_bot.generate_illustration_list(question_id, prompt_list)
    gen_illustration_time = time.time()

    print(f'gen_script_time: {gen_script_time - start_time}')
    print(f'fb_save_time: {fb_save_time - gen_script_time}')
    print(f'gen_illustration_time: {gen_illustration_time - fb_save_time}')
    # 6개의 이미지 ( 4개는 업스케일 ) 80초 정도 소요됨, 한 컷을 60초로 가정하면 10컷은 10분.
    # 질문 하나에 10분을 가정하면 1시간에 6개의 질문을 처리할 수 있음.
    # 미드저니 요금제가 200분을 주면 20개 정도 한달에 만들 수 있음. 몇개 못 만드네.


def test_gen_script():
    question_dict = fb_manager.get_unprocessed_questions_from_db()
    for question_id, question_text in question_dict.items():
        script_dict, prompt_list, category = openai_chat_bot.generate_script(question_text)
        fb_manager.append_script_list_to_db(question_id, script_dict, prompt_list)
        fb_manager.set_processed_question(question_id)


def test_gen_illustration():
    question_id = 0

    prompt_list = ['A scene with diverse children lying down, each with unique dream bubbles showing different themes.']

    midjourney_bot.generate_illustration_list(question_id, prompt_list)


#main()
#test_gen_illustration()
#test_gen_script()