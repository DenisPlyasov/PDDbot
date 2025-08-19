from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, CallbackQueryHandler
)

from signs import show_warning_sign
from signs import handle_sign_callback
from signs import start_test, handle_test_answer, send_test_question
from theory import show_theory, handle_theory_callback

# Главное меню (reply keyboard)
main_menu_keyboard = [
    ["🚗 Выучить ПДД"],
    ["🧠 Проверить мои знания"],
    ["⏰ Включить напоминания"]
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

# Список тем
topics = [
    "1. Дорожные знаки",
    "2. Дорожная разметка",
    "3. Основные положения ПДД",
    "4. Проезд перекрёстков",
    "5. Пешеходы и велосипедисты",
    "6. Железнодорожные переезды",
    "7. Светофоры и сигналы регулировщика",
    "8. Аварии и действия при ДТП",
    "9. Перевозка пассажиров и грузов",
    "10. Вождение в плохую погоду",
    "11. Медпомощь и безопасность",
    "12. Ответственность за нарушения"
]

test_topics = [
    "1. Дорожные знаки",
    "2. Дорожная разметка",
    "3. Основные положения ПДД",
    "4. Проезд перекрёстков",
    "5. Пешеходы и велосипедисты",
    "6. Железнодорожные переезды",
    "7. Светофоры и сигналы регулировщика",
    "8. Аварии и действия при ДТП",
    "9. Перевозка пассажиров и грузов",
    "10. Вождение в плохую погоду",
    "11. Медпомощь и безопасность",
    "12. Ответственность за нарушения"
]



knowledge_check_keyboard = [
    ["📘 Проверить знания по теме"],
    ["🧾 Режим экзамена"],
    ["🔙 В главное меню"]
]
knowledge_check_markup = ReplyKeyboardMarkup(knowledge_check_keyboard, resize_keyboard=True)

# Преобразуем темы в Inline-кнопки
def get_topics_keyboard():
    keyboard = []
    for i, topic in enumerate(topics, start=1):
        keyboard.append([InlineKeyboardButton(text=topic, callback_data=f"topic_{i}")])
    return InlineKeyboardMarkup(keyboard)

def get_test_topics_keyboard():
    keyboard = []
    for i, theme in enumerate(test_topics, start=1):
        data = f"theme_{i}"
        keyboard.append([InlineKeyboardButton(text=theme, callback_data=data)])
    return InlineKeyboardMarkup(keyboard)

# Обработчик /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    welcome_text = (
        f"👋 Привет, {user_first_name}!\n\n"
        "Я помогу тебе выучить ПДД и подготовиться к экзамену.\n\n"
        "Выбери, с чего хочешь начать:"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu_markup)

# Обработка текстовых кнопок из главного меню
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🚗 Выучить ПДД":
        await update.message.reply_text("📚 Вот список тем:", reply_markup=get_topics_keyboard())
    elif text == "🧠 Проверить мои знания":
        await update.message.reply_text("Выберите режим:", reply_markup=knowledge_check_markup)
    elif text == "⏰ Включить напоминания":
        await update.message.reply_text("⏰ Напоминания будут добавлены позже.")
    elif text == "📘 Проверить знания по теме":
        await update.message.reply_text("📚 Выберите тему для теста:", reply_markup=get_test_topics_keyboard())
    elif text == "🧾 Режим экзамена":
        await update.message.reply_text("🛠 Режим экзамена находится в разработке.")
    elif text == "🔙 В главное меню":
        await update.message.reply_text("🔙 Возвращаемся в главное меню:", reply_markup=main_menu_markup)
    else:
        await update.message.reply_text("Пожалуйста, выбери пункт из меню.")

# Обработка нажатий на темы (callback кнопки)
async def handle_topic_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    topic = query.data

    if topic == "topic_1":
        await show_warning_sign(update, context, index=0)
    if topic == "topic_3":
        await show_theory(update, context, index=0)

async def handle_theme_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    theme = query.data

    if theme == "theme_1":
        print('Got callback:', theme)
        await send_test_question(update, context)
    if theme == "theme_3":
        await send_test_question(update, context)
    else:
        await query.edit_message_text("Извините, данная тема ещё не реализована.")


# Запуск бота
if __name__ == '__main__':
    import os

    TOKEN = "8156068493:AAGHQPzuMaFMNf7XgdCyNHGLfiQYq9fGzFQ"  # <-- Замени на свой токен

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
    app.add_handler(CallbackQueryHandler(handle_topic_selection, pattern=r"^topic_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_theme_selection, pattern=r"^theme_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_test_answer, pattern=r"^quiz_answer\|"))
    app.add_handler(CallbackQueryHandler(show_theory, pattern=r"^theory_\+$"))
    app.add_handler(CallbackQueryHandler(handle_theory_callback, pattern="^theory_\\d+$|^back_to_topics$"))
    app.add_handler(CallbackQueryHandler(handle_sign_callback))
    app.add_handler(CallbackQueryHandler(handle_menu_selection))



    print("Бот запущен...")
    app.run_polling()