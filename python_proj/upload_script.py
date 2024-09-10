import os.path
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from dotenv import load_dotenv


class FBManger:
    def __init__(self, firebase_admin_key, firebase_db_url):
        cred = credentials.Certificate(firebase_admin_key)

        firebase_admin.initialize_app(cred, {
            'databaseURL': firebase_db_url
        })

        self.ref_question = db.reference('/question_db')
        self.ref_script = db.reference('/script_db')

    def set_processed_question(self, question_id):
        question_db = self.ref_question.get()
        if question_db is not None:
            for data in question_db:
                if data['id'] == question_id:
                    data['generated'] = 'true'
                    question_db[data['id']] = data
                    break

        self.ref_question.set(question_db)

    def get_unprocessed_questions_from_db(self):
        ret = {}
        question_db = self.ref_question.get()
        if question_db is not None:
            for data in question_db:
                if data['generated'] == 'true' or data['generated'] == 'True':
                    continue
                ret[data['id']] = data['question']
        return ret

    def append_script_list_to_db(self, question_id, script_dict, prompt_list):
        # 각 언어별 스크립트 리스트를 가져오기
        script_kr_list = script_dict.get("kr", [])
        script_en_list = script_dict.get("en", [])
        script_cn_list = script_dict.get("cn", [])
        script_ar_list = script_dict.get("ar", [])
        script_jp_list = script_dict.get("jp", [])

        # zip을 사용하여 각 언어별 스크립트와 프롬프트를 반복
        for script_kr, script_en, script_cn, script_ar, script_jp, prompt in zip(script_kr_list, script_en_list,
                                                                                 script_cn_list, script_ar_list,
                                                                                 script_jp_list, prompt_list):
            # append_script_to_db 함수 호출 시 각 언어별 스크립트를 인자로 전달
            self.append_script_to_db(question_id, script_kr, script_en, script_cn, script_ar, script_jp, prompt)

    def append_script_to_db(self, question_id, script_kr, script_en, script_cn, script_ar, script_jp, prompt):
        script_db = self.ref_script.get()
        new_id = 0
        if script_db is None:
            # 값이 없으면 초기화
            self.ref_script.set({})
        else:
            last_id = 0
            for data in script_db:
                if data['id'] > last_id:
                    last_id = data['id']
            new_id = last_id + 1

        image_style = "3d"#2d, reality
        img_index = 0
        script_seq = 0

        # 포맷팅된 값을 사용하여 image_path 생성
        formatted_question_id = f'{question_id:04d}'
        formatted_script_seq = f'{script_seq:02d}'
        formatted_img_index = f'{img_index:01d}'
        image_path = f'{image_style}/{formatted_question_id}_{formatted_script_seq}_{image_style}_{formatted_img_index}.png'

        new_data = {
            'id': new_id,
            'question_id': question_id,
            'script_kr': script_kr,
            'script_en': script_en,
            'script_cn': script_cn,
            'script_ar': script_ar,
            'script_jp': script_jp,
            'prompt': prompt,
            'image_path': image_path,
            #3d/0234_6_4
        }

        #ref.push(new_data)
        self.ref_script.child(str(new_id)).set(new_data)

        print(f"Script added to script_db")

    def test(self):
        self.append_script_list_to_db(0, ["script1", "script2"], ["prompt1", "prompt2"])
