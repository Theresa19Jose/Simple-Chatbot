import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

json_data = '''
{
    "movies": ["Movie A","Movie B", "Movie C"],
    "theater" : {
        "Movie A": ["Theater 1", "Theater 2"],
        "Movie B": ["Theater 1", "Theater 3"],
        "Movie C": ["Theater 2", "Theater 3"]
    },
    "times":{
        "Movie A": ["10:00 AM", "1:00 PM"],
        "Movie B": ["1:00 PM", "4:00 PM"],
        "Movie C": ["4:00 PM", "7:00 PM"]
    },
    "show_times": {
        "Movie A": 
        {
            "Theater 1": ["10:00 AM"],
            "Theater 2": ["1:00 PM"]
        },
        "Movie B":
        {
            "Theater 1": ["1:00 PM"],
            "Theater 3": ["4:00 PM"]
        },
        "Movie C":
        {
            "Theater 2": ["4:00 PM"],
            "Theater 3": ["7:00 PM"]
        }
    }
}
'''

# Load data from JSON string
data = json.loads(json_data)

# Handler for selecting a movie
async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton(movie, callback_data=f'selectedmovie_{movie}')] for movie in data['movies']]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text('Select a Movie:', reply_markup=reply_markup)

# Handler for when a movie is selected
async def movie_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    movie = query.data.split('_')[1]
    context.user_data['selected_movie'] = movie
    
    keyboard = [
        [InlineKeyboardButton('THEATER', callback_data=f'optiontheater_{movie}')],
        [InlineKeyboardButton('TIME', callback_data=f'optiontime_{movie}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f'Selected Movie: {movie}. Choose an option:', reply_markup=reply_markup)

# Handler for selecting a theater or time after a movie is selected
async def theater_or_time_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    option = data_parts[0]
    movie = data_parts[1]
    
    if option == 'optiontheater':
        keyboard = [[InlineKeyboardButton(theater, callback_data=f'movieshowtime_{movie}_{theater}')] for theater in data['theater'][movie]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f'Selected movie: {movie}. Choose a theater:', reply_markup=reply_markup)
    elif option == 'optiontime':
        keyboard = [[InlineKeyboardButton(time, callback_data=f'selecttheater_{movie}_{time}')] for time in data['times'][movie]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f'Selected Movie: {movie}. Choose a time:', reply_markup=reply_markup)

# Handler for selecting a showtime after a theater is selected
async def mshowtime_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    movie = data_parts[1]
    theater = data_parts[2]

    keyboard = [[InlineKeyboardButton(time, callback_data=f'confirm_{theater}_{movie}_{time}')] for time in data['show_times'][movie][theater]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f'Selected Movie: {movie}. Selected Theater: {theater}. Choose a showtime:', reply_markup=reply_markup)

# Handler for selecting a theater after a time is selected
async def mtheater_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    movie = data_parts[1]
    time = data_parts[2]

    # Filter theaters based on chosen time
    available_theaters = [theater for theater, showtimes in data['show_times'][movie].items() if time in showtimes]

    keyboard = [[InlineKeyboardButton(theater, callback_data=f'confirm_{movie}_{theater}_{time}')] for theater in available_theaters]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f'Selected Movie: {movie}. Selected Time: {time}. Choose a theater:', reply_markup=reply_markup)

# Handler for confirming the selection
async def confirm_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data_parts = query.data.split('_')
    movie = data_parts[1]
    theater = data_parts[2]
    time = data_parts[3]
    
    await query.edit_message_text(f'Booking confirmed!\nMovie: {movie}\nTheater: {theater}\nShowtime: {time}')
