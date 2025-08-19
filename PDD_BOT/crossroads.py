from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
import os
import random


main_rules = [
    {
        "name": "🔸 1. Базовые знания",
        "description": f"Что такое перекрёсток: Перекрёсток — место пересечения, примыкания или разветвления дорог на одном уровне, не считая выездов с прилегающих территорий.\n Главное правило:\n При проезде перекрёстков водитель обязан уступить дорогу в соответствии с приоритетами — по знакам, светофорам или общим правилам.",
    },
    {
        "name": "🔸 2. Типы перекрестков",
        "description": f"•	Регулируемые — движение регулируется светофором или регулировщиком.\n•	Нерегулируемые — нет ни светофора, ни регулировщика, проезд по приоритету.",
    },
    {
        "name": "🔸 3. Правила проезда регулируемых перекрестков",
        "description": f"	•	Действуй по сигналам светофора или указаниям регулировщика.\n •	При повороте налево уступи встречному транспорту.\n•	При разрешающем сигнале завершай манёвр даже на мигающий или красный.",
    },
    {
        "name": "🔸 4. Правила проезда нерегулируемых перекрестков",
        "description": f"•	Если есть знак “Главная дорога” — едь первым.\n •	Если ты на второстепенной — уступи всем на главной.\n •	Если все на равнозначных дорогах — уступи тому, кто справа (правило “помехи справа”).\n •	При повороте налево — уступи встречным.",
    },
    {
        "name": "🔸 5. Круговое движение",
        "description": f"•	При въезде уступи тем, кто уже на круге (если стоит знак «Уступи дорогу»).\n •	Следи за знаками — бывает, что главная дорога идёт по кругу или через круг.",
    },
    {
        "name": "🔸 6. Проезд с трамваем",
        "description": f"•	На равнозначных перекрёстках трамвай всегда имеет приоритет, даже при повороте.\n •	На регулируемых — действует по сигналу того же светофора, что и автомобили.",
    },

   
]


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from theory import pages_main_rules

def get_crossroad_text(theory, index, total):
    return f"*{theory['name']}*\n\n{theory['description']}\n\nТеория {index + 1} из {total}"

user_message_ids = {}


def get_crossroad_keyboard(index, total):
    buttons = []

    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"crossroad_{index - 1}"))

    if index < total - 1:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"crossroad_{index + 1}"))

    if index == total - 1:
        buttons.append(InlineKeyboardButton("Перейти к тесту", callback_data=f"start_test"))

    # Кнопка "В меню"
    buttons.append(InlineKeyboardButton("🔙 В меню", callback_data="back_to_topics"))

    return InlineKeyboardMarkup([buttons])


async def show_crossroad(update, context: ContextTypes.DEFAULT_TYPE, index: int):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if index < 0 or index >= len(main_rules):
        await context.bot.send_message(chat_id, "❗ Некорректный номер страницы.")
        return

    theory = main_rules[index]
    text = get_crossroad_text(theory, index, len(main_rules))
    keyboard = get_crossroad_keyboard(index, len(main_rules))

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
async def handle_crossroad_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("crossroad_"):
        try:
            index = int(data.split("_")[1])
            await show_crossroad(update, context, index)
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