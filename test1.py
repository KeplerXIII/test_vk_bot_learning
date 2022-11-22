from dotenv import load_dotenv
import os
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from threading import Thread
from pprint import pprint

user_dict = {}

load_dotenv()

vk_group_session = vk_api.VkApi(token=os.getenv('GROUP_TOKEN'))
vk_user_session = vk_api.VkApi(token=os.getenv('USER_TOKEN'))
vk_group = vk_group_session.get_api()
vk_user = vk_user_session.get_api()
longpoll = VkBotLongPoll(vk_group_session, group_id=os.getenv('GROUP_ID'))


def preview_photos(user_photo_list: list) -> list:
    preview_photo_list = [
        {'photo_id': photo['id'], 'likes': photo['likes']['count'],
         'photo_link': [sizes['url'] for sizes in photo['sizes']][-1]}
        for photo in user_photo_list["items"]]
    preview_photo_list.sort(key=lambda dictionary: dictionary['likes'])
    link_list = [[link['photo_id'], link['likes'], link['photo_link']] for link in preview_photo_list[-3:]]
    return link_list


def get_photo(found_user_id: int) -> list:
    photo_list = vk_user.photos.get(owner_id=found_user_id, album_id="profile", extended=1)
    return photo_list


def send_message(session, vk_id: int, text: str, attachment=None, keyboard=None) -> None:
    session.method('messages.send',
                   {'user_id': vk_id, 'message': text, 'random_id': 0, 'keyboard': keyboard, 'attachment': attachment})


def listener(self_id):
    found_user = vk_user.users.search(count=100, sex='1', fields="city, bdate, sex")
    for user in found_user['items']:
        user_photo_list = vk_user.photos.get(owner_id=user["id"], album_id="profile", extended=1)
        if user_photo_list['count'] > 2:
            user_photos = preview_photos(user_photo_list)
            pprint(user_photos)
            send_message(vk_group_session, self_id, f'{user["first_name"]} {user["last_name"]}\n'
                                                    f'https://vk.com/id{user["id"]}\n',
                         f'photo{user["id"]}_{user_photos[0][0]},'
                         f'photo{user["id"]}_{user_photos[1][0]},'
                         f'photo{user["id"]}_{user_photos[2][0]}')
        else:
            send_message(vk_group_session, self_id, "ищем...")
            continue

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if self_id == event.obj.message["from_id"]:
                    if event.obj.message["text"].lower() == "дальше":
                        send_message(vk_group_session, event.obj.message["from_id"], text="ожидай...")
                        break

                    elif event.obj.message["text"] == "выход":
                        send_message(vk_group_session, event.obj.message["from_id"], text="выходим")
                        user_dict[event.obj.message["from_id"]] = 1
                        break


def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:

            if event.obj.message["from_id"] not in user_dict:
                user_dict[event.obj.message["from_id"]] = 1
                pass

            if event.obj.message["text"] == "я" and user_dict[event.obj.message["from_id"]] == 1:
                self_id = event.obj.message["from_id"]
                send_message(vk_group_session, event.obj.message["from_id"], text=self_id)

            elif event.obj.message["text"] == "начать" and user_dict[event.obj.message["from_id"]] == 1:
                self_id = event.obj.message["from_id"]
                send_message(vk_group_session, event.obj.message["from_id"], text="вошли в поиск")
                user_dict[event.obj.message["from_id"]] = 2
                inner_listen = Thread(target=listener, args=(self_id,))
                inner_listen.start()

            else:
                if user_dict[event.obj.message["from_id"]] == 1:
                    send_message(vk_group_session, event.obj.message["from_id"], text="неизвестно")


if __name__ == "__main__":
    main()
