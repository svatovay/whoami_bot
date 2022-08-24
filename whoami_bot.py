import logging
import json
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler

from code_db.fill_db import add_room, add_player
from code_db import selects_db as selects

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

game_info = {
    'room_number': None,
    'player_name': None,
    'player_role': None,
}

characters = (
    'Магистр Йода',
    'Дарт Вейдер',
    'Винни Пух',
    'Джеймс Бонд',
    'Индиана Джонс',
    'Клариса Старлинг',
    'Рокки Бальбоа',
)

START_GAME, PLAYER_NAME, PLAYER_ROLE, PLAYERS_LIST = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Create room', 'Enter the room']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = \
        'Привет. Я бот для игры в "Кто я" или, как иногда игру называют, "Стикеры"\n' \
        'Это цифровой аналог игры, где каждому игроку приклеивается на лоб стикер с именем человека/персонажем/предметом/явлением.\n' \
        'Правила игры:\n' \
        '1. Один из игроков должен создать комнату;\n' \
        '2. Затем, оставшиеся игроки добавляются в эту комнату по её номеру;\n' \
        '3. После чего происходит распределение того, что будет указано у каждого на стикере;\n' \
        '4. Я выведу каждому игроку список других игроков с их загаданными словами;\n' \
        '5. После этого можно начинать играть;\n' \
        'Команда /cancel, чтобы прекратить разговор.\n\n'
    await update.message.reply_text(text, reply_markup=markup_key)
    return START_GAME


def select_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Create room':
        return create_room(update)
    elif update.message.text == 'Enter the room':
        return entrance_room(update)


async def create_room(update: Update):
    def random_number_pick():
        random_number = f'{random.randint(0, 10000):04}'
        if selects.select_room(random_number):
            return random_number_pick()
        else:
            return random_number

    markup_key = ReplyKeyboardMarkup([['next']], one_time_keyboard=True)

    room_number = random_number_pick()
    add_room(room_number)

    game_info['room_number'] = room_number

    text = f'Ваша комната №{room_number}.\n' \
           f'Другие игроки могут в неё войти.'

    await update.message.reply_text(text, reply_markup=markup_key)
    return PLAYER_NAME


async def entrance_room(update: Update):
    text = 'Введите номер комнаты'

    await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    return PLAYER_NAME


async def player_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not game_info['room_number'] and selects.select_room(update.message.text):
        game_info['room_number'] = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Введите своё имя")
    return PLAYER_ROLE


async def player_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game_info['player_name'] = update.message.text
    game_info['player_role'] = random.choice(selects.select_roles(1)).id

    add_player(game_info)

    markup_key = ReplyKeyboardMarkup([['view players']], one_time_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Удачной игры!", reply_markup=markup_key)
    return PLAYERS_LIST


async def players_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    players = selects.select_players(game_info['room_number'], game_info['player_name'])
    players_list = [f"{player.name} -> {selects.select_role(player.role_id).role}" for player in players]
    text = '\n'.join(players_list)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def cancel(update, _):
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


if __name__ == '__main__':
    with open('token.json', 'r') as tokenfile:
        token = json.load(tokenfile).get("token")

    application = ApplicationBuilder().token(token).build()

    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START_GAME: [MessageHandler(filters.Regex('^(Create room|Enter the room)$'), select_start)],
            PLAYER_NAME: [MessageHandler(filters.Regex('^(\d{4}|next)$'), player_name)],
            PLAYER_ROLE: [MessageHandler(filters.Regex('^([a-zA-Zа-яА-ЯёЁ]*)$'), player_role)],
            PLAYERS_LIST: [MessageHandler(filters.Regex('^(view players)$'), players_list)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(start_handler)

    application.run_polling()
