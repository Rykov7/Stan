import logging
from unittest import IsolatedAsyncioTestCase, main
import os

from telebot import asyncio_helper, types, logger

# Надо сделать до импорта бота, иначе упадет по токену
os.environ["LUTZPYBOT"] = "00000:AAAAAAAAAAAA"
from src import helpers

# нужно не дать делать реальные запросы в тестах, конкретно тут -за Правилами чата
helpers.is_url_reachable = lambda a: True
from src.commands import bot

# отключаем логи бота, в тестах они не нужны
logger.setLevel(logging.ERROR)


def get_update(text, reply_to=None):
    params = {'text': text}
    chat = types.Chat(id=11, type='private')
    user = types.User(id=10, is_bot=False, first_name='Some User')
    if reply_to:
        params["reply_to_message"] = types.Message(message_id=1, from_user=user, date=None, chat=chat,
                                                   content_type='text', options={'text': reply_to}, json_string="")
    mess = types.Message(message_id=1, from_user=user, date=None, chat=chat, content_type='text', options=params,
                         json_string="")
    edited_message = None
    channel_post = None
    edited_channel_post = None
    inline_query = None
    chosen_inline_result = None
    callback_query = None
    shipping_query = None
    pre_checkout_query = None
    poll = None
    poll_answer = None
    my_chat_member = None
    chat_member = None
    chat_join_request = None
    return types.Update(1001234038283, mess, edited_message, channel_post, edited_channel_post, inline_query,
                        chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer,
                        my_chat_member, chat_member, chat_join_request)

# сюда будут складываться результаты, перед началом теста очищается
RESULTS = []


async def custom_sender(token, url, method='get', params=None, files=None, **kwargs):
    RESULTS.append(params)
    result = {"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}}
    return result

# Чтобы перехватить запросы к телеге
asyncio_helper._process_request = custom_sender


class TestBot(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.bot = bot
        RESULTS.clear()

    async def test_start(self):
        await self.bot.process_new_updates([get_update('/start')])
        self.assertEqual(RESULTS[0]['text'], "Начни с прочтения")

    async def test_non_grata(self):
        await self.bot.process_new_updates([get_update('как вам дударь?')])
        self.assertEqual(RESULTS[0]['text'], "у нас тут таких не любят")

    async def test_non_grata2(self):
        await self.bot.process_new_updates([get_update('смотрю хауди')])
        self.assertEqual(RESULTS[0]['text'], "у нас тут таких не любят")

    async def test_rules(self):
        await self.bot.process_new_updates([get_update('/rules')])
        self.assertEqual(RESULTS[0]['text'], "Читай...")
        self.assertTrue("https://telegra.ph/pythonchatru-07-07" in RESULTS[0]['reply_markup'])

    async def test_faq(self):
        await self.bot.process_new_updates([get_update('/faq')])
        self.assertEqual(RESULTS[0]['text'], "Читай...")
        self.assertTrue("https://telegra.ph/faq-10-07-4" in RESULTS[0]['reply_markup'])

    async def test_lib(self):
        await self.bot.process_new_updates([get_update('/lib')])
        self.assertEqual(RESULTS[0]['text'], "Читай...")
        self.assertTrue("https://telegra.ph/what-to-read-10-06" in RESULTS[0]['reply_markup'])

    async def test_tr(self):
        await self.bot.process_new_updates([get_update('/tr', reply_to="ghbdtn")])
        self.assertEqual(RESULTS[0]['text'], "привет")

    async def test_tr2(self):
        await self.bot.process_new_updates([get_update('/tr', reply_to="руддщ")])
        self.assertEqual(RESULTS[0]['text'], "hello")

    async def test_tsya(self):
        await self.bot.process_new_updates([get_update('/tsya')])
        self.assertEqual(RESULTS[0]['text'], "<i>-тся</i> и <i>-ться</i> в глаголах")
        self.assertTrue("https://tsya.ru/" in RESULTS[0]['reply_markup'])

    async def test_nometa(self):
        text = """Не задавай мета-вопросов вроде:\n<i>  «Можно задать вопрос?»\n  «Кто-нибудь пользовался .. ?»\n  «Привет, мне нужна помощь по .. !»</i>\n\nПросто спроси сразу! И чем лучше объяснишь проблему, тем вероятнее получишь помощь."""
        await self.bot.process_new_updates([get_update('/nometa', reply_to="кто тут питонист?")])
        self.assertEqual(RESULTS[0]['text'], text)

    async def test_neprivet(self):
        await self.bot.process_new_updates([get_update('/neprivet', reply_to="привет всем")])
        self.assertEqual(RESULTS[0]['text'], "Пожалуйста, не пишите просто «Привет» в чате.")
        self.assertTrue("https://neprivet.com/" in RESULTS[0]['reply_markup'])

    async def test_nojob(self):
        text = """Мы здесь не для того, чтобы за тебя решать задачи.\n\nЗдесь помогают по конкретным вопросам в <u>ТВОЁМ</u> коде, поэтому тебе нужно показать код, который ты написал сам и объяснить где и почему застрял... всё просто. 🤷🏼️"""
        await self.bot.process_new_updates([get_update('/nojob', reply_to="есть работа")])
        self.assertEqual(RESULTS[0]['text'], text)

    async def test_nobot(self):
        text = """<b>Внимание</b>:\nТелеграм бот <i>не должен</i> быть твоим первым проектом на Python. Пожалуйста, изучи <code>основы Python</code>, <code>работу с модулями</code>, <code>основы веб-технологий</code>, <code>асинхронное программирование</code> и <code>отладку</code> до начала работы с Телеграм ботами. Существует много ресурсов для этого в интернете."""
        await self.bot.process_new_updates([get_update('/nobot', reply_to="как бота написать?")])
        self.assertEqual(RESULTS[0]['text'], text)

    async def test_nogui(self):
        text = """<b>Внимание</b>:\nGUI приложение <i>не должно</i> быть твоим первым проектом на Python. Пожалуйста, изучи <code>основы Python</code>, <code>работу с модулями</code>, <code>циклы событий</code> и <code>отладку</code> до начала работы с какими-либо GUI-фреймворками. Существует много ресурсов для этого в интернете."""
        await self.bot.process_new_updates([get_update('/nogui', reply_to="как gui написать?")])
        self.assertEqual(RESULTS[0]['text'], text)


if __name__ == '__main__':
    main()
