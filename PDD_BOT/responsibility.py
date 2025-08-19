from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
import os
import random


main_responsibilities = [
    {
        "name": "🔸 1. Немного теории",
        "description": f"Ответственность наступает за нарушение правил дорожного движения, которые Вы уже изучили. Не нарушайте - и все будет окей. Отвественность может быть административной и уголовной, так же предусмотрены штрафы за нарушения",
    },
    {
        "name": "🔸 2. Административная ответственность",
        "description": f"•  	Наступает за нарушение правил, не повлёкшее тяжких последствий. Может включать штрафы, лишение права управления, административный арест до 15 суток и изъятие запрещённых средств (например, спецсигналов)\n\n•  	Размеры штрафов зависят от конкретной статьи КоАП. Например, за вождение в нетрезвом состоянии — штраф и лишение прав, за превышение скорости — от предупреждения до нескольких тысяч рублей",
    },
    {
        "name": "🔸 3. Уголовная ответственность",
        "description": f"•	  Применяется при нарушениях ПДД, повлекших тяжкий вред здоровью или смерть человека.\n\n•  	Включает наказания вплоть до лишения свободы и лишения права управления транспортными средствами, как прописано в УК РФ, ст. 264 и др.",
    },
]


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

def get_responsibilities_text(theory, index, total):
    return f"*{theory['name']}*\n\n{theory['description']}\n\nТеория {index + 1} из {total}"

user_message_ids = {}


def get_responsibilities_keyboard(index, total):
    buttons = []

    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"responsibilities_{index - 1}"))

    if index < total - 1:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"responsibilities_{index + 1}"))

    if index == total - 1:
        buttons.append(InlineKeyboardButton("Перейти к тесту", callback_data=f"start_test"))

    # Кнопка "В меню"
    buttons.append(InlineKeyboardButton("🔙 В меню", callback_data="back_to_topics"))

    return InlineKeyboardMarkup([buttons])


async def show_responsibilities(update, context: ContextTypes.DEFAULT_TYPE, index: int):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if index < 0 or index >= len(main_responsibilities):
        await context.bot.send_message(chat_id, "❗ Некорректный номер страницы.")
        return

    theory = main_responsibilities[index]
    text = get_responsibilities_text(theory, index, len(main_responsibilities))
    keyboard = get_responsibilities_keyboard(index, len(main_responsibilities))

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
async def handle_responsibilities_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("responsibilities_"):
        try:
            index = int(data.split("_")[1])
            await show_responsibilities(update, context, index)
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