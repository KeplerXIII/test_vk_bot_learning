from dotenv import load_dotenv
import os
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from vk.vk import send_message
from pprint import pprint

Base = declarative_base()
load_dotenv()
engine = sq.create_engine(os.getenv("DSN"))
Base.metadata.drop_all(engine) # дропаем
Base.metadata.create_all(engine) # создаём
Session = sessionmaker(bind=engine)
session = Session()

def main():
    vk_group_session = vk_api.VkApi(token=os.getenv('GROUP_TOKEN'))
    vk_user_session = vk_api.VkApi(token=os.getenv('USER_TOKEN'))
    vk_group = vk_group_session.get_api()
    vk_user = vk_user_session.get_api()
    longpoll = VkBotLongPoll(vk_group_session, group_id=os.getenv('GROUP_ID'))

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            self_id = event.obj.message["from_id"]
            print(f'Для меня от: {event.obj.message["from_id"]}')
            print('Текст:', event.obj.message["text"])
            if event.obj.message["text"] == "привет":
                vk_group_session.method('messages.send',
                                  {'user_id': event.obj.message["from_id"], 'message': "привет", 'random_id': 0,
                                   'keyboard': None, 'attachment': None})
            if event.obj.message["text"] == "пока":
                vk_group_session.method('messages.send',
                                  {'user_id': event.obj.message["from_id"], 'message': "пока", 'random_id': 0,
                                   'keyboard': None, 'attachment': None})
            if event.obj.message["text"] == "я":
                vk_group_session.method('messages.send',
                                  {'user_id': event.obj.message["from_id"], 'message': f'твой ID: {self_id}', 'random_id': 0,
                                   'keyboard': None, 'attachment': None})

            if event.obj.message["text"] == "найти кандидата":

                request = vk_user.users.search(count=1, sex='1', has_photo='1', status='6', fields="city, bdate, sex")
                vk_group_session.method('messages.send',
                                        {'user_id': event.obj.message["from_id"], 'message': "нашли, но не покажем", 'random_id': 0,
                                         'keyboard': None, 'attachment': None})

            if event.obj.message['text'] == "логика":
                vk_group_session.method('messages.send',
                                        {'user_id': event.obj.message["from_id"], 'message': "вошли в логику",
                                         'random_id': 0,
                                         'keyboard': None, 'attachment': None})
                for event in longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        if self_id == event.obj.message["from_id"]:
                            if event.obj.message["text"] == "да":
                                send_message(vk_group_session, event.obj.message["from_id"], text="да")

                            else:
                                send_message(vk_group_session, event.obj.message["from_id"], text="нет")
                                break

            else:
                send_message(vk_group_session, event.obj.message["from_id"], text="неизвестно")



        elif event.type == VkBotEventType.MESSAGE_REPLY:
            print('Новое сообщение:')

            print('От меня для: ', end='')

            print(event.obj.peer_id)

            print('Текст:', event.obj.text)
            print()

        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            print('Печатает ', end='')

            print(event.obj.from_id, end=' ')

            print('для ', end='')

            print(event.obj.to_id)
            print()

        elif event.type == VkBotEventType.GROUP_JOIN:
            print(event.obj.user_id, end=' ')

            print('Вступил в группу!')
            print()

        elif event.type == VkBotEventType.GROUP_LEAVE:
            print(event.obj.user_id, end=' ')

            print('Покинул группу!')
            print()

        else:
            print(event.type)
            print()

session.close()

if __name__ == '__main__':
    main()
