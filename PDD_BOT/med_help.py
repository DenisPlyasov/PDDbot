from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
import os
import random


# main_med = [
#     {
#         "name": "🔸 1. Немного теории",
#         "description": f"Первая помощь при ДТП — это действия, направленные на спасение жизни и здоровья пострадавших до приезда медиков.\n\nСвоевременная помощь и соблюдение мер безопасности могут спасти жизнь и снизить тяжесть последствий ДТП.",
#     },
#     {
#         "name": "🔸 2. Обязанности водителя",
#         "description": f"	•	Остановиться и включить аварийную сигнализацию.\n•	Оценить обстановку и исключить опасность (пожар, взрыв, движение машин).\n•	Вызвать скорую помощь и полицию.",
#     },
#     {
#         "name": "🔸 3. Основы оказания помощи",
#         "description": f"	•	Проверить сознание и дыхание пострадавшего.\n•	При отсутствии дыхания — начать искусственное дыхание и непрямой массаж сердца (30 нажатий + 2 вдоха).\n•	Остановить кровотечение (жгут, повязка, прижатие).\n•	При переломах — зафиксировать конечность подручными средствами.\n•	Не перемещать пострадавшего без крайней необходимости.",
#     },
# ]


main_med = [
    {
        "name": "🔸 1. Немного теории",
        "description": f"Первая помощь при ДТП — это действия, направленные на спасение жизни и здоровья пострадавших до приезда медиков.\n\nСвоевременная помощь и соблюдение мер безопасности могут спасти жизнь и снизить тяжесть последствий ДТП.",
    },
    {
        "name": "🔸 2. Обязанности водителя",
        "description": f"•	Остановиться и включить аварийную сигнализацию.\n•	Оценить обстановку и исключить опасность (пожар, взрыв, движение машин).\n•	Вызвать скорую помощь и полицию.",
    },
    {
        "name": "🔸 3. Основы оказания помощи",
        "description": f"•	Проверить сознание и дыхание пострадавшего.\n•	При отсутствии дыхания — начать искусственное дыхание и непрямой массаж сердца (30 нажатий + 2 вдоха).\n•	Остановить кровотечение (жгут, повязка, прижатие).\n•	При переломах — зафиксировать конечность подручными средствами.\n•	Не перемещать пострадавшего без крайней необходимости.",
    },
]


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

def get_med_text(theory, index, total):
    return f"*{theory['name']}*\n\n{theory['description']}\n\nТеория {index + 1} из {total}"

user_message_ids = {}


def get_med_keyboard(index, total):
    buttons = []

    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"med_{index - 1}"))

    if index < total - 1:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"med_{index + 1}"))

    if index == total - 1:
        buttons.append(InlineKeyboardButton("Перейти к тесту", callback_data=f"start_test"))

    # Кнопка "В меню"
    buttons.append(InlineKeyboardButton("🔙 В меню", callback_data="back_to_topics"))

    return InlineKeyboardMarkup([buttons])


async def show_med(update, context: ContextTypes.DEFAULT_TYPE, index: int):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if index < 0 or index >= len(main_med):
        await context.bot.send_message(chat_id, "❗ Некорректный номер страницы.")
        return

    theory = main_med[index]
    text = get_med_text(theory, index, len(main_med))
    keyboard = get_med_keyboard(index, len(main_med))

    # Удаляем предыдущее сообщение, если было
    if user_id in user_message_ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=user_message_ids[user_id])
        except:
            pass

    # Отправляем текст
    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

    user_message_ids[user_id] = sent.message_id


# Обработчик кнопок: "Далее", "Назад", "В меню"
async def handle_med_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("med_"):
        try:
            index = int(data.split("_")[1])
            await show_med(update, context, index)
        except ValueError:
            await query.edit_message_text("Ошибка: неправильный формат данных.")
    elif data == "back_to_topics":
        # Возврат в список тем (можно заменить на вызов своей функции)
        from main import get_topics_keyboard
        chat_id = query.message.chat_id
        await context.bot.send_message(
            chat_id=chat_id,
            text="📚 Вот список тем:",
            reply_markup=get_topics_keyboard()
        )