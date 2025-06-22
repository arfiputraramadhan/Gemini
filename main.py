import logging, asyncio, datetime
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai

# === CONFIG ===
import os
TELEGRAM_BOT_TOKEN = os.environ.get('7422543116:AAFtqw0Ym-fofO7RNndX0jC2WONIxff_SQg')
GEMINI_API_KEY = os.environ.get('AIzaSyBI-dOfakOL5UOeVaii6chvYhb8m9T90l0')
CHAT_ID = int(os.environ.get('7718654363'))  # wajib integer

# === INIT GEMINI ===
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

logging.basicConfig(level=logging.INFO)

# === DAILY PROMPT ===
DAILY_PROMPT = "Apa informasi menarik atau fakta unik hari ini?"

# === KIRIM OTOMATIS
async def send_daily_message(app):
    while True:
        now = datetime.datetime.now()
        target = now.replace(hour=7, minute=0, second=0, microsecond=0)
        if now > target:
            target += datetime.timedelta(days=1)
        await asyncio.sleep((target - now).total_seconds())

        try:
            response = model.generate_content(DAILY_PROMPT)
            text = response.text
        except Exception as e:
            text = f"❌ Error dari Gemini: {e}"

        await app.bot.send_message(chat_id=CHAT_ID, text=f"🧠 *Info Harian:*\n{text}", parse_mode="Markdown")

# === RESPON MANUAL
async def handle_message(update, context):
    try:
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def start(update, context):
    await update.message.reply_text("Bot aktif. Kirim pertanyaan kapan saja!")

# === MAIN
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    asyncio.get_event_loop().create_task(send_daily_message(app))
    app.run_polling()

if __name__ == "__main__":
    main()
