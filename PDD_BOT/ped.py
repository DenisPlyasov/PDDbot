from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
import os
import random


main_ped = [
    {
        "name": "🔸 1. Права пешеходов",
        "description": f"•	Переходить дорогу можно только по пешеходному переходу.\n•	На регулируемом переходе — по зелёному сигналу.\n•	При отсутствии перехода — по кратчайшему пути перпендикулярно проезжей части, убедившись в безопасности.",
    },
    {
        "name": "🔸 2. Обязанности водителя перед пешеходами",
        "description": f"•	Уступить на пешеходных переходах (в том числе нерегулируемых).\n•	При повороте уступить пешеходам, переходящим дорогу, на которую поворачивает водитель.\n•	Снижать скорость при приближении к жилым зонам, остановкам и детским учреждениям.",
    },
    {
        "name": "🔸 3. Движение в жилой зоне",
        "description": f"•	Пешеходы имеют приоритет.\n•	Скорость автомобилей — не более 20 км/ч.",
    },
    {
        "name": "🔸 4. Велосипедист - тоже участник движения",
        "description": f"•	Должен двигаться по велодорожке или правому краю проезжей части.\n•	Детям до 14 лет — можно ехать по тротуару или пешеходной дорожке.\n•	Переезжать пешеходный переход на велосипеде нельзя — велосипедист обязан спешиться и перейти пешком.",
    },
    {
        "name": "🔸 5. Особенности",
        "description": f"•	При наличии знаков «Пешеходная дорожка» или «Велопешеходная дорожка» все участники обязаны следовать по ним.\n•	Велосипедистам запрещено ездить по автомагистралям, тротуарам (взрослым), обочинам без крайней необходимости.",
    },


   
]


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

def get_ped_text(theory, index, total):
    return f"*{theory['name']}*\n\n{theory['description']}\n\nТеория {index + 1} из {total}"

user_message_ids = {}


def get_ped_keyboard(index, total):
    buttons = []

    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"ped_{index - 1}"))

    if index < total - 1:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"ped_{index + 1}"))

    if index == total - 1:
        buttons.append(InlineKeyboardButton("Перейти к тесту", callback_data=f"start_test"))

    # Кнопка "В меню"
    buttons.append(InlineKeyboardButton("🔙 В меню", callback_data="back_to_topics"))

    return InlineKeyboardMarkup([buttons])


async def show_ped(update, context: ContextTypes.DEFAULT_TYPE, index: int):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if index < 0 or index >= len(main_ped):
        await context.bot.send_message(chat_id, "❗ Некорректный номер страницы.")
        return

    theory = main_ped[index]
    text = get_ped_text(theory, index, len(main_ped))
    keyboard = get_ped_keyboard(index, len(main_ped))

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
async def handle_ped_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("ped_"):
        try:
            index = int(data.split("_")[1])
            await show_ped(update, context, index)
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