from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Словарь для хранения данных игроков
players = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in players:
        await update.message.reply_text("Ты уже зарегистрирован!")
        return

    # Создаём клавиатуру для выбора расы
    keyboard = [
        [InlineKeyboardButton("Человек", callback_data="race_human")],
        [InlineKeyboardButton("Орк", callback_data="race_orc")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выбери свою расу:", reply_markup=reply_markup)

# Обработчик выбора расы
async def choose_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    race = query.data.split("_")[1]  # race_human → human, race_orc → orc

    # Сохраняем расу
    players[user_id] = {"race": race, "class": None}

    # Создаём клавиатуру для выбора класса
    if race == "human":
        keyboard = [
            [InlineKeyboardButton("Паладин", callback_data="class_paladin")],
            [InlineKeyboardButton("Вор", callback_data="class_rogue")]
        ]
    elif race == "orc":
        keyboard = [
            [InlineKeyboardButton("Overlord", callback_data="class_overlord")],
            [InlineKeyboardButton("Destroyer", callback_data="class_destroyer")]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Теперь выбери класс:", reply_markup=reply_markup)

# Обработчик выбора класса
async def choose_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    class_ = query.data.split("_")[1]  # class_paladin → paladin, class_rogue → rogue

    # Сохраняем класс
    players[user_id]["class"] = class_

    # Отправляем сообщение с результатами
    race = players[user_id]["race"]
    await query.edit_message_text(f"Ты {race}, класс {class_}. Добро пожаловать в игру!")

# Основная функция
def main():
    # Твой токен
    token = "7721415697:AAHg2P1-8N7YleIfNC8wZqUyB2znDHCeTAQ"
    application = Application.builder().token(token).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(choose_race, pattern="^race_"))
    application.add_handler(CallbackQueryHandler(choose_class, pattern="^class_"))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()