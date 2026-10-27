"""AI Telegram Bot Yaratuvchi — starter project.
Python 3.11+. Requires a Telegram bot token for the maker bot.
Users can connect a BotFather-created token and configure a simple reply bot.
For production, add encrypted token storage, authentication, rate limits, and persistent hosting.
"""
import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import TelegramError

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
TOKEN = os.getenv("MAKER_BOT_TOKEN", "").strip()
if not TOKEN:
    raise SystemExit("Set MAKER_BOT_TOKEN environment variable to the token of your main bot.")

# Demo mode: connected bots are validated and their requested behavior is saved in memory.
# Dynamic multi-bot hosting needs a persistent worker/service; this project intentionally
# does not save user tokens to disk or expose them in logs.
users = {}
MENU = ReplyKeyboardMarkup(
    [[KeyboardButton("🤖 Yangi bot yaratish")], [KeyboardButton("ℹ️ Qanday ishlaydi?")]],
    resize_keyboard=True,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI Telegram Bot Yaratuvchi\n\n"
        "O‘z g‘oyangizga mos botni sozlashni boshlang.\n"
        "BotFather tokenini faqat o‘zingiz yaratgan bot uchun yuboring. "
        "Token maxfiy kalit hisoblanadi.", reply_markup=MENU)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "1) ‘Yangi bot yaratish’ tugmasini bosing.\n"
        "2) Yaratmoqchi bo‘lgan botingiz nima qilishini yozing.\n"
        "3) BotFather’da yaratgan botingiz tokenini ulashing.\n\n"
        "Eslatma: bu boshlang‘ich loyiha. U hozircha boshqa botlarni avtomatik, "
        "24/7 ishga tushirishni yakunlamaydi; buning uchun alohida server worker va "
        "xavfsiz token ombori sozlanishi kerak.")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    uid = update.effective_user.id
    text = update.message.text.strip()
    state = context.user_data.get("state")
    if text == "ℹ️ Qanday ishlaydi?":
        await help_cmd(update, context)
        return
    if text == "🤖 Yangi bot yaratish":
        context.user_data["state"] = "description"
        await update.message.reply_text(
            "💡 Bot nima qilishi kerakligini yozing. Masalan: mijozlarga ish vaqtim va narxlarimni aytsin.")
        return
    if state == "description":
        context.user_data["bot_description"] = text[:1000]
        context.user_data["state"] = "token"
        await update.message.reply_text(
            "Endi @BotFather’da o‘zingiz yaratgan bot tokenini yuboring.\n\n"
            "⚠️ Tokenni hech kimga bermang. Ish tugagach uni BotFather orqali bekor qilishingiz mumkin.")
        return
    if state == "token":
        try:
            from telegram import Bot
            async with Bot(text) as bot:
                me = await bot.get_me()
            # Never log or echo the token. Do not persist it in this demo.
            users[uid] = {"username": me.username, "description": context.user_data.get("bot_description", "")}
            context.user_data.clear()
            await update.message.reply_text(
                f"✅ Token tekshirildi: @{me.username}\n\n"
                "Sizning bot g‘oyangiz qabul qilindi.\n"
                "⚠️ Bu demo tokenni saqlamaydi va yangi botni 24/7 ishga tushirmaydi. "
                "Buning uchun serverdagi alohida worker va xavfsiz saqlash qismi kerak.", reply_markup=MENU)
        except TelegramError:
            await update.message.reply_text("❌ Token noto‘g‘ri yoki Telegram bilan aloqa bo‘lmadi. Tokenni tekshiring va qayta yuboring.")
        return
    await update.message.reply_text("Menyudan tanlang yoki /start bosing.", reply_markup=MENU)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

if __name__ == "__main__":
    print("AI Telegram Bot Yaratuvchi is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
