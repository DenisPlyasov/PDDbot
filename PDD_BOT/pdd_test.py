import json
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputFile, Update
from telegram.ext import ContextTypes


import json
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from telegram import Update

# Загружаем вопросы
with open("PDD_BOT/tickets.json", "r", encoding="utf-8") as f:
    tickets_data = json.load(f)

# Путь к папке с картинками
IMAGE_PATH = "PDD_BOT/pictures/test"

# Список правильных ответов (по условию — номер вопроса * номер билета)
answers = ['2', '1', '1', '4', '2', '2', '4', '3', '1', '3', '1', '3', '3', '1', '3', '4', '3', '4', '3', '2', '2', '1', '1', '3', '3', '1', '3', '3', '1', '3', '3', '2', '3', '3', '1', '3', '2', '1', '3', '3', '1', '3', '3', '2', '2', '3', '2', '1', '3', '1', '3', '2', '2', '1', '3', '3', '4', '2', '3', '3', '2', '2', '1', '1', '2', '1', '1', '2', '2', '1', '1', '2', '3', '3', '2', '4', '1', '4', '1', '2', '1', '2', '1', '1', '3', '1', '3', '3', '2', '3', '1', '2', '2', '1', '1', '3', '2', '1', '2', '1', '3', '2', '3', '3', '2', '1', '1', '2', '3', '3', '1', '3', '3', '2', '2', '3', '3', '4', '1', '2', '1', '2', '1', '2', '2', '2', '1', '3', '2', '2', '1', '3', '2', '2', '3', '3', '3', '3', '2', '2', '2', '3', '3', '1', '1', '3', '1', '2', '3', '3', '2', '1', '1', '2', '2', '3', '2', '1', '1', '2', '2', '2', '1', '3', '1', '2', '2', '1', '3', '2', '3', '3', '2', '2', '3', '3', '4', '3', '2', '2', '2', '1', '3', '3', '2', '1', '1', '2', '1', '3', '2', '2', '3', '3', '3', '3', '2', '4', '3', '1', '2', '1', '3', '2', '3', '3', '1', '1', '2', '3', '3', '1', '1', '2', '1', '2', '3', '2', '3', '2', '2', '3', '2', '1', '2', '3', '2', '1', '3', '2', '2', '3', '2', '3', '3', '3', '2', '2', '1', '3', '3', '2', '3', '2', '3', '1', '1', '3', '2', '3', '3', '3', '1', '3', '2', '2', '1', '2', '3', '2', '1', '2', '2', '3', '2', '1', '1', '3', '1', '2', '1', '1', '3', '3', '2', '2', '1', '3', '1', '3', '4', '2', '3', '3', '4', '1', '1', '3', '1', '2', '3', '1', '3', '2', '1', '2', '4', '3', '2', '2', '4', '2', '2', '2', '3', '2', '3', '2', '3', '2', '1', '1', '2', '1', '3', '2', '3', '2', '1', '2', '1', '1', '2', '2', '3', '1', '2', '3', '2', '2', '3', '2', '1', '1', '2', '4', '3', '2', '3', '1', '1', '3', '1', '2', '2', '2', '3', '2', '2', '3', '3', '2', '3', '3', '2', '3', '2', '2', '3', '3', '2', '3', '1', '3', '2', '2', '3', '1', '1', '3', '3', '3', '2', '1', '3', '1', '2', '3', '1', '3', '4', '1', '3', '2', '2', '3', '1', '3', '2', '2', '3', '1', '3', '2', '3', '1', '2', '1', '2', '2', '2', '3', '1', '3', '3', '3', '1', '3', '2', '3', '2', '3', '3', '3', '2', '4', '3', '2', '1', '2', '1', '2', '2', '3', '2', '3', '1', '2', '3', '4', '2', '1', '1', '3', '2', '3', '2', '2', '3', '1', '2', '1', '2', '2', '3', '2', '1', '1', '3', '3', '3', '3', '2', '2', '2', '1', '3', '2', '3', '3', '3', '2', '1', '2', '2', '2', '2', '3', '2', '3', '3', '2', '1', '3', '3', '2', '1', '2', '2', '3', '1', '3', '1', '2', '4', '2', '1', '2', '3', '3', '3', '3', '1', '3', '2', '3', '2', '4', '3', '1', '3', '2', '2', '1', '2', '2', '1', '2', '3', '2', '3', '2', '2', '3', '2', '2', '1', '3', '2', '2', '2', '1', '1', '3', '3', '3', '2', '1', '1', '2', '2', '3', '3', '2', '2', '2', '2', '3', '1', '3', '1', '1', '3', '3', '1', '3', '3', '2', '1', '2', '1', '3', '3', '1', '1', '1', '2', '2', '4', '4', '3', '2', '1', '3', '1', '2', '1', '1', '2', '3', '3', '4', '3', '1', '3', '2', '4', '3', '2', '3', '1', '2', '2', '2', '3', '2', '3', '1', '3', '2', '3', '3', '3', '2', '4', '3', '1', '3', '1', '2', '4', '1', '1', '2', '4', '2', '1', '1', '3', '2', '1', '1', '1', '2', '4', '3', '2', '3', '3', '2', '2', '2', '1', '4', '3', '3', '1', '3', '4', '4', '3', '1', '3', '2', '3', '3', '2', '3', '1', '1', '2', '1', '3', '2', '3', '1', '3', '1', '4', '4', '3', '3', '4', '2', '3', '1', '2', '3', '2', '3', '3', '2', '2', '2', '1', '3', '1', '2', '3', '2', '3', '3', '1', '2', '1', '2', '3', '3', '2', '3', '3', '3', '2', '3', '1', '2', '3', '2', '3', '1', '2', '3', '3', '2', '2', '1', '1', '3', '3', '2', '1', '2', '1', '3', '3', '2', '1', '3', '1', '3', '2', '2', '3', '3', '2', '3', '3', '2', '3', '1', '2', '3', '2', '3', '1', '1', '3', '1', '3', '3', '1', '3', '2', '3', '2', '3', '3', '2', '3', '2', '2', '2', '2', '3', '1', '3', '2', '4', '2', '1', '2', '2', '3', '3', '2', '1', '3', '3', '2', '2', '3', '2', '2', '4', '3', '3', '3', '1', '2', '3', '1', '3', '3', '1', '2', '2', '2', '3', '2', '1', '1', '1', '3', '1', '2', '3', '1', '3', '1', '3', '1', '1', '4', '2', '3', '3', '1', '4', '1', '3']


# --- универсальная функция для вывода меню диапазонов ---
async def send_exam_ranges(message):
    keyboard = [
        [
            InlineKeyboardButton("1-10", callback_data="exam_range_1_10"),
            InlineKeyboardButton("11-20", callback_data="exam_range_11_20"),
        ],
        [
            InlineKeyboardButton("21-30", callback_data="exam_range_21_30"),
            InlineKeyboardButton("31-40", callback_data="exam_range_31_40"),
        ],
    ]
    await message.reply_text(
        "Выберите диапазон билетов:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# --- старое меню экзамена ---
async def start_exam_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # если вызвали из /start или "в меню"
    if update.message:
        await send_exam_ranges(update.message)
    # если вызвали из callback_query
    elif update.callback_query:
        await send_exam_ranges(update.callback_query.message)


# --- обработчик кнопки "Билеты" ---
async def exam_all_ranges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await send_exam_ranges(query.message)

# ---------- Обработка диапазона ----------
async def select_ticket_range(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, _, start, end = query.data.split("_")
    start, end = int(start), int(end)

    keyboard = []
    row = []
    for i in range(start, end + 1):
        row.append(InlineKeyboardButton(str(i), callback_data=f"exam_ticket_{i}"))
        if len(row) == 5:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    await query.message.edit_text(
        f"Выберите билет {start}-{end}:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# --- Утилита: сброс состояния доп. вопросов/ошибок ---
def _reset_extra_state(context):
    context.user_data.pop("exam_extra_limit", None)
    context.user_data["exam_errors"] = []


# ---------- Выбор билета ----------
async def select_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    ticket_number = int(query.data.split("_")[2])

    # Сбрасываем состояние при выборе нового билета
    _reset_extra_state(context)

    context.user_data["exam_ticket"] = ticket_number
    context.user_data["exam_question_index"] = 0

    keyboard = [
        [
            InlineKeyboardButton("✅ Начать экзамен", callback_data="start_exam"),
            InlineKeyboardButton("📋 В меню", callback_data="exam_to_menu")
        ]
    ]

    await query.message.edit_text(
        "На решение билета у вас есть 20 минут.\n"
        "За каждую ошибку добавляем 5 вопросов и 5 минут.\n"
        "Максимум 2 ошибки.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------- Запуск экзамена ----------
async def start_exam_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    ticket_number = context.user_data.get("exam_ticket")

    # При старте экзамена тоже чистим хвосты
    _reset_extra_state(context)
    context.user_data["exam_question_index"] = 0

    if ticket_number is None:
        await query.message.reply_text("Ошибка: номер билета не выбран.")
        return

    await send_exam_question(query.message.chat_id, ticket_number, 0, context)


import random

# ---------- Обработка ответа ----------
async def handle_exam_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    ticket_number = context.user_data.get("exam_ticket")
    question_index = context.user_data.get("exam_question_index", 0) 
    errors = context.user_data.get("exam_errors", [])

    correct_answer = answers[((ticket_number - 1) * 20) + question_index]
    user_answer = query.data.split("_")[2]

    if user_answer == correct_answer:
        context.user_data["exam_question_index"] += 1

        # ✅ Доп. режим (5 или 10 вопросов)
        if "exam_extra_limit" in context.user_data:
            if context.user_data["exam_question_index"] >= context.user_data["exam_extra_limit"]:
                # Успешно прорешаны все доп. вопросы → сбрасываем состояние
                _reset_extra_state(context)
                keyboard = [
                    [InlineKeyboardButton("🎫 Билеты", callback_data="start_exam")],
                    [InlineKeyboardButton("📋 В меню", callback_data="exam_to_menu")]
                ]
                await query.message.reply_text(
                    "✅ Дополнительные вопросы завершены.\nХотите решить другой билет?",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                return

        await send_exam_question(query.message.chat_id, ticket_number, context.user_data["exam_question_index"], context)

    else:
        errors.append((question_index + 1, correct_answer))
        context.user_data["exam_errors"] = errors

        # 🚫 Ограничение по ошибкам
        if len(errors) >= 3:
            _reset_extra_state(context)
            keyboard = [
                [InlineKeyboardButton("🎫 Билеты", callback_data="exam_all_ranges")],
                [InlineKeyboardButton("📋 В меню", callback_data="exam_to_menu")]
            ]
            await query.message.reply_text(
                f"Ошибка! Правильный ответ: {correct_answer}.\n\n🚫 Лимит ошибок исчерпан (3 ошибки). Экзамен завершён.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

        # ❌ Ошибка во время доп. вопросов → сразу конец
        if "exam_extra_limit" in context.user_data:
            _reset_extra_state(context)
            await query.message.reply_text("🚫 Ошибка в дополнительных вопросах. Экзамен завершён.")
            return

        # В обычном режиме показываем правильный ответ и идём дальше
        await query.message.reply_text(f"❌ Ошибка! Правильный ответ: {correct_answer}")
        context.user_data["exam_question_index"] += 1
        await send_exam_question(query.message.chat_id, ticket_number, context.user_data["exam_question_index"], context)



# ---------- Отправка вопроса ----------
async def send_exam_question(chat_id, ticket_number, question_index, context: ContextTypes.DEFAULT_TYPE):
    ticket_number = int(ticket_number)
    ticket = next(t for t in tickets_data if t["ticket_number"] == ticket_number)

    # Если все вопросы текущего билета пройдены
    if question_index >= len(ticket["questions"]):
        errors = context.user_data.get("exam_errors", [])

        if len(errors) == 0:
            # ✅ Успешное прохождение без ошибок
            keyboard = [
                [InlineKeyboardButton("🎫 Билеты", callback_data="exam_all_ranges")],
                [InlineKeyboardButton("📋 В меню", callback_data="exam_to_menu")]
            ]
            await context.bot.send_message(
                chat_id,
                "🎉 Поздравляем, вы прошли тест без ошибок!\nХотите решить другой билет?",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

        elif len(errors) in [1, 2]:
            # ❌ Есть ошибки → даём доп. вопросы из случайного билета
            extra_questions = 5 if len(errors) == 1 else 10

            # выбираем случайный билет, не равный текущему
            possible_tickets = [t["ticket_number"] for t in tickets_data if t["ticket_number"] != ticket_number]
            next_ticket_number = random.choice(possible_tickets)

            await context.bot.send_message(
                chat_id,
                f"❌ Вы допустили {len(errors)} ошибку(и).\n"
                f"Вам добавлено {extra_questions} вопросов из случайного билета №{next_ticket_number}."
            )
            context.user_data["exam_ticket"] = next_ticket_number
            context.user_data["exam_question_index"] = 0
            context.user_data["exam_extra_limit"] = extra_questions
            await send_exam_question(chat_id, next_ticket_number, 0, context)
            return

    # Берём вопрос по индексу
    question = ticket["questions"][question_index]
    text = f"Билет {ticket_number}, Вопрос {question['question_number']}:\n\n{question['text']}\n\n"
    for idx, ans in enumerate(question["answers"], 1):
        text += f"{idx}. {ans}\n"

    img_path = os.path.join(IMAGE_PATH, f"p{ticket_number}.{question['question_number']}.png")

    keyboard = [[
        InlineKeyboardButton(str(i + 1), callback_data=f"exam_answer_{i+1}")
        for i in range(len(question["answers"]))
    ]]
    keyboard.append([InlineKeyboardButton("📋 В меню", callback_data="exam_to_menu")])

    if os.path.exists(img_path):
        with open(img_path, "rb") as img:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=img,
                caption=text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def exam_all_ranges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await send_exam_ranges(query.message)


async def exam_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Чистим хвосты при выходе в меню
    _reset_extra_state(context)
    context.user_data.pop("exam_ticket", None)
    context.user_data.pop("exam_question_index", None)

    from main import get_topics_keyboard
    chat_id = query.message.chat_id
    await context.bot.send_message(
        chat_id=chat_id,
        text="📚 Вот список тем:",
        reply_markup=get_topics_keyboard()
    )

