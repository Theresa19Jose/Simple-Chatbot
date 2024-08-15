import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler, ApplicationBuilder

# JSON data as a string
json_data = '''
{
    "times": ["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM"],
    "show_times": {
        "Theater 1": {
            "Movie A": ["10:00 AM"],
            "Movie B": ["1:00 PM"]
        },
        "Theater 2": {
            "Movie A": ["1:00 PM"],
            "Movie C": ["4:00 PM"]
        },
        "Theater 3": {
            "Movie B": ["4:00 PM"],
            "Movie C": ["7:00 PM"]
        }
    }
}
'''

# Load data from JSON string
data = json.loads(json_data)

# Handler for selecting a time
async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton(time, callback_data=f'timeselected_{time}')] for time in data['times']]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text('Select a Time:', reply_markup=reply_markup)
    
    

# Handler for when a time is selected
async def time_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    time = query.data.split('_')[1]
    context.user_data['selected_time'] = time

    keyboard = [
        [InlineKeyboardButton('THEATER', callback_data=f'choicetheater_{time}')],
        [InlineKeyboardButton('MOVIE', callback_data=f'choicemovie_{time}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f'Selected Time: {time}. Choose an option:', reply_markup=reply_markup)

# Handler for selecting a theater or movie after a time is selected
async def theater_or_movie_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    option = data_parts[0].replace('choice', '')
    time = data_parts[1]
    
    if option == 'theater':
        # Filter theaters based on the selected time
        available_theaters = [theater for theater, showtimes in data['show_times'].items() if any(time in times for times in showtimes.values())]
        keyboard = [[InlineKeyboardButton(theater, callback_data=f'select_movie_{time}_{theater}')] for theater in available_theaters]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f'Selected Time: {time}. Choose a theater:', reply_markup=reply_markup)
    elif option == 'movie':
        # Filter movies based on the selected time
        available_movies = set()
        for theater, showtimes in data['show_times'].items():
            for movie, times in showtimes.items():
                if time in times:
                    available_movies.add(movie)
        keyboard = [[InlineKeyboardButton(movie, callback_data=f'select_theater_{time}_{movie}')] for movie in available_movies]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f'Selected Time: {time}. Choose a movie:', reply_markup=reply_markup)

# Handler for selecting a movie after a theater is selected
async def select_movie_after_theater(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    time = data_parts[2]
    theater = data_parts[3]
    print(time)
    print(theater)
    
    # Filter movies based on the chosen theater and time
    available_movies = [movie for movie, times in data['show_times'][theater].items() if time in times]
    keyboard = [[InlineKeyboardButton(movie, callback_data=f'confirm_{movie}_{theater}_{time}')] for movie in available_movies]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f'Selected Theater: {theater}. Choose a movie:', reply_markup=reply_markup)

# Handler for selecting a theater after a movie is selected
async def select_theater_after_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    time = data_parts[2]
    movie = data_parts[3]
    print(movie)
    
    # Filter theaters based on the chosen movie and time
    available_theaters = [theater for theater, showtimes in data['show_times'].items() if movie in showtimes and time in showtimes[movie]]
    keyboard = [[InlineKeyboardButton(theater, callback_data=f'confirm_{movie}_{theater}_{time}')] for theater in available_theaters]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f'Selected Movie: {movie}. Choose a theater:', reply_markup=reply_markup)

# Handler for confirming the selection
async def confirm_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    time = data_parts[1]
    theater = data_parts[2]
    movie = data_parts[3]
    
    await query.edit_message_text(f'Booking confirmed!\nTime: {time}\nTheater: {theater}\nMovie: {movie}')