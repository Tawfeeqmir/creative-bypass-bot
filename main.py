import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 CreativeBypass Bot mein aapka swagat hai!\n\n"
        "🔗 Terabox ka koi bhi public link bhejein\n"
        "⚡ Main aapko direct link dunga!"
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    terabox_domains = ["terabox.com", "1024tera.com", "teraboxapp.com"]
    if any(domain in text for domain in terabox_domains):
        await update.message.reply_text("⏳ Processing...")
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(text, headers=headers, timeout=10, allow_redirects=True)
            await update.message.reply_text(f"✅ Link:\n{r.url}")
        except:
            await update.message.reply_text("❌ Error. Dobara try karein.")
    else:
        await update.message.reply_text("⚠️ Sirf Terabox links bhejein!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()

if __name__ == "__main__":
    main()
