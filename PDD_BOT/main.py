from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, CallbackQueryHandler
)
from telegram.ext import Application
import os
from signs import show_warning_sign
from signs import handle_sign_callback
from signs import start_test, handle_test_answer, send_test_question
from theory import show_theory, handle_theory_callback
from crossroads import show_crossroad, handle_crossroad_callback
from railways import show_railways, handle_railways_callback
from tr_lights import show_lights, handle_lights_callback
from accidents import show_accidents, handle_accidents_callback
from cargo import show_cargos, handle_cargos_callback
from bad_weather import show_weather, handle_weather_callback
from ped import show_ped, handle_ped_callback
from med_help import show_med, handle_med_callback
from responsibility import show_responsibilities, handle_responsibilities_callback
from markings import show_marking_card, handle_marking_callback
from pdd_test import (
    start_exam_mode,
    select_ticket_range,
    select_ticket,
    start_exam_questions,
    handle_exam_answer,
    exam_to_menu,
    exam_all_ranges
)
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import notifications
from notifications import (
    start_reminders, choose_days, toggle_day,
    choose_time, set_time, disable_reminders
)

from telegram.ext import CallbackQueryHandler

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
        await notifications.start_reminders(update, context)
    elif text == "📘 Проверить знания по теме":
        await update.message.reply_text("📚 Выберите тему для теста:", reply_markup=get_test_topics_keyboard())
    elif text == "🧾 Режим экзамена":
        await start_exam_mode(update, context)
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
    if topic == "topic_2":
        await show_marking_card(update, context, index=0)
    if topic == "topic_3":
        await show_theory(update, context, index=0)
    if topic == "topic_4":
        await show_crossroad(update, context, index=0)
    if topic == "topic_5":
        await show_ped(update, context, index=0)
    if topic == "topic_6":
        await show_railways(update, context, index=0)
    if topic == "topic_7":
        await show_lights(update, context, index=0)
    if topic == "topic_8":
        await show_accidents(update, context, index=0)
    if topic == "topic_9":
        await show_cargos(update, context, index=0)
    if topic == "topic_10":
        await show_weather(update, context, index=0)
    if topic == "topic_11":
        await show_med(update, context, index=0)
    if topic == "topic_12":
        await show_responsibilities(update, context, index=0)

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

    # TOKEN = "8156068493:AAGHQPzuMaFMNf7XgdCyNHGLfiQYq9fGzFQ"  # <-- Замени на свой токен

    # app = ApplicationBuilder().token(TOKEN).build()
    # job_queue = app.job_queue

    TOKEN = "6753534657:AAGZ84h_1V8MAVOy6lMQkRV4az5yc8rvvr0"

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
    app.add_handler(CallbackQueryHandler(handle_topic_selection, pattern=r"^topic_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_theme_selection, pattern=r"^theme_\d+$"))

    app.add_handler(CallbackQueryHandler(handle_test_answer, pattern=r"^quiz_answer\|"))

    app.add_handler(CallbackQueryHandler(show_theory, pattern=r"^theory_\+$"))
    app.add_handler(CallbackQueryHandler(handle_theory_callback, pattern="^theory_\\d+$|^back_to_topics$"))

    app.add_handler(CallbackQueryHandler(show_crossroad, pattern=r"^crossroad_\+$"))
    app.add_handler(CallbackQueryHandler(handle_crossroad_callback, pattern="^crossroad_\\d+$|^back_to_topics$"))

    app.add_handler(CallbackQueryHandler(show_ped, pattern=r"^ped_\+$"))
    app.add_handler(CallbackQueryHandler(handle_ped_callback, pattern="^ped_\\d+$|^back_to_topics$"))

    app.add_handler(CallbackQueryHandler(show_railways, pattern=r"^railways_\+$"))
    app.add_handler(CallbackQueryHandler(handle_railways_callback, pattern="^railways_\\d+$|^back_to_topics$"))

    app.add_handler(CallbackQueryHandler(handle_marking_callback, pattern="^marking_"))
    app.add_handler(CallbackQueryHandler(handle_marking_callback, pattern="^start_marking_test$"))

    app.add_handler(CallbackQueryHandler(handle_lights_callback, pattern="^lights_"))
    app.add_handler(CallbackQueryHandler(handle_lights_callback, pattern="^start_lights_test$"))

    app.add_handler(CallbackQueryHandler(handle_accidents_callback, pattern="^accidents_"))
    app.add_handler(CallbackQueryHandler(handle_accidents_callback, pattern="^start_accidents_test$"))

    app.add_handler(CallbackQueryHandler(handle_cargos_callback, pattern="^cargos_"))
    app.add_handler(CallbackQueryHandler(handle_cargos_callback, pattern="^start_cargos_test$"))

    app.add_handler(CallbackQueryHandler(handle_med_callback, pattern="^med_"))
    app.add_handler(CallbackQueryHandler(handle_med_callback, pattern="^start_med_test$"))

    app.add_handler(CallbackQueryHandler(handle_weather_callback, pattern="^weather_"))
    app.add_handler(CallbackQueryHandler(handle_weather_callback, pattern="^start_weather_test$"))

    app.add_handler(CallbackQueryHandler(handle_responsibilities_callback, pattern="^responsibilities_"))
    app.add_handler(CallbackQueryHandler(handle_responsibilities_callback, pattern="^start_responsibilities_test$"))

    app.add_handler(CallbackQueryHandler(select_ticket_range, pattern=r"^exam_range_\d+_\d+$"))
    app.add_handler(CallbackQueryHandler(select_ticket, pattern=r"^exam_ticket_\d+$"))
    app.add_handler(CallbackQueryHandler(start_exam_questions, pattern=r"^start_exam$"))
    app.add_handler(CallbackQueryHandler(handle_exam_answer, pattern=r"^exam_answer_\d+$"))
    app.add_handler(CallbackQueryHandler(exam_to_menu, pattern=r"^exam_to_menu$"))
    app.add_handler(CallbackQueryHandler(exam_all_ranges, pattern="^exam_all_ranges$"))

    app.add_handler(CommandHandler("reminders", start_reminders))
    app.add_handler(CallbackQueryHandler(choose_days, pattern="remind_choose_day"))
    app.add_handler(CallbackQueryHandler(toggle_day, pattern="toggle_day_"))
    app.add_handler(CallbackQueryHandler(choose_time, pattern="remind_choose_time"))
    app.add_handler(CallbackQueryHandler(set_time, pattern="set_time_"))
    app.add_handler(CallbackQueryHandler(disable_reminders, pattern="remind_disable"))

    app.add_handler(CallbackQueryHandler(handle_sign_callback))
    app.add_handler(CallbackQueryHandler(handle_menu_selection))



    print("Бот запущен...")
    app.run_polling()