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

    def append_script_list_to_db(self, question_id, script_list, prompt_list):
        for script, prompt in zip(script_list, prompt_list):
            self.append_script_to_db(question_id, script, prompt)

    def append_script_to_db(self, question_id, script, prompt):
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
            'script': script,
            'prompt': prompt,
            'image_path': image_path,
            #3d/0234_6_4
        }

        #ref.push(new_data)
        self.ref_script.child(str(new_id)).set(new_data)

        print(f"Script added to script_db")

    def test(self):
        self.append_script_list_to_db(0, ["script1", "script2"], ["prompt1", "prompt2"])
