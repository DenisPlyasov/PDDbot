from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
import os
import random


main_rules = [
    {
        "name": "🔸 1. Общие требования",
        "description": f"- Участники дорожного движения обязаны знать и соблюдать ПДД. - На дорогах действует правостороннее движение. - Водитель обязан быть внимательным, не отвлекаться и контролировать ТС. - Запрещено управлять в состоянии опьянения, утомления или болезни.",
    },
    {
        "name": "🔸 2. Обязанности водителя",
        "description":     "- Иметь при себе:\n"
    "  - Водительское удостоверение.\n"
    "  - Регистрационные документы на ТС.\n"
    "  - Страховой полис ОСАГО.\n"
    "- Перед началом движения проверить:\n"
    "  - Исправность тормозов, рулевого, света и сигналов.\n"
    "- При ДТП:\n"
    "  - Остановиться, включить аварийку, выставить знак аварийной остановки.\n"
    "  - Не трогать ТС и вызвать полицию, если есть пострадавшие или ущерб.",
    },
    {
        "name": "🔸 3. Обязанности пассажиров",
        "description":     "- При движении быть пристёгнутыми ремнями безопасности.\n"
    "- Не отвлекать водителя и не мешать управлению ТС.",
    },
    {
        "name": "🔸 4. Обязанности пешеходов",
        "description": "- Двигаться по тротуару или обочине.\n"
    "- Переходить дорогу по переходу или на зелёный сигнал светофора.\n"
    "- Быть внимательными и не выходить на проезжую часть внезапно.",
    },
    {
        "name": "🔸 5. Световой режим\n",
        "description":     "- Фары ближнего света обязательны вне населённых пунктов — в любое время суток.\n"
    "- В тумане, дождь, снег — использовать противотуманные фары.\n"
    "- Аварийка включается:\n"
    "  - При вынужденной остановке в неположенном месте.\n"
    "  - При ДТП.",
    },
    {
        "name": "🔸 6. Опознавательные знаки\n",
        "description": "- «Начинающий водитель» — при стаже менее 2 лет.\n"
    "- «Шипы» — если установлены.\n"
    "- «Инвалид» — только при наличии подтверждающих документов.",
    },
    {
        "name": "🔸 7. Особенности перевозок\n",
        "description":     "- Перевозка детей:\n"
    "  - До 7 лет — только в автокресле.\n"
    "  - От 7 до 12 — допускается ремень безопасности на заднем сиденье.\n"
    "- Запрещено перевозить людей в непредназначенных местах или без фиксации.",
    },
]

pages_main_rules = [
    "🔸 4. Обязанности пешеходов\n"
    "- Двигаться по тротуару или обочине.\n"
    "- Переходить дорогу по переходу или на зелёный сигнал светофора.\n"
    "- Быть внимательными и не выходить на проезжую часть внезапно.",

    "🔸 5. Световой режим\n"
    "- Фары ближнего света обязательны вне населённых пунктов — в любое время суток.\n"
    "- В тумане, дождь, снег — использовать противотуманные фары.\n"
    "- Аварийка включается:\n"
    "  - При вынужденной остановке в неположенном месте.\n"
    "  - При ДТП.",

    "🔸 6. Опознавательные знаки\n"
    "- «Начинающий водитель» — при стаже менее 2 лет.\n"
    "- «Шипы» — если установлены.\n"
    "- «Инвалид» — только при наличии подтверждающих документов.",

    "🔸 7. Особенности перевозок\n"
    "- Перевозка детей:\n"
    "  - До 7 лет — только в автокресле.\n"
    "  - От 7 до 12 — допускается ремень безопасности на заднем сиденье.\n"
    "- Запрещено перевозить людей в непредназначенных местах или без фиксации.",
]


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from theory import pages_main_rules

def get_theory_text(theory, index, total):
    return f"*{theory['name']}*\n\n{theory['description']}\n\nТеория {index + 1} из {total}"

user_message_ids = {}


def get_theory_keyboard(index, total):
    buttons = []

    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"theory_{index - 1}"))

    if index < total - 1:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"theory_{index + 1}"))

    if index == total - 1:
        buttons.append(InlineKeyboardButton("Перейти к тесту", callback_data=f"start_test"))

    # Кнопка "В меню"
    buttons.append(InlineKeyboardButton("🔙 В меню", callback_data="back_to_topics"))

    return InlineKeyboardMarkup([buttons])


async def show_theory(update, context: ContextTypes.DEFAULT_TYPE, index: int):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if index < 0 or index >= len(main_rules):
        await context.bot.send_message(chat_id, "❗ Некорректный номер страницы.")
        return

    theory = main_rules[index]
    text = get_theory_text(theory, index, len(main_rules))
    keyboard = get_theory_keyboard(index, len(main_rules))

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
async def handle_theory_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("theory_"):
        try:
            index = int(data.split("_")[1])
            await show_theory(update, context, index)
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