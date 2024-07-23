import random
from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Words, Users, User_Word
import json

state_storage = StateMemoryStorage()

with open('info.json', encoding='utf-8') as f:
    res = json.load(f)

token_bot = res['token_bot']

bot = TeleBot(token_bot, state_storage=state_storage)

known_users = []
userStep = {}
buttons = []

def add_users(engine, сid):

    session = (sessionmaker(bind=engine))()
    session.add(Users(cid=сid))
    session.commit()

    session.close()

def get_words(engine, cid):

    session = (sessionmaker(bind=engine))()

    translate_base = session.query(Words.eng, Words.rus).all()

    user_translate_base = session.query(User_Word.eng, User_Word.rus) \
        .join(Users, Users.id == User_Word.users_id) \
        .filter(Users.cid == cid).all()

    result = translate_base + user_translate_base
    session.close()
    return result

def add_words(engine, cid, word, translate):

    session = (sessionmaker(bind=engine))()

    user_id = session.query(Users.id).filter(Users.cid == cid).first()[0]

    session.add(User_Word(eng=word, rus=translate, users_id=user_id))
    session.commit()

    session.close()

def delete_words(engine, cid, word):

    session = (sessionmaker(bind=engine))()
    user_id = session.query(Users.id).filter(Users.cid == cid).first()[0]

    session.query(User_Word).filter(User_Word.users_id == user_id, User_Word.eng == word).delete()
    session.commit()
    session.close()

def show_hint(*lines):
    return '\n'.join(lines)

def show_target(data):
    return f"{data['target_word']} -> {data['translate_word']}"

class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'

class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()

@bot.message_handler(commands=['cards', 'start'])
def create_cards(message):

    cid = message.chat.id
    if cid not in known_users:
        known_users.append(cid)
        add_users(engine, cid)
        userStep[cid] = 0
        bot.send_message(cid, 'Hello, stranger, let study English...')

    markup = types.ReplyKeyboardMarkup(row_width=2)  #создаем клавиатуру

    global buttons
    buttons = []

    words_pair = random.sample(get_words(engine, cid), 4)
    pair = words_pair[0]
    target_word = pair[0]  # брать из БД
    translate = pair[1]  # брать из БД
    others = [pair[0] for pair in words_pair[1:]]  # брать из БД

    target_word_btn = types.KeyboardButton(target_word) # создаем кнопку для целевого слова
    buttons.append(target_word_btn)
    other_words_btns = [types.KeyboardButton(word) for word in others] # создаем кнопки для остальных слов
    buttons.extend(other_words_btns)

    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons) # добавили все кнопки

    greeting = f'Выбери перевод слова:\n🇷🇺 {translate}'
    bot.send_message(message.chat.id, greeting, reply_markup=markup) # показываем все кнопки
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = others

@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):

    create_cards(message)

@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        delete_words(engine, message.chat.id, data['target_word'])
        bot.send_message(message.chat.id, 'Слово удалено')

@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):

    cid = message.chat.id
    userStep[cid] = 1
    bot.send_message(cid, "Введите слово на английском")
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)

@bot.message_handler(func=lambda message: True, content_types=['text']) # обработка любого текста
def message_reply(message):

    text = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2)
    cid = message.chat.id

    if userStep[cid] == 0:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            target_word = data['target_word']

            if text == target_word:
                hint = show_target(data)
                hint_text = ['Отлично!❤', hint]
                next_btn = types.KeyboardButton(Command.NEXT)
                add_word_btn = types.KeyboardButton(Command.ADD_WORD)
                delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
                buttons.extend([next_btn, add_word_btn, delete_word_btn])
                hint = show_hint(*hint_text)
            else:
                for btn in buttons:
                    if btn.text == text:
                        btn.text = text + '❌'
                        break
                hint = show_hint("Допущена ошибка!",
                                 f"Попробуй ещё раз вспомнить слово 🇷🇺{data['translate_word']}")
                markup.add(*buttons)
        bot.send_message(message.chat.id, hint, reply_markup=markup)

    elif userStep[cid] == 1:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['target_word'] = text
            bot.send_message(cid, "Введите перевод слова на русском")
            bot.set_state(message.from_user.id, MyStates.translate_word, message.chat.id)
            userStep[cid] = 2

    elif userStep[cid] == 2:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['translate_word'] = text
            add_words(engine, cid, data['target_word'], data['translate_word'])
            bot.send_message(cid, 'Слово добавлено')
            userStep[cid] = 0

        create_cards(message)


if __name__ == '__main__':

    with open('info.json', encoding='utf-8') as f:
        res = json.load(f)
    DSN = f"{res['postgreSQL']['bd']}://{res['postgreSQL']['login']}:{res['postgreSQL']['password']}@localhost:5432/{res['postgreSQL']['name_bd']}"

    engine = sqlalchemy.create_engine(DSN)
    Session = sessionmaker(bind=engine)
    session = Session()

    create_tables(engine)

    with open('tests_data.json', encoding='utf-8') as fd:
        data = json.load(fd)
    for record in data:
        model = {
            'words': Words,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

    session.close()

    print('Start telegram bot...')

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling(skip_pending=True)