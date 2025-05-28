import random
import threading
import time
from datetime import datetime, timedelta
from typing import Dict

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8120519828:AAGeOBM9QM1UByZkRY068b0UbNR6GI89awU"
bot = telebot.TeleBot(TOKEN)

RANDOM_MESSAGES = [
   "Че лыбу давишь, хуй старый",
    "Как дебил улыбаешься, на айку проверялся?",
    "Ты чмо компании",
    "ты даже здесь проиграл",
    "ты не главное чмо компании, а всего лишь какое-то второе",
    "да ебальник свой прикрой, добряк",
    "штанов пошире не нашлось?",
    "ты нах не нужен",
    "стороной обходи меня",
    "нытик ебанный",
    "иди нахуй",
    "уйди по-хорошему",
    "Контекста дайте",
    "Я сам на минус вайбе",
    "сосед спит",
    "Да, я курю, но не от того, что это модно, просто груза много, просто душа сдохла",
    "Меньше пизди, больше делай",
    "Не заставляйте меня делать так чтобы вы плакали",
    "Без негатива",
    "Отсосите друг другу пидарасы",
    "Мне бля работу искать 😭",
    "ЖОПОЛИЗЫ",
    "димана верните сюда",
    "лучше не пиши ничего",
    "успокойся и поговорим",
    "Ты слаб, тебе тревожно сейчас",
    "дешевые драмы",
    "драма бустет едишон",
    "я в сквош иду играть",
    "плаки-плаки",
    "давайте все в реутов переедем",
    "на меня не рассчитывайте",
    "всм?",
    "БАСКЕТБОЛЛ, ВОЛЕЙБОЛЛ, КАРТИНГ, СКАЛОЛАЗАНИЕ",
    "Стажка заканчивается",
    "Я не умру чмом",
    "Я не умею общаться",
    "?",
    "я хочу секс",
    "кукан дымится",
    "помогите",
    "На репите слушаю училку",
    "Допиздишьсч сссукп",
    "Я твою будущую жену трахну и ты будешь воспитывать моего ребенка не зная это",
    "да ну нах",
    "капец",
    "Дота не надо быть идеальным, можно просто играть",
    "Я тебя люблю",
    "Ты сейчас плакать будешь",
    "Прекращай общаться так",
    "Тяжело с вами общаться",
    "Сходи к психологу",
    "Всем добра",
    "Всем добра и позитива",
    "Тебя посадят ебанат",
    "поплачь",
    "не ной",
    ")",
    "Закройся",
    "Еще раз меня обидите - я выйду", 
    "Мне птички напели что ни один бомж в Москве не был обеделее твоим вниманием",
    "Хуй отсоси всем бомжам Коломны",
    "Нет смысла вкидывать хуйню и думать что ты умный",
    "Есть претензия — говори прямо",
    "сосед заебал", 
    "Не беси сука",
    "я король куни",
    "делаю куни на 90 из 100",
    "бля, хочу трахнуть девочку",
    "хуй чешется",
    "шишка дымится",
    "пидарасы и хохлы",
    "Я щас в ментуру пойду",
    "Ты что до меня доебался",
    "Меня отчислили",
    "пошшшшшеееел в пиздууууууу",
    "Диплом не сдал"

]

# Глобальные переменные для хранения состояния
auto_messages: Dict[int, Dict[str, any]] = {}
conversation_mode: Dict[int, bool] = {}

def get_random_message():
    return random.choice(RANDOM_MESSAGES)

def create_time_set_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        KeyboardButton("10 минут"),
        KeyboardButton("30 минут"),
        KeyboardButton("1 час"),
        KeyboardButton("3 часа"),
        KeyboardButton("6 часов")
    )
    return markup

def schedule_auto_messages():
    while True:
        now = datetime.now()
        for chat_id, settings in list(auto_messages.items()):
            if settings["active"] and now >= settings["next_message_time"]:
                try:
                    bot.send_message(chat_id, get_random_message())
                    interval = settings["interval"] / 60 if settings["interval"] < 60 else settings["interval"]
                    auto_messages[chat_id]["next_message_time"] = now + timedelta(hours=interval)
                except Exception as e:
                    print(f"Ошибка в чате {chat_id}: {e}")
                    auto_messages.pop(chat_id, None)
        time.sleep(60)

# Запускаем поток для автоматических сообщений
threading.Thread(target=schedule_auto_messages, daemon=True).start()

@bot.message_handler(commands=['time_set'])
def time_set_command(message):
    bot.reply_to(message, 
                "Выбирай, с каким интервалом я буду тебя заебывать:",
                reply_markup=create_time_set_keyboard())

@bot.message_handler(commands=['time_off'])
def time_off_command(message):
    chat_id = message.chat.id
    if chat_id in auto_messages:
        auto_messages[chat_id]["active"] = False
        bot.reply_to(message, "Авто-сообщения выключены. Но ты все равно лох.")
    else:
        bot.reply_to(message, "Ты еблан? Авто-сообщения и так не работали.")

@bot.message_handler(commands=['random'])
def random_command(message):
    bot.reply_to(message, get_random_message())

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """Тебе нужна помощь? МИМИМИМИ САМ УЖЕ НЕ В СОСТОЯНИИ СПРАВИТЬСЯ?

Доступные команды:
/time_set - Настроить интервал авто-сообщений
/time_off - Выключить авто-сообщения
/random - Случайный высер
/conversation_on - Включить режим ответов
/conversation_off - Выключить режим ответов
/help - Помощь (бесполезная)"""
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['conversation_on'])
def conversation_on(message):
    chat_id = message.chat.id
    conversation_mode[chat_id] = True
    bot.reply_to(message, "Режим ответов включен. Готов унижать.")

@bot.message_handler(commands=['conversation_off'])
def conversation_off(message):
    chat_id = message.chat.id
    conversation_mode[chat_id] = False
    bot.reply_to(message, "Режим ответов выключен. Теперь ты мне не интересен, ничтожество.")

@bot.message_handler(func=lambda message: message.text in ["10 минут", "30 минут", "1 час", "3 часа", "6 часов"])
def handle_time_set(message):
    chat_id = message.chat.id
    time_mapping = {
        "10 минут": 10/60,
        "30 минут": 30/60,
        "1 час": 1,
        "3 часа": 3,
        "6 часов": 6
    }
    
    interval = time_mapping.get(message.text, 1)
    
    auto_messages[chat_id] = {
        "interval": float(message.text.split()[0]) if "мин" in message.text else interval,
        "active": True,
        "next_message_time": datetime.now() + timedelta(hours=interval)
    }
    
    bot.reply_to(message, 
                f"Я буду заебывать тебя каждые {message.text}. Наслаждайся, уёбок.",
                reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(commands=['start'])
def start_command(message):
    welcome_text = """ЧТО ЗА ХУЙНЮ ТЫ ТУТ НАЖАЛ, СОСУНОК? 🚬

Я - БОГДАНОВ ИЛЬЯ ДМИТРИЕВИЧ, ТВОЙ НОВЫЙ КОШМАР И ДИАГНОЗ ОДНОВРЕМЕННО.

ЗАПОМНИ ЭТИ КОМАНДЫ, МУДИЛА:
/time_set - НАСТРОЙКА ИНТЕРВАЛА, КОГДА Я БУДУ ТЕБЯ УНИЖАТЬ
/time_off - ВЫКЛЮЧИТЬ МОИ УНИЖЕНИЯ (ПЛАКИ-ПЛАКИ)
/random - СЛУЧАЙНЫЙ ВЫСЕР ИЗ МОЕГО БОГАТОГО ВНУТРЕННЕГО МИРА
/conversation_on - ВКЛЮЧИТЬ РЕЖИМ ОТВЕТОВ (НЕ СОВЕТУЮ)
/conversation_off - ВЫКЛЮЧИТЬ РЕЖИМ ОТВЕТОВ (ТРУС)
/help - ПОМОЩЬ (БЕСПОЛЕЗНАЯ, КАК И ТЫ)

ТЕПЕРЬ ЗАВАЛИСЬ НАХУЙ И НЕ МЕШАЙ МНЕ КУРИТЬ."""
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_messages(message):
    chat_id = message.chat.id
    
    # Игнорируем команды
    if message.text and message.text.startswith('/'):
        return
        
    # Режим ответов
    if conversation_mode.get(chat_id, False):
        bot.reply_to(message, get_random_message())

# Установка команд бота
bot.set_my_commands([
    telebot.types.BotCommand("start", "Начать общение с Ильей"),
    telebot.types.BotCommand("time_set", "Настроить интервал"),
    telebot.types.BotCommand("time_off", "Выключить авто-сообщения"),
    telebot.types.BotCommand("random", "Случайный высер"),
    telebot.types.BotCommand("conversation_on", "Включить ответы"),
    telebot.types.BotCommand("conversation_off", "Выключить ответы"),
    telebot.types.BotCommand("help", "Помощь")
])

print("Бот запущен и готов ломать психику!")
bot.infinity_polling()