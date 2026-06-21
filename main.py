import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, Update
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
YOUR_USERNAME = os.getenv("YOUR_USERNAME", "HTML_PRO5")
APP_URL = os.getenv("APP_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "danya-secret-2026")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")
if not ADMIN_ID:
    raise RuntimeError("ADMIN_ID is not set")
if not APP_URL:
    raise RuntimeError("APP_URL is not set")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class RequestForm(StatesGroup):
    project = State()
    contacts = State()


BOT_VARIANTS = {
    "shopbot": """
🛒 <b>ShopBot — бот для продаж и заказов</b>

Это Telegram-бот, который помогает продавать товары или услуги прямо в Telegram.

<b>Что может быть внутри:</b>
✅ Каталог товаров/услуг  
✅ Корзина  
✅ Оформление заказа  
✅ Уведомления владельцу  
✅ Админ-панель  
✅ Оплата  
✅ Автоматические ответы клиентам  

<b>Кому подойдёт:</b>
магазинам, кондитерам, мастерам, салонам, продавцам одежды, косметики, аксессуаров и услуг.

<b>Главная польза:</b>
клиент сам выбирает, что ему нужно, а заявка сразу приходит владельцу.
""",
    "edubot": """
🎓 <b>EduBot — бот для обучения</b>

Бот для курсов, онлайн-школ, репетиторов и обучающих проектов.

<b>Что может быть внутри:</b>
✅ Уроки и материалы  
✅ Тесты и викторины  
✅ Проверка ответов  
✅ Прогресс учеников  
✅ Доступ к урокам  
✅ Сертификаты  
✅ Рассылка материалов  

<b>Кому подойдёт:</b>
репетиторам, наставникам, школам, авторам курсов и обучающих программ.

<b>Главная польза:</b>
бот сам выдаёт материалы и помогает вести учеников без постоянной ручной переписки.
""",
    "eventbot": """
📅 <b>EventBot — бот для мероприятий</b>

Бот для записи участников, регистрации и организации событий.

<b>Что может быть внутри:</b>
✅ Регистрация участников  
✅ Сбор имени, телефона и Telegram  
✅ Расписание мероприятия  
✅ Напоминания  
✅ QR-билеты  
✅ Список гостей  
✅ Статистика  

<b>Кому подойдёт:</b>
организаторам мероприятий, мастер-классов, тренировок, вебинаров и встреч.

<b>Главная польза:</b>
все заявки собираются автоматически, а участники получают нужную информацию без лишних вопросов.
"""
}


def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="🤖 Варианты ботов", callback_data="variants")
    kb.button(text="💼 Услуги", callback_data="services")
    kb.button(text="👨‍💻 Обо мне", callback_data="about")
    kb.button(text="📝 Оставить заявку", callback_data="request")
    kb.button(text="📩 Связаться напрямую", url=f"https://t.me/{YOUR_USERNAME}")
    kb.adjust(1)
    return kb.as_markup()


def variants_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="🛒 ShopBot — продажи", callback_data="bot_shopbot")
    kb.button(text="🎓 EduBot — обучение", callback_data="bot_edubot")
    kb.button(text="📅 EventBot — мероприятия", callback_data="bot_eventbot")
    kb.button(text="📝 Хочу похожего бота", callback_data="request")
    kb.button(text="⬅️ Назад", callback_data="main")
    kb.adjust(1)
    return kb.as_markup()


def back_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Оставить заявку", callback_data="request")
    kb.button(text="⬅️ Назад в меню", callback_data="main")
    kb.adjust(1)
    return kb.as_markup()


@dp.message(CommandStart())
async def start_handler(message: Message):
    text = """
👋 <b>Добро пожаловать в DANYA DEV!</b>

Я — Telegram-бот ассистент по разработке ботов и автоматизации.

Здесь можно:

🤖 посмотреть варианты Telegram-ботов  
💼 узнать, какие услуги можно заказать  
👨‍💻 познакомиться с DANYA DEV  
📝 оставить заявку на разработку  
📩 передать идею проекта напрямую разработчику  

<b>DANYA DEV</b> — это разработка Telegram-ботов под бизнес, обучение, продажи, мероприятия и любые задачи, где нужно убрать ручную работу.

Выберите нужный раздел ниже 👇
"""
    await message.answer(text, reply_markup=main_menu(), parse_mode="HTML")


@dp.callback_query()
async def callback_handler(call: CallbackQuery, state: FSMContext):
    data = call.data

    if data == "main":
        await state.clear()
        await call.message.edit_text(
            """
🏠 <b>Главное меню DANYA DEV</b>
Выберите, что хотите посмотреть:

🤖 варианты готовых решений  
💼 услуги по разработке  
👨‍💻 информацию обо мне  
📝 форму заявки на проект
""",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )

    elif data == "variants":
        await call.message.edit_text(
            """
🤖 <b>Варианты Telegram-ботов</b>

Ниже собраны примеры решений, которые можно сделать под разные задачи.

Каждый бот можно изменить под ваш бизнес: добавить нужные кнопки, меню, оплату, уведомления, админ-панель, заявки и другую логику.

Выберите пример, чтобы узнать подробнее 👇
""",
            reply_markup=variants_menu(),
            parse_mode="HTML"
        )

    elif data and data.startswith("bot_"):
        bot_key = data.replace("bot_", "")
        await call.message.edit_text(
            BOT_VARIANTS.get(bot_key, "Такой вариант пока не найден."),
            reply_markup=back_menu(),
            parse_mode="HTML"
        )

    elif data == "services":
        await call.message.edit_text(
            """
💼 <b>Услуги DANYA DEV</b>

Я могу сделать Telegram-бота под вашу задачу с нуля.

<b>Что можно заказать:</b>

🤖 <b>Telegram-бот под ключ</b>  
Полная разработка: структура, кнопки, логика, тексты, запуск.

🛒 <b>Бот для продаж</b>  
Каталог, корзина, заказы, уведомления, оплата.

📋 <b>Бот для заявок</b>  
Сбор имени, телефона, услуги, комментария и отправка заявки владельцу.

🎓 <b>Бот для обучения</b>  
Уроки, тесты, материалы, прогресс учеников.

📅 <b>Бот для мероприятий</b>  
Регистрация, расписание, напоминания, QR-билеты.

⚙️ <b>Доработка готового бота</b>  
Можно улучшить уже существующего бота, добавить функции или исправить ошибки.

Чтобы я понял задачу, лучше сразу оставить заявку 👇
""",
            reply_markup=back_menu(),
            parse_mode="HTML"
        )

    elif data == "about":
        await call.message.edit_text(
            """
👨‍💻 <b>О DANYA DEV</b>

DANYA DEV — это разработка Telegram-ботов для бизнеса, услуг, обучения и автоматизации.

Я создаю не просто “бота с кнопками”, а удобного помощника, который может:

✅ принимать заявки  
✅ отвечать клиентам  
✅ собирать данные  
✅ показывать товары или услуги  
✅ отправлять уведомления  
✅ экономить время владельцу проекта  

<b>Главная цель:</b>
сделать так, чтобы клиенту было удобно, а владельцу бизнеса — проще работать.

Если у вас есть идея, можно оставить заявку, и я свяжусь с вами напрямую.
""",
            reply_markup=back_menu(),
            parse_mode="HTML"
        )

    elif data == "request":
        await state.set_state(RequestForm.project)
        await call.message.edit_text(
            """
📝 <b>Заявка на разработку Telegram-бота</b>

Опишите, какой бот вам нужен.

Напишите одним сообщением:

1️⃣ Для чего нужен бот?  
2️⃣ Что он должен уметь?  
3️⃣ Для какого проекта или бизнеса?  
4️⃣ Нужны ли заявки, оплата, каталог, админ-панель?  
5️⃣ Есть ли пример, на который нужно ориентироваться?

<b>Пример:</b>
«Мне нужен бот для магазина. Нужно меню товаров, корзина, оформление заказа и чтобы заявки приходили администратору».
""",
            parse_mode="HTML"
        )

    await call.answer()


@dp.message(RequestForm.project)
async def get_project_info(message: Message, state: FSMContext):
    await state.update_data(project=message.text)
    await state.set_state(RequestForm.contacts)

    await message.answer(
        """
Отлично 👍

Теперь оставьте контакт для связи.

Можно написать:

📱 номер телефона  
или  
💬 ваш Telegram username  

<b>Пример:</b>
@username  
или  
+380XXXXXXXXX
""",
        parse_mode="HTML"
    )


@dp.message(RequestForm.contacts)
async def get_contacts(message: Message, state: FSMContext):
    data = await state.get_data()
    project = data.get("project")
    contacts = message.text

    user = message.from_user
    username = f"@{user.username}" if user.username else "username не указан"

    admin_text = f"""
📩 <b>Новая заявка на Telegram-бота</b>

👤 <b>Клиент:</b>
{user.full_name}

🔗 <b>Telegram:</b>
{username}

🆔 <b>ID:</b>
<code>{user.id}</code>

📌 <b>Описание проекта:</b>
{project}

📞 <b>Контакт для связи:</b>
{contacts}
"""

    await bot.send_message(
        ADMIN_ID,
        admin_text,
        parse_mode="HTML"
    )

    await message.answer(
        """
✅ <b>Заявка отправлена!</b>

Спасибо, я получил вашу информацию.

Разработчик DANYA DEV посмотрит заявку и свяжется с вами напрямую в Telegram или по указанному контакту.
""",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

    await state.clear()


@dp.message()
async def text_handler(message: Message):
    await message.answer(
        """
Я помогу разобраться с Telegram-ботами 🤖

Выберите нужный раздел в меню ниже:
""",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_url = f"{APP_URL.rstrip('/')}/webhook/{WEBHOOK_SECRET}"
    await bot.set_webhook(webhook_url, drop_pending_updates=True)
    logging.info("Webhook set: %s", webhook_url)
    yield
    await bot.delete_webhook()
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def home():
    return {
        "status": "DANYA DEV bot is running",
        "webhook": "enabled"
    }


@app.post("/webhook/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    data = await request.json()
    update = Update.model_validate(data, context={"bot": bot})
    await dp.feed_update(bot, update)

    return {"ok": True}
