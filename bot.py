import telebot
from telebot import types
from pymongo import MongoClient
from config import BOT_TOKEN, MONGODB_URI, CHANNEL_ID , GROUP_ID

# Replace 'YOUR_TOKEN' with your actual bot token
bot = telebot.TeleBot(BOT_TOKEN)

# Connect to MongoDB Atlas and specify the default database and collection
client = MongoClient(MONGODB_URI)
db = client['Dhominoz']
messages_collection = db['Logging']

@bot.message_handler(content_types=['photo', 'video', 'audio', 'voice'])
def handle_media(message):
    # Get the user's first name
    user_first_name = message.from_user.first_name
    
    # Download the media file
    file_id = message.photo[-1].file_id if message.content_type == 'photo' else message.audio.file_id if message.content_type == 'audio' else message.video.file_id if message.content_type == 'video' else message.voice.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)
    
    # Save the media file to MongoDB along with user ID
    messages_collection.insert_one({
        'user_id': message.from_user.id,
        'user_first_name': user_first_name,
        'media': downloaded_file,
        'media_type': message.content_type
    })
    
    # Forward the media file to the specified channel with user's first name as caption
    bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)
    
    # Delete the media file from MongoDB
    messages_collection.delete_one({'user_id': message.from_user.id, 'media_type': message.content_type})


@bot.message_handler(func=lambda message: True)
def forward_message_to_channel(message):
    if message.chat.type == 'supergroup':
        # Forward text messages to the specified channel
        bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)

bot.polling()
