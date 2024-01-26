from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from googletrans import Translator, LANGUAGES
import os
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define command handlers
def start(update: Update, context):
    user = update.effective_user
    welcome_text = f"Hi {user.first_name}, I am your Translation Bot. Choose a language for translation:"
    keyboard = [
        [InlineKeyboardButton("English to Russian", callback_data='en-ru')],
        [InlineKeyboardButton("English to Hindi", callback_data='en-hi')],
        # Add other buttons similarly
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(welcome_text, reply_markup=reply_markup)

def button(update: Update, context):
    query = update.callback_query
    query.answer()
    context.user_data['choice'] = query.data
    query.edit_message_text(text=f"Selected language: {LANGUAGES[query.data.split('-')[1]]}. Send me text or media to translate.")

def translate(update: Update, context):
    translator = Translator()
    choice = context.user_data.get('choice')
    if not choice:
        update.message.reply_text("Please choose a language first.")
        return

    dest_lang = choice.split('-')[1]
    if update.message.text:
        translated_text = translator.translate(update.message.text, dest=dest_lang).text
        update.message.reply_text(translated_text)
    elif update.message.caption:
        translated_caption = translator.translate(update.message.caption, dest=dest_lang).text
        if update.message.photo:
            update.message.reply_photo(photo=update.message.photo[-1].file_id, caption=translated_caption)
        elif update.message.video:
            update.message.reply_video(video=update.message.video.file_id, caption=translated_caption)

def error(update, context):
    """Log errors caused by updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Use environment variable for token
    TOKEN = os.environ.get('6836176293:AAFaC4HjsWAkSBAZVLD1WN6keAqacbCu0iw')

    if not TOKEN:
        logger.error("No token provided. Set the TELEGRAM_TOKEN environment variable.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text | Filters.photo | Filters.video, translate))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
