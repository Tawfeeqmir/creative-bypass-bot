import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *CreativeBypass Bot mein aapka swagat hai!*\n\n"
        "🔗 Terabox ka koi bhi public link bhejein\n"
        "⚡ Main aapko direct access dunga\n\n"
        "📌 Example:\nhttps://terabox.com/s/xxxxxxx",
        parse_mode="Markdown"
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    terabox_domains = ["terabox.com", "1024tera.com", "teraboxapp.com", "terasharelink.com"]
    if any(domain in text for domain in terabox_domains):
        await update.message.reply_text("⏳ Link check ho raha hai...")
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(text, headers=headers, timeout=10, allow_redirects=True)
            final_url = r.url
            keyboard = [[InlineKeyboardButton("🔗 Link Kholo", url=final_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"✅ *Link mil gaya!*\n\nNeeche button press karein:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            await update.message.reply_text("❌ Link kaam nahi kar raha. Dobara try karein.")
    else:
        await update.message.reply_text("⚠️ Sirf Terabox links support hain!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.run_polling()
