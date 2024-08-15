from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from theater_module import confirm_selection, theater, theater_selected, movie_or_time_selected, showtime_selected, selected_movie
from  movie_module  import movie, movie_selected, theater_or_time_selected, mshowtime_selected,mtheater_selected
from  time_module import time , time_selected , theater_or_movie_selected, select_movie_after_theater , select_theater_after_movie

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton('MOVIE', callback_data='start_movie')],
        [InlineKeyboardButton('THEATER', callback_data='start_theater')],
        [InlineKeyboardButton('TIME', callback_data='start_time')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('WELCOME To Movie Ticket BOT.YourChoose an option:', reply_markup=reply_markup)

def main() -> None:
    # Create the Application
    application = ApplicationBuilder().token("6993588387:AAGHwj2liS2hXsxgqpalxYtPjBp11IBRlF4").build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(theater, pattern='^start_theater$'))
    application.add_handler(CallbackQueryHandler(theater_selected, pattern='^theater_'))
    application.add_handler(CallbackQueryHandler(movie_or_time_selected, pattern='^(movie|time)_'))
    application.add_handler(CallbackQueryHandler(showtime_selected, pattern='^showtime_'))
    application.add_handler(CallbackQueryHandler(selected_movie, pattern='^movieselected_'))
    application.add_handler(CallbackQueryHandler(confirm_selection, pattern='^confirm_'))

    application.add_handler(CallbackQueryHandler(movie, pattern='^start_movie$'))
    application.add_handler(CallbackQueryHandler(movie_selected, pattern='^selectedmovie_'))
    application.add_handler(CallbackQueryHandler(theater_or_time_selected, pattern='^(optiontheater|optiontime)_'))
    application.add_handler(CallbackQueryHandler(mshowtime_selected, pattern='^movieshowtime_'))
    application.add_handler(CallbackQueryHandler(mtheater_selected, pattern='^selecttheater_'))

    application.add_handler(CallbackQueryHandler(time, pattern='start_time$'))
    application.add_handler(CallbackQueryHandler(time_selected, pattern='^timeselected_'))
    application.add_handler(CallbackQueryHandler(theater_or_movie_selected, pattern='^(choicetheater|choicemovie)_'))
    application.add_handler(CallbackQueryHandler(select_movie_after_theater, pattern='^select_movie_'))
    application.add_handler(CallbackQueryHandler(select_theater_after_movie, pattern='^select_theater_'))


    application.run_polling()

if __name__ == "__main__":
    main()

