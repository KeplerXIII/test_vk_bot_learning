def send_message(session, vk_id: int, text: str) -> None:
    session.method('messages.send', {'user_id': vk_id, 'message': text, 'random_id': 0, 'keyboard': None, 'attachment': None})