import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    WebAppInfo
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ================= КОНФИГУРАЦИЯ =================
BOT_TOKEN = "8649233618:AAF9Vf1whfA9-KngeL93U-oCZDTVII5JqOk"
ADMIN_ID = 2011272893
WEBAPP_URL = "https://playerok-webapp-gty7.vercel.app/"

SITE_URL = "https://playerok.com"    
HEADER_IMAGE_URL = "AgACAgIAAxkBAAEiT1JqmzLWgy9eckir_kjfxDDFeTBTzQAChSVrG5-02UgJ1PUZf8wjMQEAAwIAA3kAAz0E"

users_db = set()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

# ================= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =================
def get_trade_url(trade_id: str = "main") -> str:
    """Генерирует ссылку на WebApp с параметром трейда"""
    return f"{WEBAPP_URL}?trade_id={trade_id}"

# ================= КЛАВИАТУРЫ =================
def get_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔗 Открыть", 
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(text="👤 Профиль", callback_data="btn_profile"),
                InlineKeyboardButton(text="👛 Кошелек", callback_data="btn_wallet")
            ],
            [
                InlineKeyboardButton(text="💬 Чаты", callback_data="btn_chats"),
                InlineKeyboardButton(text="➕ Создать", callback_data="btn_create")
            ],
            [
                InlineKeyboardButton(text="🎧 Поддержка", callback_data="btn_support"),
                InlineKeyboardButton(text="🔗 Сайт ↗", url=SITE_URL)
            ]
        ]
    )

def get_trade_keyboard(trade_id: str = "1001") -> InlineKeyboardMarkup:
    """Клавиатура с прямой ссылкой в Mini App на сделку"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤝 Принять сделку", 
                    web_app=WebAppInfo(url=get_trade_url(trade_id))
                )
            ]
        ]
    )

# ================= ХЕНДЛЕРЫ =================
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    users_db.add(message.from_user.id)
    
    caption_text = (
        "🟢 <b>Playerok — Сервис для проведения сделок</b>\n\n"
        "Покупайте, продавайте и обменивайте товары или услуги безопасно и удобно 🌲"
    )
    
    await message.answer_photo(
        photo=HEADER_IMAGE_URL,
        caption=caption_text,
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )

# Хендлер для отправки ссылки на трейд (/trade или /trade 12345)
@dp.message(Command("trade"))
async def cmd_trade(message: types.Message):
    args = message.text.split()
    trade_id = args[1] if len(args) > 1 else "1001"

    trade_caption = (
        "📦 <b>PLAYEROK: ОБНОВЛЕНИЕ В ТРЕЙДЕ</b>\n\n"
        f"Вы получили приглашение в сделку <b>#{trade_id}</b>!\n\n"
        "Нажмите кнопку ниже, чтобы принять сделку:"
    )

    await message.answer_photo(
        photo=HEADER_IMAGE_URL,
        caption=trade_caption,
        parse_mode="HTML",
        reply_markup=get_trade_keyboard(trade_id=trade_id)
    )

@dp.callback_query(F.data.startswith("btn_"))
async def process_menu_buttons(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    
    responses = {
        "profile": "👤 <b>Ваш профиль в Playerok:</b>\n\nID: <code>{}</code>\nБаланс: 0.00 RUB",
        "wallet": "👛 <b>Кошелек Playerok</b>\n\nДоступный баланс: 0.00 RUB",
        "chats": "💬 <b>Мои чаты</b>\n\nУ вас пока нет активных диалогов.",
        "create": "➕ <b>Создание сделки</b>\n\nВыберите категорию товара или услуги.",
        "support": "🎧 <b>Поддержка Playerok</b>\n\nОбратитесь к оператору через форму в приложении."
    }
    
    text = responses.get(action, "Раздел обновляется.").format(callback.from_user.id)
    await callback.answer()
    await callback.message.answer(text, parse_mode="HTML")

# ================= ЗАПУСК =================
async def main():
    try:
        await bot.set_my_name("Playerok")
    except Exception:
        pass
        
    print("Бот Playerok запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
