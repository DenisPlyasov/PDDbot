from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
import os
import random

# Пример структуры данных
markings = [
    {
        "name": "1.1 Cплошная линия",
        "description": "разделяет транспортные потоки противоположных направлений и обозначает границы полос движения в опасных местах на дорогах; обозначает границы стояночных мест транспортных средств;",
        "image": "PDD_BOT/markings/r1.1.png"
    },
    {
        "name": "1.2 Толстая сплошная линия",
        "description": "обозначает край проезжей части или границы участков проезжей части, на которые въезд запрещен;",
        "image": "PDD_BOT/markings/r1.2.png"
    },
    {
        "name": "1.3 Двойная сплошная",
        "description": "разделяет транспортные потоки противоположных направлений на дорогах с четырьмя и более полосами для движения в обоих направлениях, с двумя или тремя полосами - при ширине полос более 3,75 м;",
        "image": "PDD_BOT/markings/r1.4.png"
    },
    {
        "name": "1.4 Желтая сплошная",
        "description": "обозначает места, где запрещена остановка транспортных средств",
        "image": "PDD_BOT/markings/r1.4.png"
    },
    {
        "name": "1.5 Прерывистая",
        "description": " разделяет транспортные потоки противоположных направлений на дорогах, имеющих две или три полосы; обозначает границы полос движения при наличии двух и более полос, предназначенных для движения в одном направлении;",
        "image": "PDD_BOT/markings/r1.5.png"
    },
    {
        "name": "1.6 Линия предупреждения",
        "description": "предупреждает о приближении к разметке 1.1  или 1.11 , которая разделяет транспортные потоки противоположных или попутных направлений;",
        "image": "PDD_BOT/markings/r1.6.png"
    },
    {
        "name": "1.7 Короткая прерывистая",
        "description": "обозначает полосы движения в пределах перекрестка или зону парковки. Разметка синего цвета обозначает, что зона парковки используется на платной основе;",
        "image": "PDD_BOT/markings/r1.7.png"
    },
    {
        "name": "1.8 Широкая прерывистая",
        "description": "обозначает границы полос движения, на которых осуществляется реверсивное регулирование; разделяет транспортные потоки противоположных направлений (при выключенных реверсивных светофорах) на дорогах, где осуществляется реверсивное регулирование;",
        "image": "PDD_BOT/markings/r1.8.png"
    },
    {
        "name": "1.9 Двойная прерывистая ",
        "description": "обозначает границы полос движения, на которых осуществляется реверсивное регулирование; разделяет транспортные потоки противоположных направлений (при выключенных реверсивных светофорах) на дорогах, где осуществляется реверсивное регулирование;",
        "image": "PDD_BOT/markings/r1.9.png"
    },
    {
        "name": "1.10 Желтая прерывистая",
        "description": " (цвет - желтый) - обозначает места, где запрещена стоянка транспортных средств;",
        "image": "PDD_BOT/markings/r1.10.png"
    },
    {
        "name": "1.11 Сплошная и прерывистая ",
        "description": "разделяет транспортные потоки противоположных или попутных направлений на участках дорог, где перестроение разрешено только из одной полосы; обозначает места, где необходимо разрешить движение только со стороны прерывистой линии (в местах разворота, въезда и выезда с прилегающей территории);",
        "image": "PDD_BOT/markings/r1.11.png"
    },
    {
        "name": "1.12 Стоп-линия ",
        "description": "указывает место, где водитель должен остановиться при наличии знака 2.5  или при запрещающем сигнале светофора (регулировщика);",
        "image": "PDD_BOT/markings/r1.12.png"
    },
    {
        "name": "1.13 Линия 'Уступи Дорогу'",
        "description": "указывает место, где водитель должен при необходимости остановиться, уступая дорогу транспортным средствам, движущимся по пересекаемой дороге;",
        "image": "PDD_BOT/markings/r1.13.png"
    },
    {
        "name": "1.14.1 - 1.14.2 Пешеходный переход",
        "description": "обозначает пешеходный переход; стрелы разметки 1.14.2  указывают направление движения пешеходов;",
        "image": "PDD_BOT/markings/r1.14.1.png"
    },
    {
        "name": "1.14.3 Диагональный пешеходный переход",
        "description": "обозначает пешеходный переход; стрелы разметки 1.14.2  указывают направление движения пешеходов;",
        "image": "PDD_BOT/markings/r1.14.3.png"
    },
    {
        "name": "1.15 Пересекающая",
        "description": "обозначает место, где велосипедная дорожка пересекает проезжую часть;",
        "image": "PDD_BOT/markings/r1.15.png"
    },
    {
        "name": "1.15 Велосипедная дорожка",
        "description": "обозначает место, где велосипедная дорожка пересекает проезжую часть;",
        "image": "PDD_BOT/markings/r1.15.png"
    },
    {
        "name": "1.16.1 Направляющие островки",
        "description": "обозначает островки, которые разделяют либо транспортные потоки противоположных направлений, либо места для стоянки транспортных средств (парковки) от велосипедных полос;",
        "image": "PDD_BOT/markings/r1.16.1.png"
    },
    {
        "name": "1.16.2 Особая",
        "description": "обозначает островки, разделяющие транспортные потоки одного направления",
        "image": "PDD_BOT/markings/r1.16.2.png"
    },
    {
        "name": "1.16.3 Особая",
        "description": "обозначает островки в местах слияния транспортных потоков",
        "image": "PDD_BOT/markings/r1.16.3.png"
    },
    {
        "name": "1.17.1 Особая",
        "description": "(цвет - желтый) - обозначает места остановок маршрутных транспортных средств и стоянок транспортных средств, используемых в качестве легковых такси",
        "image": "PDD_BOT/markings/r1.17.png"
    },
    {
        "name": "1.18 Направление движения по полосам",
        "description": "указывает разрешенные на перекрестке направления движения по полосам. Разметка с изображением тупика наносится для указания того, что поворот на ближайшую проезжую часть запрещен; разметка, разрешающая поворот налево из крайней левой полосы, разрешает и разворот;",
        "image": "PDD_BOT/markings/r1.18.png"
    },
    {
        "name": "1.19 Перестроение",
        "description": "предупреждает о приближении к сужению проезжей части (участку, где уменьшается число полос движения в данном направлении) или к линиям разметки 1.1  или 1.11 , разделяющим транспортные потоки противоположных направлений;",
        "image": "PDD_BOT/markings/r1.19.png"
    },
    {
        "name": "1.20 Треугольник",
        "description": "предупреждает о приближении к разметке 1.13 ",
        "image": "PDD_BOT/markings/r1.20.png"
    },
    {
        "name": "1.21 СТОП",
        "description": "предупреждает о приближении к разметке 1.12 , когда она применяется в сочетании со знаком 2.5 СТОП",
        "image": "PDD_BOT/markings/r1.21.png"
    },
    {
        "name": "1.22 Номер дороги",
        "description": "обозначает номер дороги;",
        "image": "PDD_BOT/markings/r1.22.png"
    },
    {
        "name": "1.23.1 Спец полоса",
        "description": "обозначает специальную полосу для маршрутных транспортных средств;",
        "image": "PDD_BOT/markings/r1.23.1.png"
    },
    {
        "name": "1.23.2 Пешеходная дорожка",
        "description": "обозначение пешеходной дорожки или пешеходной части дорожки, предназначенной для совместного движения пешеходов, лиц, использующих для передвижения средства индивидуальной мобильности, и велосипедистов;",
        "image": "PDD_BOT/markings/r1.23.2.png"
    },
    {
        "name": "1.23.3 Велосипедная дорожка",
        "description": "обозначение пешеходной дорожки или пешеходной части дорожки, предназначенной для совместного движения пешеходов, лиц, использующих для передвижения средства индивидуальной мобильности, и велосипедистов;",
        "image": "PDD_BOT/markings/r1.23.3.png"
    },
    {
        "name": "1.24.1 Дублирующая",
        "description": "дублирование запрещающих дорожных знаков",
        "image": "PDD_BOT/markings/r1.24.1.png"
    },
    {
        "name": "1.24.2 Дублирующая",
        "description": "дублирование ограниченией",
        "image": "PDD_BOT/markings/r1.24.2.png"
    },
    {
        "name": "1.24.3 Дублирующая",
        "description": "дублирование таблички инвалиды",
        "image": "PDD_BOT/markings/r1.30.png"
    },
    {
        "name": "1.24.4 Фотовидеофиксация",
        "description": "дублирование дорожного знака Фотовидеофиксация и (или) обозначение участков дороги, на которых может осуществляться фотовидеофиксация; разметка 1.24.4  может применяться самостоятельно;",
        "image": "PDD_BOT/markings/r1.24.4.png"
    },
    {
        "name": "1.24.5 Дублирующая",
        "description": "дублирование дорожного знака Фотовидеофиксация и (или) обозначение участков дороги, на которых может осуществляться фотовидеофиксация; разметка 1.24.4  может применяться самостоятельно;",
        "image": "PDD_BOT/markings/r1.24.5.png"
    },
    {
        "name": "1.24.6 Велосипедная зона",
        "description": "дублирование дорожного знака Велосипедная зона",
        "image": "PDD_BOT/markings/r1.24.6.png"
    },
    {
        "name": "1.24.7 Стоянка ТС дипломатического корпуса",
        "description": "дублирование дорожного знака Стоянка только для транспортных средств дипломатического корпуса",
        "image": "PDD_BOT/markings/r1.24.7.png"
    },
    {
        "name": "1.25 Искусственная неровность",
        "description": "Обозначает искусственные неровности («лежачих полицейских») по ГОСТу Р 52605-2006, предназначенных для принудительного снижения скорости движения ТС внутри жилых зон, у детских учреждений и т. п.",
        "image": "PDD_BOT/markings/r1.25.png"
    },
    {
        "name": "1.26 Обозначение",
        "description": "(цвет - желтый) - обозначает участок перекрестка, на который запрещается выезжать, если впереди по пути следования образовался затор, который вынудит водителя остановиться, создав препятствие для движения транспортных средств в поперечном направлении, за исключением поворота направо или налево в случаях, установленных настоящими Правилами. Разметка может применяться самостоятельно либо совместно с дорожным знаком 1.35 ",
        "image": "PDD_BOT/markings/r1.26.png"
    },
]

user_message_ids = {}  # словарь для хранения последних сообщений пользователя
user_test_state = {}


def get_marking_text(marking, index, total):
    return f"*{marking['name']}*\n\n{marking['description']}\n\nРазметка {index + 1} из {total}"

def get_marking_keyboard(index, total):
    buttons = []

    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"marking_{index - 1}"))

    if index < total - 1:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"marking_{index + 1}"))

    if index == total - 1:
        buttons.append(InlineKeyboardButton("Перейти к тесту", callback_data="start_marking_test"))

    buttons.append(InlineKeyboardButton("🔙 В меню", callback_data="back_to_topics"))
    return InlineKeyboardMarkup([buttons])

async def show_marking_card(update, context: ContextTypes.DEFAULT_TYPE, index: int):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if index < 0 or index >= len(markings):
        await context.bot.send_message(chat_id, "Некорректный номер разметки.")
        return

    marking = markings[index]
    text = get_marking_text(marking, index, len(markings))
    keyboard = get_marking_keyboard(index, len(markings))

    if user_id in user_message_ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=user_message_ids[user_id])
        except:
            pass

    if not os.path.isfile(marking["image"]):
        await context.bot.send_message(chat_id, "Ошибка: изображение не найдено.")
        return

    with open(marking["image"], "rb") as img:
        sent = await context.bot.send_photo(
            chat_id=chat_id,
            photo=InputFile(img),
            caption=text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        user_message_ids[user_id] = sent.message_id







def get_marking_test_keyboard(choices, correct_index):
    keyboard = []
    for i in range(4):
        is_correct = "correct" if i == correct_index else "wrong"
        keyboard.append(InlineKeyboardButton(text=str(i + 1), callback_data=f"marking_answer|{is_correct}"))
    return InlineKeyboardMarkup.from_row(keyboard)

async def start_marking_test(update, context: ContextTypes.DEFAULT_TYPE):
    await send_marking_question(update, context)

async def send_marking_question(update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    marking = random.choice(markings)
    correct_name = marking['name']

    choices = [correct_name]
    while len(choices) < 4:
        choice = random.choice(markings)
        if choice not in choices:
            choices.append(choice)
    random.shuffle(choices)
    correct_index = choices.index(correct_name)
    user_test_state[user_id] = correct_name

    caption_lines = ["Что означает эта разметка?\n"]
    for idx, name in enumerate(choices, start=1):
        caption_lines.append(f"{idx}) {name}")
    caption_text = "\n".join(caption_lines)

    image_path = marking["image"]
    if not os.path.isfile(image_path):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Изображение не найдено: {image_path}"
        )
        return

    with open(image_path, "rb") as img:
        sent = await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=InputFile(img),
            caption=caption_text,
            reply_markup=get_marking_test_keyboard(choices, correct_index)
        )
        user_message_ids[user_id] = sent.message_id

async def handle_marking_test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, result = query.data.split("|")

    if result == "correct":
        await query.edit_message_caption(caption="✅ Правильно!")
    else:
        await query.edit_message_caption(caption="❌ Неправильно. Попробуй ещё раз!")

    await send_marking_question(update, context)





async def handle_marking_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("marking_"):
        try:
            index = int(data.split("_")[1])
            await show_marking_card(update, context, index)
        except ValueError:
            await query.edit_message_text("Ошибка: неправильный формат.")
    elif data == "start_marking_test":
        await start_marking_test(update, context)
    elif data == "back_to_topics":
        from main import get_topics_keyboard
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="📚 Вот список тем:",
            reply_markup=get_topics_keyboard()
        )