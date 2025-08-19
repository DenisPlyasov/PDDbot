from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
import os
import random


main_railways = [
    {
        "name": "🔸 1. Немного теории",
        "description": f"Железнодорожный переезд — это место пересечения дороги с ж/д путями.\nНа переезде действует повышенная опасность, и правила проезда строго регламентированы.",
    },
    {
        "name": "🔸 2. Запрещён проезд через переезд, если:",
        "description": f"•	Закрыт или опускается шлагбаум.\n•	Горит красный сигнал светофора.\n•	Есть приближающийся поезд или дежурный подал сигнал “стоп”.\n•	Машина не успеет проехать полностью (образуется затор).",
    },
    {
        "name": "🔸 3. Обязанности водителя перед переездом:",
        "description": f"•	Снизить скорость.\n•	Убедиться в безопасности.\n•	Остановиться при необходимости у стоп-линии, знака «Стоп», светофора или шлагбаума.\n•	При неисправности автомобиля на путях — немедленно освободить переезд и сообщить дежурному.",
    },
    {
        "name": "🔸 4. Проезд трамвайных путей:",
        "description": f"•	На регулируемых перекрёстках трамвай подчиняется светофору.\n•	На нерегулируемых перекрёстках:\n   •	Трамвай на главной — уступи.\n   •	 При равнозначных дорогах — трамвай имеет преимущество, даже если поворачивает.\n•	Разрешён объезд трамвая справа, а слева — только при отсутствии помех и если это не запрещено знаками/разметкой.",
    },
    {
        "name": "🔸 5. Особенности",
        "description": f"•	При наличии знаков «Пешеходная дорожка» или «Велопешеходная дорожка» все участники обязаны следовать по ним.\n•	Велосипедистам запрещено ездить по автомагистралям, тротуарам (взрослым), обочинам без крайней необходимости.",
    },
]


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

def get_railways_text(theory, index, total):
    return f"*{theory['name']}*\n\n{theory['description']}\n\nТеория {index + 1} из {total}"

user_message_ids = {}


def get_railways_keyboard(index, total):
    buttons = []

    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"railways_{index - 1}"))

    if index < total - 1:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"railways_{index + 1}"))

    if index == total - 1:
        buttons.append(InlineKeyboardButton("Перейти к тесту", callback_data=f"start_test"))

    # Кнопка "В меню"
    buttons.append(InlineKeyboardButton("🔙 В меню", callback_data="back_to_topics"))

    return InlineKeyboardMarkup([buttons])


async def show_railways(update, context: ContextTypes.DEFAULT_TYPE, index: int):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if index < 0 or index >= len(main_railways):
        await context.bot.send_message(chat_id, "❗ Некорректный номер страницы.")
        return

    theory = main_railways[index]
    text = get_railways_text(theory, index, len(main_railways))
    keyboard = get_railways_keyboard(index, len(main_railways))

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
async def handle_railways_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("railways_"):
        try:
            index = int(data.split("_")[1])
            await show_railways(update, context, index)
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