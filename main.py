import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Token & Configuration
BOT_TOKEN = "8783616591:AAEYGC43fEZjspF_SQ8-qWyjLPzfxfMAPYw"
MINI_APP_URL = "https://gmailtaskminiapp.netlify.app"  # আপনার মিনি অ্যাপের লিংক

# আপনার চ্যানেলগুলোর ইউজারনেম (@ সহ)
CHANNELS = ["@channel1", "@channel2", "@channel3", "@group"] 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_membership(user_id, context):
    """ব্যবহারকারী সব চ্যানেলে যুক্ত আছে কিনা যাচাই করবে"""
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception:
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id

    # চেক করবে অলরেডি জয়েন করা আছে কিনা
    is_joined = await check_membership(user_id, context)

    if is_joined:
        # জয়েন থাকলে সরাসরি মিনি অ্যাপের বাটন দেখাবে
        keyboard = [
            [InlineKeyboardButton("🚀 Open Mini App", web_app={"url": "https://gmailtaskminiapp.netlify.app"})] # অথবা সরাসরি মিনি অ্যাপ ইউআরএল
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"👋 Hello, {first_name}!\n\nWelcome back! Click below to open the Mini App:",
            reply_markup=reply_markup
        )
    else:
        # জয়েন না থাকলে চ্যানেলের বাটনগুলো দেখাবে
        keyboard = [
            [
                InlineKeyboardButton("➕ Join Channel 1", url="https://t.me/RsnTechHub"),
                InlineKeyboardButton("➕ Join Channel 2", url="https://t.me/tmarif19")
            ],
            [
                InlineKeyboardButton("➕ Join Channel 3", url="https://t.me/rasineditz14"),
                InlineKeyboardButton("➕ Join Group", url="https://t.me/rasingroupchat")
            ],
            [InlineKeyboardButton("🛡 Check / Joined All Channels", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"👋 Hello, {first_name}!\n\n"
            "✨ Welcome to our bot! Explore all features and enjoy the experience.\n\n"
            "🎯 Don't forget to join all channels and try out the options below 👇",
            reply_markup=reply_markup
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_name = query.from_user.first_name

    if query.data == "check_join":
        if await check_membership(user_id, context):
            keyboard = [
                [InlineKeyboardButton("🚀 Open Mini App", url=MINI_APP_URL)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"✅ Thank you for joining, {first_name}!\n\nClick below to access the Mini App:",
                reply_markup=reply_markup
            )
        else:
            await query.answer("❌ You haven't joined all channels yet! Please join first.", show_alert=True)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.run_polling()
