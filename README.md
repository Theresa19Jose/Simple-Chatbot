# Chatbot
# Simple Chatbot with Python and Telegram API

This repository contains the code for a simple chatbot developed using Python and the Telegram API. The bot can interact with users, respond to common greetings, and even request phone numbers through an interactive button. This project was created during an internship by a team of talented developers.

## Features

- **Responsive Commands:** The bot can handle various commands like `/start`, `/help`, and custom commands to guide users.
- **Interactive Chat:** It responds to messages, making conversations engaging and informative.
- **Contact Sharing:** Users can easily share their phone numbers with the bot through an interactive button.
- **Error Handling:** Robust error handling to ensure smooth operation.

## Tech Stack

- **Programming Language:** Python 🐍
- **Framework:** Python Telegram Bot API

## Getting Started

### Prerequisites

- Python 3.6 or higher
- `python-telegram-bot` library

You can install the required library using pip:

```bash
pip install python-telegram-bot
```

### Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/simple-telegram-chatbot.git
cd simple-telegram-chatbot
```

2. Replace the `TOKEN` variable in the `bot.py` file with your Telegram bot token:

```python
TOKEN: Final[str] = 'Enter your chatbot token'
```

3. Run the bot:

```bash
python bot.py
```

## Bot Commands

- `/start`: Initiates a conversation with the bot and requests the user's phone number.
- `/help`: Provides information on how to interact with the bot.
- `/custom`: A custom command that you can modify to fit your needs.

## Response Logic

The bot can handle a variety of text inputs, including greetings, questions about its name, capabilities, and jokes. It provides appropriate responses based on the user's input.

## Example Usage

### Starting the Bot

Send the `/start` command to initiate a conversation with the bot. The bot will greet you and request your phone number.

### Sending a Message

You can send various text messages to the bot, and it will respond based on the predefined logic. For example:

- User: "Hi"
- Bot: "Hey there!"

- User: "How are you?"
- Bot: "I am good, thanks! How are you?"

- User: "Tell me a joke"
- Bot: "Why did the scarecrow win an award? Because he was outstanding in his field!"

### Sharing Contact

When prompted, you can share your phone number with the bot using the provided button.

## Error Handling

The bot includes an error handler to log and manage any issues that occur during execution.

## Contributing

Feel free to fork this repository and make your own changes. Pull requests are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


