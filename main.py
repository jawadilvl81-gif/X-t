import os
import yt_dlp
import requests

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# =========================
# CONFIG
# =========================

TOKEN = os.getenv("TOKEN")

# =========================
# IMAGE SEARCH FUNCTION
# =========================

def get_image(query):
    try:
        url = f"https://picsum.photos/seed/{query}/800/500"
        return url
    except:
        return None

# =========================
# SEARCH COMMAND
# =========================

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = " ".join(context.args)

    if not query:
        await update.message.reply_text(
            "Use:\n/search anything"
        )
        return

    loading = await update.message.reply_text(
        f"Searching for: {query}..."
    )

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
    }

    try:

        # =========================
        # IMAGE SEND
        # =========================

        image_url = get_image(query)

        if image_url:
            await update.message.reply_photo(
                photo=image_url,
                caption=f"Image result for: {query}"
            )

        # =========================
        # VIDEO SEARCH
        # =========================

        results_text = f"Top Results For: {query}\n\n"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            search_query = f"ytsearch10:{query}"

            info = ydl.extract_info(
                search_query,
                download=False
            )

            entries = info.get("entries", [])

            if not entries:
                await update.message.reply_text(
                    "No results found."
                )
                return

            for i, entry in enumerate(entries, start=1):

                title = entry.get("title", "No Title")
                video_id = entry.get("id", "")
                url = f"https://www.youtube.com/watch?v={video_id}"

                results_text += (
                    f"{i}. {title}\n"
                    f"{url}\n\n"
                )

        # Telegram limit protection
        if len(results_text) > 4000:
            results_text = results_text[:4000]

        await update.message.reply_text(results_text)

        await loading.delete()

    except Exception as e:
        await update.message.reply_text(
            f"Error:\n{str(e)}"
        )

# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "Bot Online ✅\n\n"
        "Commands:\n"
        "/search anything"
    )

    await update.message.reply_text(text)

# =========================
# MAIN
# =========================

def main():

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))

    print("Bot Running...")

    app.run_polling()

if __name__ == "__main__":
    main()
