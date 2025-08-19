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

# ---------- Вход в режим экзамена ----------
async def start_exam_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1-10 билеты", callback_data="exam_range_1_10")],
        [InlineKeyboardButton("11-20 билеты", callback_data="exam_range_11_20")],
        [InlineKeyboardButton("21-30 билеты", callback_data="exam_range_21_30")],
        [InlineKeyboardButton("31-40 билеты", callback_data="exam_range_31_40")],
    ]
    await update.message.reply_text(
        "📚 Выберите диапазон билетов:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


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


# ---------- Выбор билета ----------
async def select_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    ticket_number = int(query.data.split("_")[2])
    context.user_data["exam_ticket"] = ticket_number
    context.user_data["exam_question_index"] = 0
    context.user_data["exam_errors"] = []

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
    question_index = context.user_data.get("exam_question_index", 0)

    if ticket_number is None:
        await query.message.reply_text("Ошибка: номер билета не выбран.")
        return

    await send_exam_question(query.message.chat_id, ticket_number, question_index, context)


# ---------- Отправка вопроса ----------
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
                [InlineKeyboardButton("🎫 Билеты", callback_data="exam_range_1_10")],
                [InlineKeyboardButton("📋 В меню", callback_data="exam_to_menu")]
            ]
            await context.bot.send_message(
                chat_id,
                "🎉 Поздравляем, вы прошли тест без ошибок!\nХотите решить другой билет?",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

        elif len(errors) in [1, 2]:
            # ❌ Есть ошибки → даём доп. вопросы из следующего билета
            extra_questions = 5 if len(errors) == 1 else 10
            next_ticket_number = ticket_number + 1

            # Проверяем, что следующий билет есть
            next_ticket = next((t for t in tickets_data if t["ticket_number"] == next_ticket_number), None)
            if next_ticket:
                await context.bot.send_message(
                    chat_id,
                    f"❌ Вы допустили {len(errors)} ошибку(и).\n"
                    f"Вам добавлено {extra_questions} вопросов из билета {next_ticket_number}."
                )
                context.user_data["exam_ticket"] = next_ticket_number
                context.user_data["exam_question_index"] = 0
                context.user_data["exam_extra_limit"] = extra_questions
                await send_exam_question(chat_id, next_ticket_number, 0, context)
                return
            else:
                await context.bot.send_message(chat_id, "Все билеты закончились. Экзамен завершён ✅")
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

    print('Selected ticket:', ticket_number)
    print('Displayed question:', question_index)


# ---------- Обработка ответа ----------
async def handle_exam_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    ticket_number = context.user_data.get("exam_ticket")
    question_index = context.user_data.get("exam_question_index", 0) 
    errors = context.user_data.get("exam_errors", [])

    correct_answer = answers[((ticket_number - 1) * 20) + question_index]
    user_answer = query.data.split("_")[2]

    print("Правильный ответ:", correct_answer)
    print(ticket_number, question_index)
    print("Ответ пользователя:", user_answer)

    if user_answer == correct_answer:
        context.user_data["exam_question_index"] += 1
        # Проверка лимита для дополнительных вопросов
        if "exam_extra_limit" in context.user_data:
            if context.user_data["exam_question_index"] >= context.user_data["exam_extra_limit"]:
                await query.message.reply_text("Экзамен завершен ✅")
                return
        await send_exam_question(query.message.chat_id, ticket_number, context.user_data["exam_question_index"], context)
    else:
        errors.append((question_index + 1, correct_answer))
        context.user_data["exam_errors"] = errors

        if len(errors) < 2:
            await query.message.reply_text(
                f"❌ Ошибка! Правильный ответ: {correct_answer}\n"
                f"Добавлено 5 вопросов и 5 минут времени."
            )
            context.user_data["exam_question_index"] += 1
            await send_exam_question(query.message.chat_id, ticket_number, context.user_data["exam_question_index"], context)
        else:
            await query.message.reply_text("🚫 Лимит ошибок исчерпан. Экзамен завершен.")
# ---------- Возврат в меню ----------
async def exam_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text("📚 Вы вернулись в меню экзамена.")
    await start_exam_mode(update, context)