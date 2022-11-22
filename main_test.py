import asyncio
from dotenv import load_dotenv
import os
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
load_dotenv()
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from vk.vk import send_message
from pprint import pprint
from threading import Thread
from database.database import User

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    stage = sq.Column(sq.Integer)


vk_group_session = vk_api.VkApi(token=os.getenv('GROUP_TOKEN'))
vk_user_session = vk_api.VkApi(token=os.getenv('USER_TOKEN'))
vk_group = vk_group_session.get_api()
vk_user = vk_user_session.get_api()
longpoll = VkBotLongPoll(vk_group_session, group_id=os.getenv('GROUP_ID'))

user_dict = {}


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
    engine = sq.create_engine(os.getenv('DSN'))
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print(f'Для меня от: {event.obj.message["from_id"]}')
            print('Текст:', event.obj.message["text"])



            if event.obj.message["from_id"] not in user_dict:
                user = User(vk_id=event.obj.message["from_id"], stage=1)
                session.add(user)
                session.commit()
                request = session.query(User).filter_by(vk_id=event.obj.message["from_id"]).one()
                user_dict[request.vk_id] = request.stage
                print(request.stage)
                print(user_dict)


            if event.obj.message["text"] == "привет" and request.stage == 1:
                vk_group_session.method('messages.send',
                                        {'user_id': event.obj.message["from_id"], 'message': "привет",
                                         'random_id': 0,
                                         'keyboard': None, 'attachment': None})
            elif event.obj.message["text"] == "пока" and request.stage == 1:
                vk_group_session.method('messages.send',
                                        {'user_id': event.obj.message["from_id"], 'message': "пока", 'random_id': 0,
                                         'keyboard': None, 'attachment': None})
            elif event.obj.message["text"] == "я" and request.stage == 1:
                self_id = event.obj.message["from_id"]
                vk_group_session.method('messages.send',
                                        {'user_id': event.obj.message["from_id"], 'message': f'твой ID: {self_id}',
                                         'random_id': 0,
                                         'keyboard': None, 'attachment': None})

            elif event.obj.message["text"] == "найти кандидата" and request.stage == 1:
                vk_group_session.method('messages.send',
                                        {'user_id': event.obj.message["from_id"], 'message': "нашли, но не покажем",
                                         'random_id': 0,
                                         'keyboard': None, 'attachment': None})

            elif event.obj.message['text'] == "логика" and user_dict[event.obj.message["from_id"]] == 1:
                self_id = event.obj.message["from_id"]
                vk_group_session.method('messages.send',
                                        {'user_id': event.obj.message["from_id"], 'message': "вошли в логику",
                                         'random_id': 0,
                                         'keyboard': None, 'attachment': None})
                request = session.query(User).filter(user.vk_id == self_id).one()
                request.stage = 2
                session.commit()
                user_dict[event.obj.message["from_id"]] = 2
                test_thread = Thread(target=listener, args=(self_id,))
                test_thread.start()
                # test_thread.join()



                # for event in longpoll.listen():
                #     if event.type == VkBotEventType.MESSAGE_NEW:
                #         if self_id == event.obj.message["from_id"]:
                #             if event.obj.message["text"] == "да":
                #                 send_message(vk_group_session, event.obj.message["from_id"], text="да")
                #
                #             else:
                #                 send_message(vk_group_session, event.obj.message["from_id"], text="нет")
                #                 # break




if __name__ == "__main__":

    main()
