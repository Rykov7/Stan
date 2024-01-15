from unittest import TestCase, main
from unittest.mock import MagicMock
from src.constants import SPAM, BAN_WORDS, ADMIN_ID, RULES_TEXT
from src.helpers import (
    is_spam, is_mixed, is_ban_words_in_caption, is_in_not_allowed, is_nongrata, is_admin, fetch_rule, cleaned_text,
    remove_spaces, has_no_letters, has_links
)

REAL_CASES = (
    "Оформим резидeнтствo ОАЭ без предoплаты за 5000 дирхам. Пoдробнoсти в лc",
    "Всем привет Я в поисках людей в kpиптo кoмaнду У нас вы пройдете 6ecплaтноe обученue 1-3 дня Можно совмещать с основной paбoтoй",
    "Здравствуйте! Нужны 2 человека от 200 $/день. Можно без опыта Пишите в личные сообщения +",
    "Здравствуйте!Нужны 2 человека от 200 $/день.Пишите в личные сообщение +",

    f"🙌Присоединяйтесь к нашей команде и освойте мир цифровой валюты совершенно бесплатно! Низкий порог входа "
    f"позволяет каждому воплотить свои финансовые амбиции. У нас - не просто обучение, а возможность изменить свое "
    f"финансовое будущее. Прокачайте свои навыки вместе с нами!Писать в личные✌️",

    f"Ищу партнёров для совместной работы в сфере цифровых активов Опыт не обязателен, всему обучаю бесплатно, "
    f"без предоплат! Мой интерес % от чистого дохода 💵Все внутри биржи, без левых обменников. "
    f"Пишите, расскажу подробнее."
)

TEST_CASES = ('here it me.sv/122', "My site is tg.sv/home", "look here goo.by/home", "Go there go.sv/home",
              "I am here intim.video/home", "Here ckick it uclck.ru/home", 'WOW💎', 'Attention 🔞', 'Look here ➡️',
              'Money for you💰', 'Some cash💸', 'Real money‼️', 'Много раб0т', '0плата гарантируется',
              'для вас новый способ заработка', 'в сфере криптовалют', 'в сфере цифровых валют', 'на бирже Binance',
              'на бирже ByBit', 'Помогу заработать денег', 'арбитраж вам нужен', 'DEX биржи', 'любую девушку можно',
              'прибыль у вaс в кармане', 'обучaю быстро и бесплатно', 'Предлагаю новый вид заработка',
              'межбиржевой круг', 'КУПЮРЫ как настоящие', 'kрипта форева', 'биpжа ждет', 'apбитpaж валют',
              'в неделю выходит до 100', 'хочу предложить заработок', 'голые фотки баб', 'интимные фото девчат',
              'заработка в крипте много не бывает', 'Веду набор в команде', 'Идёт набор ко мне', 'Доход от 100',
              'Trading это круто', 'P2P бойз', 'Идет набор куда то', 'нaбop номера', 'в комaндy', 'kpuпта есть',
              'бupжы рулят', 'пишитe всем', 'ноль $ в неделю', 'обучаю с нуля и единицы', 'доходы для всех парней',
              'по трейдингу пройдем', 'фальшивые рубли это зло', 'зароботку в нете', 'Набuраю номера', 'цuфры есть?',
              'Обучу вас плясать', 'прuбором владею', 'остались курсы по шитью', 'Cryptограф', 'kристалл', 'рuсовать',
              'в лc пиши', "в личные сообщения пиши", 'Жду в ЛС ребят', 'подробнее в лс напишу', 'напиши в личку друг',
              'пишите в ЛС парни', 'Писать в ЛИЧКУ! ура!', 'Пишите в личку админу', 'в л.с. кпсс', 'по вопросам в ЛС',
              'пишите мне в ЛС девчата', 'Писать в ЛС не нужно', 'мне в ЛС не пишите', 'в лс пишите', 'Писать в личные',
              'пишем в личку', 'стучите в личку', 'жду в личке', 'жду в личных сообщениях', 'шлем в личные сообщения +',
              'Пишем в личные', 'напишите в личные', 'превет мы ищем партнеров', 'я ищу партнеров для дела',
              'команда в поиске партнеров', 'пить обучим бесплатно', 'обучу бесплатно петь', 'обучаю бесплатно всему',
              'цифровых активов нет', 'цифровые активы кончились', 'цифровые валюты в твоем кошельке',
              'обучим без предоплат', 'вас обучим без предоплаты', 'никаких предоплат не нужно',
              'для этого предоплаты не требуется', 'для этого предоплата не требуется', 'в этом предоплата не нужна'
              )


class TestSpam(TestCase):
    def test_simple(self):
        for spam_word in SPAM:
            with self.subTest(f"check spam word({spam_word})"):
                self.assertTrue(is_spam(spam_word))

    def test_case_first(self):
        for text in REAL_CASES:
            with self.subTest(f"check case({text})"):
                self.assertTrue(is_spam(text))

    def test_main_cases(self):
        for text in TEST_CASES:
            with self.subTest(f"check case({text})"):
                self.assertTrue(is_spam(text))

    def test_one(self):
        self.assertTrue(is_spam("привeт"))  # e английская

    def test_is_mixed(self):
        self.assertTrue(is_mixed("привeт"))  # e английская
        self.assertFalse(is_mixed("привет ребята!"))
        self.assertFalse(is_mixed("hi guys"))
        self.assertFalse(is_mixed("hi guys! #%^&%^$ @Вася привет g! п@"))
        self.assertFalse(is_mixed("hi guys! #%^&%^$ @Вася привет g! п@"))
        self.assertFalse(is_mixed("тут *подробнее* https://hack.comp.com"))
        self.assertTrue(is_mixed("hi guys! #%^&%^$ ghb привет g! пQ"))
        text = """
        В целом очень интересный чат, где 4 человека
 считают себя выше мира всего и нападают/насмехаются на всех/над всеми, кто что-то "недо". 
Один из которых вообще выдаёт какие-то фразы через бота) интересно, потому что сам не может сказать, или потому что раздвоение личности дело такое)
«Я пуп земли», – твердит гордец надменно,
Забыв, что он – песчинка во вселенной."""
        self.assertFalse(is_mixed(text))
        self.assertFalse(is_mixed('print("привет")'))
        self.assertFalse(is_mixed("print('привет')"))
        self.assertFalse(is_mixed("text='слово'"))
        self.assertTrue(is_mixed("kрипт"))
        self.assertTrue(is_mixed("kpuпт"))
        self.assertTrue(is_mixed('бupж'))
        self.assertTrue(is_mixed('пишитe'))
        self.assertTrue(is_mixed('нaбop'))
        self.assertTrue(is_mixed('комaндy'))
        self.assertTrue(is_mixed('Набuраю'))
        self.assertTrue(is_mixed('цuфр'))
        self.assertTrue(is_mixed('прuб'))
        self.assertTrue(is_mixed('kр'))
        self.assertTrue(is_mixed('рu'))
        self.assertTrue(is_mixed('apбитpaж'))
        self.assertTrue(is_mixed('биpж'))


class TestOthers(TestCase):
    def test_ban(self):
        for word in BAN_WORDS:
            with self.subTest(f"check ban word({word})"):
                self.assertTrue(is_ban_words_in_caption(word))

    def test_allowed(self):
        params = (
            (True, [], 'any'),
            (True, ['one'], 'two'),
            (False, ['one', 'two'], 'two'),
            (False, ['one', 'two'], 'Two'),
            (False, ['one', 'two'], 'TWO'),
        )
        for expected, words, mess in params:
            with self.subTest(f"check allowed({words, mess})"):
                self.assertEqual(is_in_not_allowed(words, mess), expected)

    def test_non_grata(self):
        params = (
            (False, 'any'),
            (True, 'дудар'),
            (True, 'хауди'),
            (True, 'dudar'),
        )
        for expected, text in params:
            with self.subTest(f"check non-grata({text})"):
                m = MagicMock(text=text)
                self.assertEqual(is_nongrata(m), expected)

    def test_is_admin(self):
        params = (
            (False, 'any'),
            (True, ADMIN_ID),
        )
        for expected, text in params:
            with self.subTest(f"check non-grata({text})"):
                m = MagicMock(from_user=MagicMock(id=text))
                self.assertEqual(is_admin(m), expected)

    def test_fetch_rule(self):
        for index, text in enumerate(RULES_TEXT, 1):
            with self.subTest(f"fetch rule {index}"):
                self.assertEqual(fetch_rule(index), text)

    def test_fetch_non_existent_rule(self):
        self.assertEqual(fetch_rule(0), 'Пока не придумали')
        self.assertEqual(fetch_rule(100), 'Пока не придумали')

    def test_cleaned_text(self):
        params = (
            ('f1   b2  print  text  ', 'f1!, b2# print("text")'),
            ('text', 'text'),
            ('    ', '!@#$'),
        )
        for expected, text in params:
            with self.subTest(f"cleaned_text {text}"):
                self.assertEqual(expected, cleaned_text(text))

    def test_remove_spaces(self):
        params = (
            ('f1 b2 print text', 'f1   b2  print  text  '),
            ('text', 'text'),
            ('!@#$', '!@#$'),
        )
        for expected, text in params:
            with self.subTest(f"remove_spaces {text}"):
                self.assertEqual(expected, remove_spaces(text))

    def test_has_no_letters(self):
        params = (
            (False, 'f1   b2  print  text  '),
            (True, ''),
            (True, ' '),
            (True, '12 @# &*'),
            (False, '12 @# &* f'),
            (False, '12 @# &* Z'),
            (False, '12 @# &* я'),
            (False, '12 @# &* Я'),
        )
        for expected, text in params:
            with self.subTest(f"has_no_letters {text}"):
                self.assertEqual(expected, has_no_letters(text))

    def test_has_links(self):
        params = (
            (True, 'My bot https://t.me/bot.some'),
            (True, 'My bot http://t.me/bot.some'),
            (False, 'My bot here'),
            (False, 'I can use http'),
        )
        for expected, text in params:
            with self.subTest(f"has_links {text}"):
                self.assertEqual(expected, has_links(text))


if __name__ == '__main__':
    main()
