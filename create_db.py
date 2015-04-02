from apps.chat.models import create_chat_models
from apps.registration.models import create_user


if __name__ == '__main__':
    create_user()
    create_chat_models()
