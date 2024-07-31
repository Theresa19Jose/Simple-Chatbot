from typing import Final
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# pip install python-telegram-bot

# Constants
TOKEN: Final[str] = 'Enter your chatbot token'
BOT_USERNAME: Final[str] = '@YOUR_BOT'


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! Nice to meet you. Let\'s chat!')

    # Create button for requesting phone number
    button = KeyboardButton(text="Share phone number", request_contact=True)
    keyboard = [[button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        'Please share your phone number with me.',
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Just type something and I will respond to you!')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command.')


# Create your own response logic
def handle_response(text: str):
    processed = text.lower()
    
    greetings = ['hai', 'hello', 'hey', 'hi']
    for greeting in greetings:
        if greeting in processed:
            return 'Hey there!'

    if 'how are you' in processed:
        return 'I am good, thanks! How are you?'
    
    if 'i am good' in processed:
        return 'Good to hear that!!'

    if 'i love python' in processed:
        return 'Python is coooooool.'

    if 'bye' in processed:
        return 'It was nice talking to you. See you soon!'

    if 'what is your name' in processed:
        return 'I am a chatbot created to assist you!'

    if 'what can you do' in processed:
        return 'I can chat with you, answer your questions, and help you with various tasks.'

    if 'thank you' in processed or 'thanks' in processed:
        return 'You are welcome!'

    if 'tell me a joke' in processed:
        return 'Why did the scarecrow win an award? Because he was outstanding in his field!'

    if 'what is your favorite color' in processed:
        return 'I love all the colors of the rainbow!'

    if 'who created you' in processed:
        return 'I was created by a team of talented developers.'

    if 'help' in processed:
        return 'How can I assist you today?'

    if 'weather' in processed:
        return 'I can’t check the weather, but I hope it’s nice wherever you are!'

    return 'I do not understand...'



# Handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    message_type: str = update.message.chat.type
    text: str = update.message.text
    #print(update)
    # Log users
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Handle message type
    response: str = handle_response(text)

    # Reply
    print('Bot:', response)
    await update.message.reply_text(response)


# Handle incoming contacts
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    print(update)
    print(contact)
    print(f"User {update.message.chat.id} shared their phone number: {contact.phone_number}")
    await update.message.reply_text(f'Thanks for sharing your phone number: {contact.phone_number}')


# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error: {context.error}')


def main():
    print('Starting up bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    # Errors
    app.add_error_handler(error)

    # Define a poll interval
    print('Polling...')
    app.run_polling(poll_interval=1)


if __name__ == '__main__':
    main()