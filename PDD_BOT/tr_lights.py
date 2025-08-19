from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
import os
import random


main_lights = [
    {
        "name": "🔸 1. Немного теории",
        "description": f"Светофор регулирует движение с помощью сигналов:\n•	Зелёный — движение разрешено.\n•	Жёлтый — движение запрещено, но если начал пересекать перекрёсток — можно завершить манёвр.\n•	Красный — движение запрещено.\n•	Зелёная стрелка на доп. секции — разрешает движение в указанном направлении при включённом основном сигнале.\n•	Мигающий жёлтый — перекрёсток нерегулируемый, действует правило приоритета.",
    },
    {
        "name": "🔸 2. Стрелки в светофоре",
        "description": f"	•	Показывают разрешённые направления движения.\n•	При горящей стрелке можно ехать только в указанную сторону.",
    },
    {
        "name": "🔸 3. Основные сигналы регулировщика:",
        "description": f"	•	Руки вытянуты в стороны или опущены вниз — ехать нельзя, поперечное направление имеет приоритет.\n•	Рука вытянута вперёд — со спины и груди движение запрещено, слева и справа — разрешено прямо и направо.\n•	Круговое движение рукой — означает требование ускорить выезд с перекрёстка.\nЗапомни:\n\nЕсли есть регулировщик — выполняй только его команды, даже если светофор показывает другое.",
    },
]


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

def get_lights_text(theory, index, total):
    return f"*{theory['name']}*\n\n{theory['description']}\n\nТеория {index + 1} из {total}"

user_message_ids = {}


def get_lights_keyboard(index, total):
    buttons = []

    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"lights_{index - 1}"))

    if index < total - 1:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"lights_{index + 1}"))

    if index == total - 1:
        buttons.append(InlineKeyboardButton("Перейти к тесту", callback_data=f"start_test"))

    # Кнопка "В меню"
    buttons.append(InlineKeyboardButton("🔙 В меню", callback_data="back_to_topics"))

    return InlineKeyboardMarkup([buttons])


async def show_lights(update, context: ContextTypes.DEFAULT_TYPE, index: int):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if index < 0 or index >= len(main_lights):
        await context.bot.send_message(chat_id, "❗ Некорректный номер страницы.")
        return

    theory = main_lights[index]
    text = get_lights_text(theory, index, len(main_lights))
    keyboard = get_lights_keyboard(index, len(main_lights))

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
async def handle_lights_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("lights_"):
        try:
            index = int(data.split("_")[1])
            await show_lights(update, context, index)
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