from dotenv import load_dotenv
import os
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from threading import Thread

user_dict = {}

load_dotenv()

vk_group_session = vk_api.VkApi(token=os.getenv('GROUP_TOKEN'))
vk_user_session = vk_api.VkApi(token=os.getenv('USER_TOKEN'))
vk_group = vk_group_session.get_api()
vk_user = vk_user_session.get_api()
longpoll = VkBotLongPoll(vk_group_session, group_id=os.getenv('GROUP_ID'))

def send_message(session, vk_id: int, text: str) -> None:
    session.method('messages.send', {'user_id': vk_id, 'message': text, 'random_id': 0, 'keyboard': None, 'attachment': None})

def listener(self_id):
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if self_id == event.obj.message["from_id"]:
                if event.obj.message["text"] == "да":
                    send_message(vk_group_session, event.obj.message["from_id"], text="да")

                elif event.obj.message["text"] == "выход":
                    send_message(vk_group_session, event.obj.message["from_id"], text="выходим")
                    user_dict[event.obj.message["from_id"]] = 1
                    break

def main():

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:

            if event.obj.message["from_id"] not in user_dict:
                user_dict[event.obj.message["from_id"]] = 1
                print(user_dict)

            elif event.obj.message["text"] == "я" and user_dict[event.obj.message["from_id"]] == 1:
                self_id = event.obj.message["from_id"]
                send_message(vk_group_session, event.obj.message["from_id"], text=self_id)

            elif event.obj.message["text"] == "логика" and user_dict[event.obj.message["from_id"]] == 1:
                send_message(vk_group_session, event.obj.message["from_id"], text="вошли в логику")
                user_dict[event.obj.message["from_id"]] = 2
                inner_listen = Thread(target=listener, args=(self_id,))
                inner_listen.start()

            else:
                if user_dict[event.obj.message["from_id"]] == 1:
                    send_message(vk_group_session, event.obj.message["from_id"], text="неизвестно")

if __name__ == "__main__":
    main()