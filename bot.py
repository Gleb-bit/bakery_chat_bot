#!/usr/bin/env python3
import random
from io import BytesIO

import PIL.Image
import requests

import handlers
from settings import DEFAULT_ANSWER
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import models
from models import UserState

import settings

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class Bot:
    """
    Echo bot for vk.com

    Use python 3.9
    """

    def __init__(self, group_id, token):
        """
        :param group_id: group id из группы vk
        :param token: секретный токен
        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)  # объект vk_api для longpoll
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)  # создание longpoll
        self.api = self.vk.get_api()

    def run(self):
        """Запуск бота."""
        for event in self.long_poller.listen():  # принимаем события
            try:
                self.on_event(event)
            except Exception as exc:
                print(exc, type(exc), exc.args)

    def on_event(self, event):
        """
        Отправляет сообщение назад, если это текст.

        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type != VkBotEventType.MESSAGE_NEW:
            return
        user_id = event.message.peer_id
        text = event.message.text
        try:
            state = UserState.get(user_id=str(user_id))
        except models.UserState.DoesNotExist:
            # search intent
            for intent in settings.INTENTS:
                if any(token in text.lower() for token in intent['tokens']):
                    if intent['answer']:
                        self.send_text(intent['answer'], user_id)
                    else:
                        self.start_scenario(user_id)
                    break
            else:
                self.send_text(settings.DEFAULT_ANSWER, user_id)
        else:
            self.continue_scenario(text, state, user_id)

    def send_text(self, text_to_send, user_id, keyboard=None):
        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id,
            keyboard=keyboard.get_keyboard() if isinstance(keyboard, VkKeyboard) else None
        )

    def send_image(self, reply, user_id):
        description = reply[0]
        bytes_image = reply[1]
        with open('pic.jpg', "wb") as file:
            file.write(bytes_image)
        base = PIL.Image.open('pic.jpg').convert('RGBA')
        temp_file = BytesIO()
        base.save(temp_file, 'png')
        temp_file.seek(0)
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        upload_data = requests.post(url=upload_url, files={'photo': ('pic.jpg', temp_file, 'image/jpg')}).json()
        image_data = self.api.photos.saveMessagesPhoto(**upload_data)
        owner_id = image_data[0]['owner_id']
        media_id = image_data[0]['id']
        attachment = f'photo{owner_id}_{media_id}'
        self.api.messages.send(
            attachment=attachment,
            message=description,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id,
        )

    def send_step(self, step, user_id, reply):
        if 'text' in step:
            self.send_text(step['text'].format(), user_id, keyboard=reply)
        if 'image' in step:
            self.send_image(reply, user_id)

    def start_scenario(self, user_id, text=''):
        first_step = settings.SCENARIOS['first_step']
        step = settings.SCENARIOS['steps'][first_step]
        keyboard = self.get_reply(text=text, step=step)
        self.send_text(step['text'], user_id, keyboard=keyboard)
        state = UserState(user_id=str(user_id), text=text, step_name=step['next_step'],
                          keyboard=keyboard)
        state.save()

    def continue_scenario(self, text, state, user_id):
        steps = settings.SCENARIOS['steps']
        step = steps[int(state.step_name)]
        reply = self.get_reply(text=text, step=step)
        if reply:
            # next_step
            self.send_step(step, user_id, reply)

            if step['next_step']:
                # switch to next step
                state.step_name = step['next_step']
                state.text = text
                if isinstance(reply, VkKeyboard):
                    state.keyboard = reply
                state.save()
        else:
            back_or_to_the_main = self.back_or_to_the_main(text, state)
            if back_or_to_the_main:
                text_to_send = back_or_to_the_main
                reply = state.keyboard
            # retry current step
            else:
                text_to_send = DEFAULT_ANSWER.format()
            self.send_text(text_to_send, user_id, reply)

    def back_or_to_the_main(self, text, state):
        text_to_send = None
        if text == 'Вернуться на главную':
            state.step_name = 2
            state.keyboard = self.get_reply(state.text)
            text_to_send = settings.BACK_TO_MAIN_ANSWER
        elif text == 'Назад':
            state.step_name = int(state.step_name) - 2
            steps = settings.SCENARIOS['steps']
            step = steps[state.step_name]
            state.keyboard = self.get_reply(text=state.text, step=step)
            text_to_send = settings.BACK_ANSWER
        state.save()
        return text_to_send

    def get_reply(self, text, step=None):
        handler = getattr(handlers, step['handler'] if step else 'handle_first_keyboard')
        reply = handler(text=text)
        return reply


if __name__ == "__main__":
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()
