from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import datetime

# --- меню напоминаний ---
async def start_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔔 Напоминания - ключ к стабильному прогрессу!\n\n"
        "Выберите свободное время, в которое хотели бы получать напоминалку о том, "
        "что надо выучить новый материал и получайте постоянный прогресс!\n\n"
        "Главное - включить уведомления от бота и не игнорировать их — "
        "обещаем, никакой рекламы мы не присылаем 🙂",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📅 Выбрать день", callback_data="remind_choose_day")],
            [InlineKeyboardButton("🔕 Отключить напоминания", callback_data="remind_disable")],
            [InlineKeyboardButton("📋 В меню", callback_data="to_menu")]
        ])
    )

# --- выбор дней ---
async def choose_days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if "remind_days" not in context.user_data:
        context.user_data["remind_days"] = set()

    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    keyboard = []

    for d in days:
        mark = "✅" if d in context.user_data["remind_days"] else ""
        keyboard.append([InlineKeyboardButton(f"{d} {mark}", callback_data=f"toggle_day_{d}")])

    keyboard.append([InlineKeyboardButton("⏰ Выбрать время", callback_data="remind_choose_time")])
    keyboard.append([InlineKeyboardButton("📋 В меню", callback_data="to_menu")])

    await query.message.edit_text(
        "Выберите дни недели, когда хотите получать напоминания:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- переключение дня ---
async def toggle_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    day = query.data.replace("toggle_day_", "")

    if "remind_days" not in context.user_data:
        context.user_data["remind_days"] = set()

    if day in context.user_data["remind_days"]:
        context.user_data["remind_days"].remove(day)
    else:
        context.user_data["remind_days"].add(day)

    await choose_days(update, context)

# --- выбор времени ---
async def choose_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    times = [f"{h:02d}:00" for h in range(10, 23)]
    keyboard = []

    for t in times:
        keyboard.append([InlineKeyboardButton(t, callback_data=f"set_time_{t}")])

    keyboard.append([InlineKeyboardButton("📋 В меню", callback_data="to_menu")])

    await query.message.edit_text(
        "Выберите время, в которое хотите получать напоминания:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- установка времени ---
async def set_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    time_str = query.data.replace("set_time_", "")
    context.user_data["remind_time"] = time_str

    days = ", ".join(context.user_data.get("remind_days", []))
    text = (
        f"✅ Отлично! Вы выбрали дни: {days}\n"
        f"⏰ Время: {time_str}\n\n"
        f"Теперь вы будете получать напоминания!"
    )

    await query.message.edit_text(text)

    # передаём и chat_id, и context
    await schedule_notifications(update.effective_chat.id, context)

# --- постановка задач ---
async def schedule_notifications(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    days = context.user_data.get("remind_days", [])
    time_str = context.user_data.get("remind_time")
    job_queue = getattr(context.application, "job_queue", None)

    if not days or not time_str or not job_queue:
        return

    # очищаем старые задачи
    for job in job_queue.get_jobs_by_name(f"reminder_{chat_id}"):
        job.schedule_removal()

    hour, minute = map(int, time_str.split(":"))
    day_map = {"Пн": 0, "Вт": 1, "Ср": 2, "Чт": 3, "Пт": 4, "Сб": 5, "Вс": 6}

    for day in days:
        job_queue.run_daily(
            send_reminder,
            time=datetime.time(hour, minute),
            days=(day_map[day],),
            chat_id=chat_id,
            name=f"reminder_{chat_id}"
        )

# --- отключение напоминаний ---
async def disable_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    job_queue = getattr(context.application, "job_queue", None)

    if job_queue:
        jobs = job_queue.get_jobs_by_name(f"reminder_{chat_id}")
        for job in jobs:
            job.schedule_removal()

    # чистим user_data
    context.user_data.pop("remind_days", None)
    context.user_data.pop("remind_time", None)

    await query.message.edit_text(
        "🔕 Напоминания отключены.\n"
        "Вы всегда можете снова включить их через меню."
    )

# --- отправка уведомления ---
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        context.job.chat_id,
        "📖 Пора выучить новую тему ПДД! Вперёд к знаниям!"
    )