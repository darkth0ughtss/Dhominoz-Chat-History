import telebot

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6617412135:AAFi7k0BBdGhsoSLm9maa48Z-puqRwA1wvw')

# Define a handler for the '/start' command
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Hello! I'm your Telegram bot. How can I assist you today?")

# Define a handler for regular messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "I'm sorry, I didn't understand that command.")

# Polling the bot to listen for new messages
bot.polling()
