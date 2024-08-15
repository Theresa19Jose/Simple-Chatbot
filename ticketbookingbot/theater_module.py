import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

json_data = '''
{
    "theaters": ["Theater 1", "Theater 2", "Theater 3"],
    "movies": {
        "Theater 1": ["Movie A", "Movie B"],
        "Theater 2": ["Movie A", "Movie C"],
        "Theater 3": ["Movie B", "Movie C"]
    },
    "times": {
        "Theater 1": ["10:00 AM", "1:00 PM"],
        "Theater 2": ["1:00 PM", "4:00 PM"],
        "Theater 3": ["4:00 PM", "7:00 PM"]
    },
    "show_times": {
        "Theater 1": {
            "Movie A": ["10:00 AM", "1:00 PM"],
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

# Handler for selecting a theater
async def theater(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton(theater, callback_data=f'theater_{theater}')] for theater in data['theaters']]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text('Select a theater:', reply_markup=reply_markup)

# Handler for when a theater is selected
async def theater_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    theater = query.data.split('_')[1]
    context.user_data['selected_theater'] = theater
    
    keyboard = [
        [InlineKeyboardButton('MOVIE', callback_data=f'movie_{theater}')],
        [InlineKeyboardButton('TIME', callback_data=f'time_{theater}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f'Selected Theater: {theater}. Choose an option:', reply_markup=reply_markup)

# Handler for selecting a movie or time after a theater is selected
async def movie_or_time_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    option = data_parts[0]
    theater = data_parts[1]
    
    if option == 'movie':
        keyboard = [[InlineKeyboardButton(movie, callback_data=f'showtime_{theater}_{movie}')] for movie in data['movies'][theater]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f'Selected Theater: {theater}. Choose a movie:', reply_markup=reply_markup)
    elif option == 'time':
        keyboard = [[InlineKeyboardButton(time, callback_data=f'movieselected_{theater}_{time}')] for time in data['times'][theater]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f'Selected Theater: {theater}. Choose a time:', reply_markup=reply_markup)

# Handler for selecting a showtime after a movie is selected
async def showtime_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    theater = data_parts[1]
    movie = data_parts[2]
    print(movie)

    keyboard = [[InlineKeyboardButton(time, callback_data=f'confirm_{theater}_{movie}_{time}')] for time in data['show_times'][theater][movie]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f'Selected Theater: {theater}. Selected Movie: {movie}. Choose a showtime:', reply_markup=reply_markup)

# Handler for selecting a movie after a time is selected
async def selected_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    theater = data_parts[1]
    time = data_parts[2]
    print(theater)

    # Filter movies based on chosen time
    available_movies = [movie for movie, showtimes in data['show_times'][theater].items() if time in showtimes]

    keyboard = [[InlineKeyboardButton(movie, callback_data=f'confirm_{theater}_{movie}_{time}')] for movie in available_movies]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f'Selected Theater: {theater}. Selected Time: {time}. Choose a movie:', reply_markup=reply_markup)

# Handler for confirming the selection
async def confirm_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    theater = data_parts[1]
    movie = data_parts[2]
    time = data_parts[3]
    
    await query.edit_message_text(f'Booking confirmed!\nTheater: {theater}\nMovie: {movie}\nShowtime: {time}')
