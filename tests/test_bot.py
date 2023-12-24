import logging
from unittest import IsolatedAsyncioTestCase, main, TestCase
import os
from unittest.mock import patch, MagicMock

from telebot import asyncio_helper, types, logger

# Надо сделать до импорта бота, иначе упадет, так как нет енва в тестах
os.environ["LUTZPYBOT"] = "00000:AAAAAAAAAAAA"
os.environ["whiteids"] = "100,200,300"
os.environ["rollback"] = "1,2,3"
os.environ["use_reminder"] = "FALSE"

from src import helpers

# нужно не дать делать реальные запросы в тестах, конкретно тут -за Правилами чата
helpers.is_url_reachable = lambda a: True
from src.commands import bot
from src.constants import BDMTSS_ID, LUTZ_ID, ADMIN_ID
from src.filters import is_white_id

# отключаем логи бота, в тестах они не нужны
logger.setLevel(logging.ERROR)

# сюда будут складываться результаты, перед началом теста очищается
RESULTS = []


def _all_nones():
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
    return (edited_message, channel_post, edited_channel_post, inline_query, chosen_inline_result, callback_query,
            shipping_query, pre_checkout_query, poll, poll_answer, my_chat_member, chat_member, chat_join_request)


def get_update(text, reply_to=None, user_id=10):
    """Хелпер, генерирующий событие обновления для бота"""
    params = {'text': text}
    chat = types.Chat(id=11, type='group')
    user = types.User(id=user_id, is_bot=False, first_name='Some User')
    if reply_to:
        params["reply_to_message"] = types.Message(message_id=2, from_user=user, date=None, chat=chat,
                                                   content_type='text', options={'text': reply_to}, json_string="")
    mess = types.Message(message_id=1, from_user=user, date=None, chat=chat, content_type='text', options=params,
                         json_string='')
    return types.Update(1001234038283, mess, *_all_nones())


def member(leave: bool = False):
    """Хелпер, генерирующий событие входа и выхода юзера"""
    type_ = 'left_chat_member' if leave else 'new_chat_members'
    chat = types.Chat(id=11, type='group')
    params = {'content_type': type_}
    user = types.User(id=555, is_bot=False, first_name='Some User')
    mess = types.Message(message_id=1, from_user=user, date=None, chat=chat, content_type=type_,
                         options=params, json_string='')
    return types.Update(100100, mess, *_all_nones())


async def custom_sender(token, url, method='get', params=None, files=None, **kwargs):
    """Замена для тестов, чтобы не слать запросы в телегу"""
    RESULTS.append((params, url))
    chat = {"id": 1000, "type": "group", "bio": "bio",
            "photo": {"big_file_id": "file_id", "small_file_id": "file_id", "small_file_unique_id": "file_id",
                      "big_file_unique_id": "file_id"}}
    result = {"message_id": 1000, "date": 1, "chat": chat}
    if url == "getChat":
        result = chat
    return result


# Чтобы перехватить запросы к телеге
asyncio_helper._process_request = custom_sender


class TestOther(TestCase):
    def test_is_white(self):
        params = (
            (False, 1),
            (False, 10),
            (True, 100),
            (True, 200),
            (True, 300),
        )
        for expected, text in params:
            with self.subTest(f"check non-is_white_id({text})"):
                m = MagicMock(from_user=MagicMock(id=text))
                self.assertEqual(is_white_id(m), expected)


class TestBot(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.bot = bot
        RESULTS.clear()

    async def test_start(self):
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/start')])
            self.assertEqual(RESULTS[0][0]['text'], "Начни с прочтения")

    async def test_non_grata(self):
        await self.bot.process_new_updates([get_update('как вам дударь?')])
        self.assertEqual(RESULTS[0][0]['text'], "у нас тут таких не любят")

    async def test_non_grata2(self):
        await self.bot.process_new_updates([get_update('смотрю хауди')])
        self.assertEqual(RESULTS[0][0]['text'], "у нас тут таких не любят")

    async def test_rules(self):
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/rules')])
            self.assertEqual(RESULTS[0][0]['text'], "Читай...")
            self.assertTrue("https://telegra.ph/pythonchatru-07-07" in RESULTS[0][0]['reply_markup'])

    async def test_faq(self):
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/faq')])
            self.assertEqual(RESULTS[0][0]['text'], "Читай...")
            self.assertTrue("https://telegra.ph/faq-10-07-4" in RESULTS[0][0]['reply_markup'])

    async def test_lib(self):
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/lib')])
            self.assertEqual(RESULTS[0][0]['text'], "Читай...")
            self.assertTrue("https://telegra.ph/what-to-read-10-06" in RESULTS[0][0]['reply_markup'])

    async def test_tr(self):
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/tr', reply_to="ghbdtn")])
            self.assertEqual(RESULTS[0][0]['text'], "привет")

    async def test_tr2(self):
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/tr', reply_to="руддщ")])
            self.assertEqual(RESULTS[0][0]['text'], "hello")

    async def test_tsya(self):
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/tsya')])
            self.assertEqual(RESULTS[0][0]['text'], "<i>-тся</i> и <i>-ться</i> в глаголах")
            self.assertTrue("https://tsya.ru/" in RESULTS[0][0]['reply_markup'])

    async def test_nometa(self):
        text = """Не задавай мета-вопросов вроде:\n<i>  «Можно задать вопрос?»\n  «Кто-нибудь пользовался .. ?»\n  «Привет, мне нужна помощь по .. !»</i>\n\nПросто спроси сразу! И чем лучше объяснишь проблему, тем вероятнее получишь помощь."""
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/nometa', reply_to="кто тут питонист?")])
            self.assertEqual(RESULTS[0][0]['text'], text)

    async def test_neprivet(self):
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/neprivet', reply_to="привет всем")])
            self.assertEqual(RESULTS[0][0]['text'], "Пожалуйста, не пишите просто «Привет» в чате.")
            self.assertTrue("https://neprivet.com/" in RESULTS[0][0]['reply_markup'])

    async def test_lutz(self):
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/lutz', reply_to="привет всем")])
            self.assertEqual(RESULTS[0][0]['caption'], "вот, не позорься")
            self.assertEqual(RESULTS[0][0]['document'], LUTZ_ID)
            self.assertEqual(RESULTS[0][1], "sendDocument")
            self.assertEqual(RESULTS[1][1], "deleteMessage")

    async def test_bdmtss(self):
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/bdmtss', reply_to="привет всем")])
            self.assertEqual(RESULTS[0][0]['voice'], BDMTSS_ID)
            self.assertEqual(RESULTS[0][1], "sendVoice")
            self.assertEqual(RESULTS[1][1], "deleteMessage")

    async def test_google(self):
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/g', reply_to="python")])
            self.assertEqual(RESULTS[0][0]['text'], "<i>Ищем «<i>python</i>»...</i>")
            self.assertTrue("https://www.google.com/search?q=python" in RESULTS[0][0]['reply_markup'])

    async def test_nojob(self):
        text = """Мы здесь не для того, чтобы за тебя решать задачи.\n\nЗдесь помогают по конкретным вопросам в <u>ТВОЁМ</u> коде, поэтому тебе нужно показать код, который ты написал сам и объяснить где и почему застрял... всё просто. 🤷🏼️"""
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/nojob', reply_to="есть работа")])
            self.assertEqual(RESULTS[0][0]['text'], text)

    async def test_nobot(self):
        text = """<b>Внимание</b>:\nТелеграм бот <i>не должен</i> быть твоим первым проектом на Python. Пожалуйста, изучи <code>основы Python</code>, <code>работу с модулями</code>, <code>основы веб-технологий</code>, <code>асинхронное программирование</code> и <code>отладку</code> до начала работы с Телеграм ботами. Существует много ресурсов для этого в интернете."""
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/nobot', reply_to="как бота написать?")])
            self.assertEqual(RESULTS[0][0]['text'], text)

    async def test_nogui(self):
        text = """<b>Внимание</b>:\nGUI приложение <i>не должно</i> быть твоим первым проектом на Python. Пожалуйста, изучи <code>основы Python</code>, <code>работу с модулями</code>, <code>циклы событий</code> и <code>отладку</code> до начала работы с какими-либо GUI-фреймворками. Существует много ресурсов для этого в интернете."""
        # Нужно пропустить проверку на спам
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/nogui', reply_to="как gui написать?")])
            self.assertEqual(RESULTS[0][0]['text'], text)

    async def test_spam_text(self):
        # Нужно подставить антиспам вкл.
        with patch("src.filters.is_antispam_enabled") as mocked:
            # Нужно подменить инкремент, нельзя реально в шелве работать в тестах
            with patch("src.commands.increment") as _mocked_shelve:
                mocked.return_value = True
                await self.bot.process_new_updates([get_update('пишите мне в ЛС, Писать в ЛС')])
                self.assertEqual(RESULTS[0][1], "deleteMessage")
                self.assertEqual(RESULTS[1][1], "banChatMember")
                self.assertEqual(RESULTS[1][0], {'chat_id': 11, 'user_id': 10, 'until_date': None})

    async def test_wrong_url(self):
        # Нужно подставить антиспам вкл.
        with patch("src.filters.is_antispam_enabled") as mocked:
            # Нужно подменить инкремент, нельзя реально в шелве работать в тестах
            with patch("src.commands.increment") as _mocked_shelve:
                mocked.return_value = True
                await self.bot.process_new_updates([get_update('тут подробнее https://zvuk.com/artist/61375')])
                self.assertEqual(RESULTS[0][1], "deleteMessage")
                self.assertEqual(RESULTS[0][0], {'chat_id': 11, 'message_id': 1})

    async def test_update_stats(self):
        # Нужно подставить антиспам вкл.
        with patch("src.filters.is_antispam_enabled") as mocked:
            # Нужно подменить инкремент, нельзя реально в шелве работать в тестах
            with patch("src.commands.increment") as _mocked_shelve:
                # Подменяем обновление статистики, нам важно что оно просто было вызвано
                with patch("src.commands.update_stats") as update_stats:
                    mocked.return_value = True
                    update_stats.side_effect = lambda x: RESULTS.append(x)
                    await self.bot.process_new_updates([get_update('просто текст')])
                    self.assertEqual(RESULTS[0].text, "просто текст")

    async def test_admin_can_delete(self):
        # Нужно подставить антиспам вкл.
        with patch("src.filters.is_antispam_enabled") as mocked:
            mocked.return_value = True
            await self.bot.process_new_updates([get_update('/ddel', reply_to="shit text", user_id=ADMIN_ID)])
            self.assertEqual(RESULTS[0], ({'chat_id': 11, 'message_id': 1}, 'deleteMessage'))
            self.assertEqual(RESULTS[1], ({'chat_id': 11, 'message_id': 2}, 'deleteMessage'))

    async def test_user_cant(self):
        for command in ('/ddel', '/bban', '/unban_id', '/unban_id 1', '/add', '/remove'):
            with self.subTest(f"user cant use {command}"):
                # Нужно подставить антиспам вкл.
                with patch("src.filters.is_antispam_enabled") as mocked:
                    # Нужно подменить инкремент, нельзя реально в шелве работать в тестах
                    with patch("src.commands.increment") as _mocked_shelve:
                        # Подменяем обновление статистики, нам важно что оно просто было вызвано
                        with patch("src.commands.update_stats") as update_stats:
                            # Подменяем speak, чтобы Стен не начал отвечать
                            with patch("src.stan.speak") as speak:
                                speak.return_value = None
                                mocked.return_value = True
                                update_stats.side_effect = lambda x: None
                                await self.bot.process_new_updates([get_update(command, reply_to="shit text")])
                                self.assertEqual(RESULTS, [])

    async def test_admin_can_ban(self):
        # Нужно подставить антиспам вкл.
        with patch("src.filters.is_antispam_enabled") as mocked:
            # Нужно подменить инкремент, нельзя реально в шелве работать в тестах
            with patch("src.commands.increment") as _mocked_shelve:
                # Подменяем обновление статистики, нам важно что оно просто было вызвано
                with patch("src.commands.update_stats") as update_stats:
                    mocked.return_value = True
                    update_stats.side_effect = lambda x: None
                    await self.bot.process_new_updates([get_update('/bban', reply_to="shit text", user_id=ADMIN_ID)])
                    self.assertEqual(RESULTS[0], ({'chat_id': 11, 'message_id': 1}, 'deleteMessage'))
                    self.assertEqual(RESULTS[1], ({'chat_id': 11, 'message_id': 2}, 'deleteMessage'))
                    self.assertEqual(RESULTS[2][1], 'banChatMember')

    async def test_admin_can_unban(self):
        # Нужно подставить антиспам вкл.
        with patch("src.filters.is_antispam_enabled") as mocked:
            # Нужно подменить инкремент, нельзя реально в шелве работать в тестах
            with patch("src.commands.increment") as _mocked_shelve:
                # Подменяем обновление статистики, нам важно что оно просто было вызвано
                with patch("src.commands.update_stats") as update_stats:
                    mocked.return_value = True
                    update_stats.side_effect = lambda x: None
                    await self.bot.process_new_updates(
                        [get_update('/unban_id 1', reply_to="shit text", user_id=ADMIN_ID)])
                    self.assertEqual(RESULTS[0][1], 'unbanChatMember')

    async def test_white_id_can_add_quote(self):
        # Нужно подставить список цитат
        with patch("src.stan.all_chat_quotes") as mocked:
            # Нужно подменить инкремент, нельзя реально в шелве работать в тестах
            with patch("src.commands.increment") as _mocked_shelve:
                # Подменяем обновление статистики, нам важно что оно просто было вызвано
                with patch("src.stan.add_quote") as aq:
                    mocked.return_value = []
                    aq.side_effect = lambda *a: None
                    await self.bot.process_new_updates([get_update('/add', reply_to="good text", user_id=100)])
                    self.assertEqual(RESULTS[0][1], 'sendMessage')
                    self.assertEqual(RESULTS[0][0]['text'], '➕\n  └ good text')
                    self.assertEqual(RESULTS[1][1], 'deleteMessage')

    async def test_white_id_cant_add_existing_quote(self):
        # Нужно подставить список цитат
        with patch("src.stan.all_chat_quotes") as mocked:
            # Нужно подменить инкремент, нельзя реально в шелве работать в тестах
            with patch("src.commands.increment") as _mocked_shelve:
                # Подменяем реальное добавление цитаты, нам важно что оно просто было вызвано
                with patch("src.stan.add_quote") as add_qoute:
                    mocked.return_value = [["good text"]]
                    add_qoute.side_effect = lambda x, y: None
                    await self.bot.process_new_updates([get_update('/add', reply_to="good text", user_id=100)])
                    self.assertEqual(RESULTS[0][1], 'sendMessage')
                    self.assertEqual(RESULTS[0][0]['text'], '⛔️ Не добавил, есть токое\n  └ good text')

    async def test_white_id_cant_remove_non_existing_quote(self):
        # Нужно вернуть запрос о наличии цитаты
        with patch("src.stan.is_quote_in_chat") as mocked:
            mocked.return_value = False
            await self.bot.process_new_updates([get_update('/remove', reply_to="good text", user_id=100)])
            self.assertEqual(RESULTS[0][1], 'sendMessage')
            self.assertEqual(RESULTS[0][0]['text'], '⛔️ Нет такого\n  └ good text')

    async def test_white_id_can_remove_existing_quote(self):
        # Нужно вернуть запрос о наличии цитаты
        with patch("src.stan.is_quote_in_chat") as mocked:
            # Подменяем удаление цитаты, нам важно что оно просто было вызвано
            with patch("src.stan.delete_quote_in_chat") as delete_qoute:
                mocked.return_value = [["good text"]]
                delete_qoute.side_effect = lambda x, y: None
                mocked.return_value = True
                await self.bot.process_new_updates([get_update('/remove', reply_to="good text", user_id=100)])
                self.assertEqual(RESULTS[0][1], 'sendMessage')
                self.assertEqual(RESULTS[1][1], 'deleteMessage')
                self.assertEqual(RESULTS[0][0]['text'], '➖ \n  └ good text')

    async def test_new_user_in_chat(self):
        await self.bot.process_new_updates([member()])
        self.assertEqual(RESULTS[0][1], 'deleteMessage')
        self.assertEqual(RESULTS[1], ({'chat_id': 555}, 'getChat'))

    async def test_user_leave_chat(self):
        await self.bot.process_new_updates([member(leave=True)])
        self.assertEqual(RESULTS[0][1], 'deleteMessage')


if __name__ == '__main__':
    main()
