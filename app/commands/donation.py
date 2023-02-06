from telebot.types import LabeledPrice, Message, PreCheckoutQuery
from ..config import YOOPAY, bot

prices = [LabeledPrice('Сумма', 100_00)]


@bot.message_handler(commands=['donate'])
def request_invoice(message: Message):
    bot.send_invoice(message.chat.id, 'Поддержать проект', 'Stan', 'donate_stan', provider_token=YOOPAY,
                     currency='RUB', prices=prices,
                     provider_data='{"capture": true}',
                     max_tip_amount=500_000_00,
                     suggested_tip_amounts=[150_00, 300_00, 500_00, 1_000_00], capture=True,
                     )


@bot.pre_checkout_query_handler(func=lambda a: True)
def process_pre_checkout(q: PreCheckoutQuery):
    bot.answer_pre_checkout_query(q.id, True, 'Извините, пожертвования больше не принимаем!')
