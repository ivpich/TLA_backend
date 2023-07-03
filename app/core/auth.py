from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from app.config import SECRET_KEY

s = Serializer(SECRET_KEY)


def create_init_data(chat_id: int):
    return s.dumps({'chat_id': chat_id}).decode()


def verify_init_data(init_data: str):
    try:
        data = s.loads(init_data)
    except SignatureExpired:
        return None  # valid init_data, but expired
    except BadSignature:
        return None  # invalid init_data
    return data['chat_id']
