from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
import os
import random


main_weather = [
    {
        "name": "🔸 1. Немного теории",
        "description": f"Плохая погода — это дождь, снег, туман, гололёд, сильный ветер или недостаточная видимость (менее 300 м).\nГлавная задача в плохую погоду — обеспечить максимальную безопасность себе и другим участникам движения.",
    },
    {
        "name": "🔸 2. Если ты попал в аварию, сделай следующее:",
        "description": f"•	Снизь скорость и увеличь дистанцию до впереди идущих автомобилей.\n•	Включи ближний свет фар или противотуманные фары.\n•	Избегай резких манёвров — торможение и повороты выполняй плавно.\n•	На скользкой дороге используй торможение двигателем и плавное нажатие на педали.\n•	В сильный боковой ветер держи руль крепче, особенно при обгоне и выезде из-за укрытий.\nn•	В тумане и снегопаде ориентируйся по разметке и краю проезжей части.",
    },
    {
        "name": "🔸 3. Особенности",
        "description": f"•	При гололёде тормозной путь может увеличиваться в 3–5 раз.\n•	В дождь и снег избегай луж и снежной каши — возможен аквапланинг или занос.\n•	При ухудшении видимости до нуля (сильный туман, метель) лучше остановиться в безопасном месте и переждать.",
    },
]


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

def get_weather_text(theory, index, total):
    return f"*{theory['name']}*\n\n{theory['description']}\n\nТеория {index + 1} из {total}"

user_message_ids = {}


def get_weather_keyboard(index, total):
    buttons = []

    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"weather_{index - 1}"))

    if index < total - 1:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"weather_{index + 1}"))

    if index == total - 1:
        buttons.append(InlineKeyboardButton("Перейти к тесту", callback_data=f"start_test"))

    # Кнопка "В меню"
    buttons.append(InlineKeyboardButton("🔙 В меню", callback_data="back_to_topics"))

    return InlineKeyboardMarkup([buttons])


async def show_weather(update, context: ContextTypes.DEFAULT_TYPE, index: int):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if index < 0 or index >= len(main_weather):
        await context.bot.send_message(chat_id, "❗ Некорректный номер страницы.")
        return

    theory = main_weather[index]
    text = get_weather_text(theory, index, len(main_weather))
    keyboard = get_weather_keyboard(index, len(main_weather))

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
async def handle_weather_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("weather_"):
        try:
            index = int(data.split("_")[1])
            await show_weather(update, context, index)
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