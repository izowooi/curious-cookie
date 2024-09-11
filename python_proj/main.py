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
    start_time = time.time()

    question_dict = fb_manager.get_no_script_from_db()

    for question_id, question_text in question_dict.items():
        print(f'question_id: {question_id}, question_text: {question_text}')
        script_dict, prompt_list, category = openai_chat_bot.generate_script(question_text)
        script_id_list = fb_manager.append_script_list_to_db(question_id, script_dict, prompt_list)
        fb_manager.set_generated_script(question_id)

        gen_script_time = time.time()
        #todo:script_id_list 로직 추가 후 테스트 안 되었음.
        midjourney_bot.generate_and_save_illustrations_list(script_id_list, prompt_list)
        gen_illustration_time = time.time()
        #todo:일러스트 만든 후에 디비에 저장하는 코드 추가

        print(f'gen_script_time: {gen_script_time - start_time}')
        print(f'gen_illustration_time: {gen_illustration_time - gen_script_time}')
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
    no_illustration_dict = fb_manager.get_no_illustration_from_db()

    for script_id, prompt in no_illustration_dict.items():
        print(f'script_id: {script_id}, prompt_list: {prompt}')
        midjourney_bot.generate_and_save_illustrations(script_id, prompt)
        fb_manager.set_processed_script(script_id)


#main()
test_gen_illustration()
#test_gen_script()
