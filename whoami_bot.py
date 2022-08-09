import logging
import json
import random
from telegram import Update, Bot
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def create_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    def random_number_pick(input_rooms: dict):
        random_number = f'{random.randint(0, 10000):04}'
        if random_number in input_rooms.keys() and input_rooms[random_number]['is_reserved']:
            return random_number_pick(input_rooms)
        else:
            return random_number

    with open("sessions.json", "r") as game_sessions:
        rooms = json.load(game_sessions)

    room_number = random_number_pick(rooms)
    rooms[room_number] = {
        "players_roles": None,
        "is_reserved": True
    }

    with open("sessions.json", "w") as game_sessions:
        json.dump(rooms, game_sessions)

    text = f'Ваша комната №{room_number}.\n' \
           f'Другие игроки могут в неё войти.'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def entrance_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Введите номер комнаты")


async def entrance_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Введите номер комнаты")


if __name__ == '__main__':
    with open('token.json', 'r') as tokenfile:
        token = json.load(tokenfile).get("token")

    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    create_room_handler = CommandHandler('create_room', create_room)
    # entrance_room_handler = CommandHandler('entrance_room', entrance_room)
    # entrance_dialog_handler = ConversationHandler(entry_points=[CommandHandler('entrance_room', entrance_room)])

    application.add_handler(start_handler)
    application.add_handler(create_room_handler)
    # application.add_handler(entrance_dialog_handler)

    application.run_polling()
