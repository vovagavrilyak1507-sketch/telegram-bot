import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# ================== НАЛАШТУВАННЯ ==================

BOT_TOKEN = "8463196633:AAHCyzSUSD02FROx8v0IG2X8YGEf2Q5JXms"
ADMIN_ID = 634176629

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ================== СТАТИСТИКА ==================

stats = {
    "requests": 0
}

# ================== FSM ==================

class RequestForm(StatesGroup):
    service = State()
    description = State()
    contact = State()

# ================== КНОПКИ ==================

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📩 Залишити заявку")],
        [KeyboardButton(text="ℹ️ Послуги")],
        [KeyboardButton(text="📞 Контакти")]
    ],
    resize_keyboard=True
)

services_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🤖 Telegram-бот")],
        [KeyboardButton(text="🧩 CRM / автоматизація")],
        [KeyboardButton(text="🧠 AI-рішення")],
        [KeyboardButton(text="❓ Інше")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="⬅️ Назад у меню")]
    ],
    resize_keyboard=True
)

# ================== START ==================

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Вітаю!\n\n"
        "Я — бот компанії *Havryliak Limited Company*.\n"
        "Допомагаю бізнесу виходити на новий рівень:\n"
        "автоматизація, Telegram-боти, AI.\n\n"
        "⬇️ Обери дію:",
        reply_markup=main_kb,
        parse_mode="Markdown"
    )

# ================== ПОСЛУГИ ==================

@dp.message(F.text == "ℹ️ Послуги")
async def services(message: Message):
    await message.answer(
        "🛠 *Наші послуги:*\n\n"
        "• 🤖 Telegram-боти\n"
        "• 🧩 CRM та автоматизація бізнесу\n"
        "• 🧠 AI-рішення\n"
        "• ⚙️ Інтеграції та оптимізація процесів\n\n"
        "📩 Натисни *Залишити заявку*",
        parse_mode="Markdown"
    )

# ================== КОНТАКТИ ==================

@dp.message(F.text == "📞 Контакти")
async def contacts(message: Message):
    await message.answer(
        "📞 *Контакти:*\n\n"
        "Telegram: @Havryliak\n"
        "Email: info@havryliak.com\n\n"
        "Пиши — будемо раді співпраці 🤝",
        parse_mode="Markdown"
    )

# ================== ЗАЯВКА ==================

@dp.message(F.text == "📩 Залишити заявку")
async def start_request(message: Message, state: FSMContext):
    await state.set_state(RequestForm.service)
    await message.answer(
        "📌 Обери послугу:",
        reply_markup=services_kb
    )

@dp.message(RequestForm.service)
async def request_service(message: Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.clear()
        await message.answer("Повертаємось у меню ⬇️", reply_markup=main_kb)
        return

    await state.update_data(service=message.text)
    await state.set_state(RequestForm.description)

    await message.answer(
        "✍️ Опиши свою задачу:",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(RequestForm.description)
async def request_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(RequestForm.contact)

    await message.answer(
        "📞 Залиш контакт (телефон або @username):"
    )

@dp.message(RequestForm.contact)
async def request_contact(message: Message, state: FSMContext):
    data = await state.get_data()

    stats["requests"] += 1

    text = (
        "📥 *Нова заявка!*\n\n"
        f"🛠 Послуга: {data['service']}\n"
        f"📝 Опис: {data['description']}\n"
        f"📞 Контакт: {message.text}\n\n"
        f"👤 @{message.from_user.username}\n"
        f"🆔 `{message.from_user.id}`"
    )

    await bot.send_message(ADMIN_ID, text, parse_mode="Markdown")

    await message.answer(
        "✅ Дякую! Заявку прийнято.\n"
        "Наш менеджер скоро з тобою звʼяжеться 👌",
        reply_markup=main_kb
    )

    await state.clear()

# ================== АДМІН-ПАНЕЛЬ ==================

@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "🛠 *Адмін-панель*\n\n"
        "Доступні дії ⬇️",
        reply_markup=admin_kb,
        parse_mode="Markdown"
    )

@dp.message(F.text == "📊 Статистика")
async def admin_stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        f"📊 *Статистика бота:*\n\n"
        f"📩 Заявок отримано: *{stats['requests']}*",
        parse_mode="Markdown"
    )

@dp.message(F.text == "⬅️ Назад у меню")
async def admin_back(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "Повернення в головне меню ⬇️",
        reply_markup=main_kb
    )

# ================== ЗАПУСК ==================

async def main():
    print("🤖 Бот запущений")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
def is_admin(user_id: int) -> bool:
    ADMINS = list(map(int, os.getenv("ADMINS", "").split(",")))
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Всі замовлення")],
        [KeyboardButton(text="🆕 Нові замовлення")],
        [KeyboardButton(text="👤 Користувачі")],
        [KeyboardButton(text="⚙️ Налаштування")],
    ],
    resize_keyboard=True
)
@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ У вас немає доступу")
        return

    await message.answer(
        "🔐 Адмін-панель",
        reply_markup=admin_kb
    )
@dp.message(lambda m: m.text == "📋 Всі замовлення")
async def all_orders(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer("📋 Тут буде список всіх замовлень")
@dp.message(lambda m: m.text == "🆕 Нові замовлення")
async def new_orders(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer("🆕 Тут будуть нові замовлення")
@dp.message(lambda m: m.text == "👤 Користувачі")
async def users_list(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer("👤 Тут буде список користувачів")
@dp.message(lambda m: m.text == "⚙️ Налаштування")
async def settings(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer("⚙️ Налаштування бота (буде далі)")
import asyncio

async def main():
    print("🤖 Бот запущений")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




