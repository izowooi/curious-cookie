from upload_script import FBManger
from generate_scripts import OpenAIChatbot
import os
from dotenv import load_dotenv

load_dotenv()

open_ai_api_key = os.getenv('OPEN_AI_API_KEY')
firebase_admin_key = os.getenv('FIREBASE_ADMIN_KEY')
firebase_db_url = os.getenv('FIREBASE_DB_URL')

fb_manager = FBManger(firebase_admin_key, firebase_db_url)
chatbot = OpenAIChatbot(open_ai_api_key)

pre_question = '공룡은 왜 멸종했나요?'
question_id = 1
script_list, prompt_list, category = chatbot.generate_script(pre_question)

# 결과 출력
print(f"script_list = {script_list}")
print(f"prompt_list = {prompt_list}")
print(f"category = {category}")


fb_manager.append_script_list_to_db(question_id, script_list, prompt_list)
# fb 초기화하고
# 미리 정의된 질문을 읽어서
# 이에 대한 script 와 prompt 를 생성하고
# 이 정보를 db 에 저장한다. ( 그리고 여기서 나온 카테고리 정보도 저장한다. )