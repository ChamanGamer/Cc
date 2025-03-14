import logging
import time
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from yt_dlp import YoutubeDL  # For downloading videos

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token (replace with your actual bot token)
BOT_TOKEN = "7634755080:AAGKo5abztkfSkeEdX3fRI9S5aMW1NFSAqg"

# Rate limiting: Max 3 requests per user every 10 minutes
rate_limit = {}
RATE_LIMIT_MAX = 3
RATE_LIMIT_TIME = 600  # 10 minutes in seconds

# Path to cookies file (replace with your actual cookies file path)
COOKIES_FILE = "cookies.txt"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 Welcome to the **Video Downloader Bot**!\n\n"
        "I can download videos from YouTube, Instagram, TikTok, and TeraBox!\n\n"
        "📥 **Commands**:\n"
        "1. /yt <url> - Download a YouTube video.\n"
        "2. /insta <url> - Download an Instagram video.\n"
        "3. /tiktok <url> - Download a TikTok video.\n"
        "4. /terabox <url> - Download a TeraBox video.\n"
        "5. /help - Show this help message."
    )

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 **Video Downloader Bot**\n\n"
        "📥 **Commands**:\n"
        "1. /yt <url> - Download a YouTube video.\n"
        "2. /insta <url> - Download an Instagram video.\n"
        "3. /tiktok <url> - Download a TikTok video.\n"
        "4. /terabox <url> - Download a TeraBox video.\n"
        "5. /help - Show this help message."
    )

# Download YouTube video
async def yt_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    video_url = " ".join(context.args)

    # Rate limiting check
    if user_id in rate_limit:
        if rate_limit[user_id]["count"] >= RATE_LIMIT_MAX:
            time_remaining = rate_limit[user_id]["time"] + RATE_LIMIT_TIME - time.time()
            if time_remaining > 0:
                await update.message.reply_text(f"⚠️ You've reached the rate limit. Please try again in {int(time_remaining)} seconds.")
                return
        else:
            rate_limit[user_id]["count"] += 1
    else:
        rate_limit[user_id] = {"count": 1, "time": time.time()}

    # Notify user
    await update.message.reply_text("📦 Processing your request...")

    # Download video using yt-dlp with cookies
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'cookiefile': COOKIES_FILE,  # Use cookies for authentication
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_title = info.get('title', 'video')
            video_file = ydl.prepare_filename(info)

        # Send video to user
        with open(video_file, 'rb') as video:
            await update.message.reply_video(
                video=video,
                caption=f"📦 **{video_title}**\n\n✅ Here's your video!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📥 Download", url=video_url)]
                ])
            )

        # Delete the downloaded file
        os.remove(video_file)
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to download the video. Error: {str(e)}")

# Download Instagram video
async def insta_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📦 Instagram download feature is under development. Stay tuned!")

# Download TikTok video
async def tiktok_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📦 TikTok download feature is under development. Stay tuned!")

# Download TeraBox video
async def terabox_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    video_url = " ".join(context.args)

    # Rate limiting check
    if user_id in rate_limit:
        if rate_limit[user_id]["count"] >= RATE_LIMIT_MAX:
            time_remaining = rate_limit[user_id]["time"] + RATE_LIMIT_TIME - time.time()
            if time_remaining > 0:
                await update.message.reply_text(f"⚠️ You've reached the rate limit. Please try again in {int(time_remaining)} seconds.")
                return
        else:
            rate_limit[user_id]["count"] += 1
    else:
        rate_limit[user_id] = {"count": 1, "time": time.time()}

    # Notify user
    await update.message.reply_text("📦 Processing your request...")

    # Download video using yt-dlp
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_title = info.get('title', 'video')
            video_file = ydl.prepare_filename(info)

        # Send video to user
        with open(video_file, 'rb') as video:
            await update.message.reply_video(
                video=video,
                caption=f"📦 **{video_title}**\n\n✅ Here's your video!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📥 Download", url=video_url)]
                ])
            )

        # Delete the downloaded file
        os.remove(video_file)
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to download the video. Error: {str(e)}")

# Main function
def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("yt", yt_download))
    application.add_handler(CommandHandler("insta", insta_download))
    application.add_handler(CommandHandler("tiktok", tiktok_download))
    application.add_handler(CommandHandler("terabox", terabox_download))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()