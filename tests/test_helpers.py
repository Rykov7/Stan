from unittest import TestCase, main
from unittest.mock import MagicMock
from src.constants import SPAM, BAN_WORDS, ADMIN_ID
from src.helpers import is_spam, is_mixed, is_ban_words_in_caption, is_in_not_allowed, is_nongrata, is_admin

CASES = (
    "Оформим резидeнтствo ОАЭ без предoплаты за 5000 дирхам. Пoдробнoсти в лc",
    "Всем привет Я в поисках людей в kpиптo кoмaнду У нас вы пройдете 6ecплaтноe обученue 1-3 дня Можно совмещать с основной paбoтoй"
)


class TestSpam(TestCase):
    def test_simple(self):
        for spam_word in SPAM:
            with self.subTest(f"check spam word({spam_word})"):
                self.assertTrue(is_spam(spam_word))

    def test_case_first(self):
        for text in CASES:
            with self.subTest(f"check case({text})"):
                self.assertTrue(is_spam(text))

    def test_one(self):
        self.assertTrue(is_spam("привeт"))  # e английская

    def test_is_mixed(self):
        self.assertTrue(is_mixed("привeт"))  # e английская
        self.assertFalse(is_mixed("привет ребята!"))
        self.assertFalse(is_mixed("hi guys"))
        self.assertFalse(is_mixed("hi guys! #%^&%^$ @Вася привет g! п@"))
        self.assertFalse(is_mixed("тут подробнее https://hack.comp.com"))
        self.assertTrue(is_mixed("hi guys! #%^&%^$ ghb привет g! пQ"))



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


if __name__ == '__main__':
    main()
