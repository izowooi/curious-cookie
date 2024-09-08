import os.path
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from dotenv import load_dotenv


def main():
    load_dotenv()

    firebase_admin_key = os.getenv('FIREBASE_ADMIN_KEY')
    firebase_db_url = os.getenv('FIREBASE_DB_URL')

    cred = credentials.Certificate(firebase_admin_key)

    firebase_admin.initialize_app(cred, {
        'databaseURL': firebase_db_url
    })

    ref = db.reference('/question_db')
    data = ref.get()

    print(f"Data : {data}")


if __name__ == "__main__":
    main()