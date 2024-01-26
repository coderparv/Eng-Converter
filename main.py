from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from googletrans import Translator
import logging

# Enable logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the command handlers
def start(update: Update, context):
    user = update.effective_user
    welcome_text = f"Hi {user.first_name}, I am [BotName]. I can help you translate text. Choose a language:"
    keyboard = [
        [InlineKeyboardButton("English to Russian", callback_data='en-ru')],
        [InlineKeyboardButton("English to Hindi", callback_data='en-hi')],
        [InlineKeyboardButton("English to German", callback_data='en-de')],
        [InlineKeyboardButton("English to Chinese", callback_data='en-zh')],
        [InlineKeyboardButton("English to French", callback_data='en-fr')],
        [InlineKeyboardButton("English to Spanish", callback_data='en-es')],
        [InlineKeyboardButton("English to Italian", callback_data='en-it')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(welcome_text, reply_markup=reply_markup)

def button(update: Update, context):
    query = update.callback_query
    query.answer()
    context.user_data['choice'] = query.data
    query.edit_message_text(text=f"Selected language: {query.data.split('-')[1]}. Now send me text to translate.")

def translate_text(update: Update, context):
    choice = context.user_data.get('choice')
    if choice:
        translator = Translator()
        result = translator.translate(update.message.text, dest=choice.split('-')[1])
        update.message.reply_text(result.text)
    else:
        update.message.reply_text("Please choose a language first.")

def error(update, context):
    """Log errors caused by updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    TOKEN = '6836176293:AAFaC4HjsWAkSBAZVLD1WN6keAqacbCu0iw'

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
