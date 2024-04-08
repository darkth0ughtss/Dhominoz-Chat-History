import telebot
from telebot import types
from pymongo import MongoClient
from sudo import sudo_user_id

bot_token = '6617412135:AAFi7k0BBdGhsoSLm9maa48Z-puqRwA1wvw'
mongo_connection_url = 'mongodb+srv://phantmp:loniko0908@cluster0.nocjks1.mongodb.net/?retryWrites=true&w=majority'

bot = telebot.TeleBot(bot_token)

# Connect to MongoDB
client = MongoClient(mongo_connection_url)
db = client.get_database("fancy_text_bot")  # Replace with your database name
collection = db.get_collection("messages")  # Replace with your collection name
groups_collection = db.get_collection("groups")  # Collection to store group IDs
users_collection = db.get_collection("users")  # Collection to store user IDs


font_mapping = {
    'small_caps': {'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ',
                       'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ',
                       'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ', 'u': 'ᴜ',
                       'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
                       'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ꜰ', 'G': 'ɢ',
                       'H': 'ʜ', 'I': 'ɪ', 'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ',
                       'O': 'ᴏ', 'P': 'ᴘ', 'Q': 'ǫ', 'R': 'ʀ', 'S': 'ꜱ', 'T': 'ᴛ', 'U': 'ᴜ',
                       'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x', 'Y': 'ʏ', 'Z': 'ᴢ', ' ': ' '},

        'double_struck': {'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖', 'f': '𝕗', 'g': '𝕘',
                  'h': '𝕙', 'i': '𝕚', 'j': '𝕛', 'k': '𝕜', 'l': '𝕝', 'm': '𝕞', 'n': '𝕟',
                  'o': '𝕠', 'p': '𝕡', 'q': '𝕢', 'r': '𝕣', 's': '𝕤', 't': '𝕥', 'u': '𝕦',
                  'v': '𝕧', 'w': '𝕨', 'x': '𝕩', 'y': '𝕪', 'z': '𝕫', 'A': '𝔸', 'B': '𝔹',
                  'C': 'ℂ', 'D': '𝔻', 'E': '𝔼', 'F': '𝔽', 'G': '𝔾', 'H': 'ℍ', 'I': '𝕀',
                  'J': '𝕁', 'K': '𝕂', 'L': '𝕃', 'M': '𝕄', 'N': 'ℕ', 'O': '𝕆', 'P': 'ℙ',
                  'Q': 'ℚ', 'R': 'ℝ', 'S': '𝕊', 'T': '𝕋', 'U': '𝕌', 'V': '𝕍', 'W': '𝕎',
                  'X': '𝕏', 'Y': '𝕐', 'Z': 'ℤ', ' ': ' ' },

        'bold': {'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴',
         'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻',
         'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂',
         'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇', 'A': '𝗔', 'B': '𝗕',
         'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛', 'I': '𝗜',
         'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣',
         'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨', 'V': '𝗩', 'W': '𝗪',
         'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭', ' ': ' '},

        'italic': {'a': '𝑎', 'b': '𝑏', 'c': '𝑐', 'd': '𝑑', 'e': '𝑒', 'f': '𝑓', 'g': '𝑔',
           'h': 'ℎ', 'i': '𝑖', 'j': '𝑗', 'k': '𝑘', 'l': '𝑙', 'm': '𝑚', 'n': '𝑛',
           'o': '𝑜', 'p': '𝑝', 'q': '𝑞', 'r': '𝑟', 's': '𝑠', 't': '𝑡', 'u': '𝑢',
           'v': '𝑣', 'w': '𝑤', 'x': '𝑥', 'y': '𝑦', 'z': '𝑧', 'A': '𝐴', 'B': '𝐵',
           'C': '𝐶', 'D': '𝐷', 'E': '𝐸', 'F': '𝐹', 'G': '𝐺', 'H': 'ℍ', 'I': '𝐼',
           'J': '𝐽', 'K': '𝐾', 'L': '𝐿', 'M': '𝑀', 'N': '𝑁', 'O': '𝑂', 'P': '𝑃',
           'Q': '𝑄', 'R': '𝑅', 'S': '𝑆', 'T': '𝑇', 'U': '𝑈', 'V': '𝑉', 'W': '𝑊',
           'X': '𝑋', 'Y': '𝑌', 'Z': '𝑍', ' ': ' '},


        'bold_italic': {'a': '𝒂', 'b': '𝒃', 'c': '𝒄', 'd': '𝒅', 'e': '𝒆', 'f': '𝒇', 'g': '𝒈',
                'h': '𝒉', 'i': '𝒊', 'j': '𝒋', 'k': '𝒌', 'l': '𝒍', 'm': '𝒎', 'n': '𝒏',
                'o': '𝒐', 'p': '𝒑', 'q': '𝒒', 'r': '𝒓', 's': '𝒔', 't': '𝒕', 'u': '𝒖',
                'v': '𝒗', 'w': '𝒘', 'x': '𝒙', 'y': '𝒚', 'z': '𝒛', 'A': '𝑨', 'B': '𝑩',
                'C': '𝑪', 'D': '𝑫', 'E': '𝑬', 'F': '𝑭', 'G': '𝑮', 'H': '𝑯', 'I': '𝑰',
                'J': '𝑱', 'K': '𝑲', 'L': '𝑳', 'M': '𝑴', 'N': '𝑵', 'O': '𝑶', 'P': '𝑷',
                'Q': '𝑸', 'R': '𝑹', 'S': '𝑺', 'T': '𝑻', 'U': '𝑼', 'V': '𝑽', 'W': '𝑾',
                'X': '𝑿', 'Y': '𝒀', 'Z': '𝒁', ' ': ' '},


       'monospace': {'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎', 'f': '𝚏', 'g': '𝚐',
               'h': '𝚑', 'i': '𝚒', 'j': '𝚓', 'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗',
               'o': '𝚘', 'p': '𝚙', 'q': '𝚚', 'r': '𝚛', 's': '𝚜', 't': '𝚝', 'u': '𝚞',
               'v': '𝚟', 'w': '𝚠', 'x': '𝚡', 'y': '𝚢', 'z': '𝚣', 'A': '𝙰', 'B': '𝙱',
               'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶', 'H': '𝙷', 'I': '𝙸',
               'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽', 'O': '𝙾', 'P': '𝙿',
               'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃', 'U': '𝚄', 'V': '𝚅', 'W': '𝚆',
               'X': '𝚇', 'Y': '𝚈', 'Z': '𝚉', ' ': ' '},


        'bodoni': {'a': '𝓪', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮', 'f': '𝓯', 'g': '𝓰',
           'h': '𝓱', 'i': '𝓲', 'j': '𝓳', 'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷',
           'o': '𝓸', 'p': '𝓹', 'q': '𝓺', 'r': '𝓻', 's': '𝓼', 't': '𝓽', 'u': '𝓾',
           'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃', 'A': '𝓐', 'B': '𝓑',
           'C': '𝓒', 'D': '𝓓', 'E': '𝓔', 'F': '𝓕', 'G': '𝓖', 'H': '𝓗', 'I': '𝓘',
           'J': '𝓙', 'K': '𝓚', 'L': '𝓛', 'M': '𝓜', 'N': '𝓝', 'O': '𝓞', 'P': '𝓟',
           'Q': '𝓠', 'R': '𝓡', 'S': '𝓢', 'T': '𝓣', 'U': '𝓤', 'V': '𝓥', 'W': '𝓦',
           'X': '𝓧', 'Y': '𝓨', 'Z': '𝓩', ' ': ' '},


        'futura': {'a': '𝓪', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮', 'f': '𝓯', 'g': '𝓰',
           'h': '𝓱', 'i': '𝓲', 'j': '𝓳', 'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷',
           'o': '𝓸', 'p': '𝓹', 'q': '𝓺', 'r': '𝓻', 's': '𝓼', 't': '𝓽', 'u': '𝓾',
           'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃', 'A': '𝓐', 'B': '𝓑',
           'C': '𝓒', 'D': '𝓓', 'E': '𝓔', 'F': '𝓕', 'G': '𝓖', 'H': '𝓗', 'I': '𝓘',
           'J': '𝓙', 'K': '𝓚', 'L': '𝓛', 'M': '𝓜', 'N': '𝓝', 'O': '𝓞', 'P': '𝓟',
           'Q': '𝓠', 'R': '𝓡', 'S': '𝓢', 'T': '𝓣', 'U': '𝓤', 'V': '𝓥', 'W': '𝓦',
           'X': '𝓧', 'Y': '𝓨', 'Z': '𝓩', ' ': ' '},

         'garamond': {'a': '𝒶', 'b': '𝒷', 'c': '𝒸', 'd': '𝒹', 'e': '𝑒', 'f': '𝒻', 'g': '𝑔',
             'h': '𝒽', 'i': '𝒾', 'j': '𝒿', 'k': '𝓀', 'l': '𝓁', 'm': '𝓂', 'n': '𝓃',
             'o': '𝑜', 'p': '𝓅', 'q': '𝓆', 'r': '𝓇', 's': '𝓈', 't': '𝓉', 'u': '𝓊',
             'v': '𝓋', 'w': '𝓌', 'x': '𝓍', 'y': '𝓎', 'z': '𝓏', 'A': '𝒜', 'B': 'ℬ',
             'C': '𝒞', 'D': '𝒟', 'E': '𝑬', 'F': '𝒻', 'G': '𝒢', 'H': 'ℋ', 'I': 'ℐ',
             'J': '𝒥', 'K': '𝒦', 'L': 'ℒ', 'M': '𝑀', 'N': '𝒩', 'O': '𝒪', 'P': '𝒫',
             'Q': '𝒬', 'R': 'ℛ', 'S': '𝒮', 'T': '𝒯', 'U': '𝒰', 'V': '𝒱', 'W': '𝒲',
             'X': '𝒳', 'Y': '𝒴', 'Z': '𝒵', ' ': ' '},

         'script': {'a': '𝒶', 'b': '𝒷', 'c': '𝒸', 'd': '𝒹', 'e': 'ℯ', 'f': '𝒻', 'g': 'ℊ',
           'h': '𝒽', 'i': '𝒾', 'j': '𝒿', 'k': '𝓀', 'l': '𝓁', 'm': '𝓂', 'n': '𝓃',
           'o': 'ℴ', 'p': '𝓅', 'q': '𝓆', 'r': '𝓇', 's': '𝓈', 't': '𝓉', 'u': '𝓊',
           'v': '𝓋', 'w': '𝓌', 'x': '𝓍', 'y': '𝓎', 'z': '𝓏', 'A': '𝒜', 'B': 'ℬ',
           'C': '𝒞', 'D': '𝒟', 'E': 'ℰ', 'F': 'ℱ', 'G': '𝒢', 'H': 'ℋ', 'I': 'ℐ',
           'J': '𝒥', 'K': '𝒦', 'L': 'ℒ', 'M': 'ℳ', 'N': '𝒩', 'O': '𝒪', 'P': '𝒫',
           'Q': '𝒬', 'R': 'ℛ', 'S': '𝒮', 'T': '𝒯', 'U': '𝒰', 'V': '𝒱', 'W': '𝒲',
           'X': '𝒳', 'Y': '𝒴', 'Z': '𝒵'},
        
    }

def convert_text(input_text, font='double_struck , bold , bodoni , script , monospace , bold_italic , italic , garamond'):
    converted_text = ''
    for char in input_text:
        if char in font_mapping[font]:
            converted_text += font_mapping[font][char]
        else:
            converted_text += char
    return converted_text

# Load message from MongoDB
def load_message(message_type):
    message_document = collection.find_one({'type': message_type})
    if message_document:
        return message_document['message']
    else:
        return None

# Save message to MongoDB
def save_message(message_type, message_text):
    collection.update_one({'type': message_type}, {'$set': {'message': message_text}}, upsert=True)

welcome_message = load_message('start_message') or (
    "🌐 Welcome to the Fancy Text Converter Bot! 🚀\n\n"
    "Experience the power of text transformation with elegance and style.\n\n"
    "To begin, explore available commands by typing /help.\n\n"
    "Start typing and let the magic unfold! ✨"
)

help_message = load_message('help_message') or """
🌟 𝐇𝐞𝐥𝐩 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 🌟

Welcome to Fancy Text Converter Bot! This bot allows you to transform your text into various stylish fonts. Here's how you can use it:

- Use /ds to convert text into 𝕕𝕠𝕦𝕓𝕝𝕖 𝕤𝕥𝕣𝕦𝕔𝕜 style.
- Use /mo for 𝚖𝚘𝚗𝚘𝚜𝚙𝚎𝚊𝚌𝚎 style.
- Use /bd for 𝑩𝒐𝒅𝒐𝒏𝒊 touch.
- Use /gad for 𝔾𝕒𝕣𝕒𝕞𝕠𝕟𝕕 vibes.
- Use /ftr for 𝗙𝘂𝘁𝘂𝗿𝗮 style.
- Use /bo to add boldness to your text.
- Use /it to make your text italic.
- Use /boit to combine bold and italic.
- Use /sc for 𝖘𝖒𝖆𝖑𝖑 𝖈𝖆𝖕𝖘.

Explore these commands and create unique text expressions. If you ever need assistance, just type /help to get this guide.

Enjoy transforming your text with Fancy Text Converter Bot! 🎨
"""

# Command handler for sudo users to edit the start/help message
@bot.message_handler(commands=['edit_start', 'edit_help'])
def handle_edit_message(message):
    message_type = 'start_message' if message.text == '/edit_start' else 'help_message'
    # Check if the user is a sudo user
    if message.from_user.id == sudo_user_id:
        # Ask the sudo user to provide the new message
        bot.send_message(message.chat.id, f"Please provide the new {message_type.replace('_', ' ').title()}:")
        # Register the handler for receiving the new message
        bot.register_next_step_handler(message, process_edit_message, message_type)
    else:
        bot.send_message(message.chat.id, "🛑 You are not authorized to edit the message")

# Function to process the new message provided by the sudo user
def process_edit_message(message, message_type):
    global welcome_message, help_message
    # Update the message based on the message type
    if message_type == 'start_message':
        welcome_message = message.text
    else:
        help_message = message.text
    # Save the updated message to MongoDB
    save_message(message_type, message.text)
    bot.send_message(message.chat.id, f"✅ {message_type.replace('_', ' ').title()} updated successfully")

# Command handler for /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    print("Received /start command in chat:", message.chat.id, "of type:", message.chat.type)
    # Save group ID if it's a group or supergroup
    if message.chat.type in ['group', 'supergroup']:
        print("Saving group ID:", message.chat.id)
        groups_collection.update_one({'group_id': message.chat.id}, {'$set': {'group_id': message.chat.id}}, upsert=True)
    # Save user ID
    users_collection.update_one({'user_id': message.from_user.id}, {'$set': {'user_id': message.from_user.id}}, upsert=True)
    
    # Construct the Telegram link with the user's first name and user ID
    user_link = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
    
    # Update the welcome message to include the user's name as a link
    welcome_message_with_name = f"ʜᴇʏ ᴛʜᴇʀᴇ {user_link}!\n\n" + welcome_message
    
    # Send the updated welcome message
    markup = types.InlineKeyboardMarkup()
    owner_button = types.InlineKeyboardButton("👽 Owner", url="https://t.me/senpaiii10")
    markup.add(owner_button)
    bot.send_message(message.chat.id, welcome_message_with_name, reply_markup=markup, parse_mode='HTML')

# Command handler for /botinfo
@bot.message_handler(commands=['botinfo'])
def handle_botinfo(message):
    # Check if the user is a sudo user
    if message.from_user.id == sudo_user_id:
        # Count the number of groups and users dynamically
        num_groups = groups_collection.count_documents({})
        num_users = users_collection.count_documents({})
        # Send the bot information to the sudo user
        bot.send_message(message.chat.id, f"ℹ️ Bot Information:\n\nNumber of Groups: {num_groups}\nNumber of Users: {num_users}")
    else:
        bot.send_message(message.chat.id, "🛑 You are not authorized to access bot information")


# Command handler for /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    # Send the help_message
    bot.send_message(message.chat.id, help_message)

 
 
# Command handler for /double_struck
@bot.message_handler(commands=['ds'])
def handle_double_struck(message):
    command_parts = message.text.split(' ', 1)
    text_to_convert = command_parts[1] if len(command_parts) > 1 else ''

    if text_to_convert:
        converted_text = convert_text(text_to_convert, 'double_struck')
        bot.send_message(message.chat.id, f"{converted_text}")
    else:
        bot.send_message(message.chat.id, "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘁𝗲𝘅𝘁 𝘁𝗼 𝗰𝗼𝗻𝘃𝗲𝗿𝘁.\n\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /ds (𝑻𝒆𝒙𝒕𝑻𝑶𝑪𝒐𝒏𝒗𝒆𝒓𝒕)")

# Command handler for /monospace
@bot.message_handler(commands=['mo'])
def handle_monospace(message):
    command_parts = message.text.split(' ', 1)
    text_to_convert = command_parts[1] if len(command_parts) > 1 else ''

    if text_to_convert:
        converted_text = convert_text(text_to_convert, 'monospace')
        bot.send_message(message.chat.id, f"{converted_text}")
    else:
        bot.send_message(message.chat.id, "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘁𝗲𝘅𝘁 𝘁𝗼 𝗰𝗼𝗻𝘃𝗲𝗿𝘁. \n\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /mo (𝑻𝒆𝒙𝒕𝑻𝑶𝑪𝒐𝒏𝒗𝒆𝒓𝒕)")

# Command handler for /bodoni
@bot.message_handler(commands=['bd'])
def handle_bodoni(message):
    command_parts = message.text.split(' ', 1)
    text_to_convert = command_parts[1] if len(command_parts) > 1 else ''

    if text_to_convert:
        converted_text = convert_text(text_to_convert, 'bodoni')
        bot.send_message(message.chat.id, f"{converted_text}")
    else:
        bot.send_message(message.chat.id, "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘁𝗲𝘅𝘁 𝘁𝗼 𝗰𝗼𝗻𝘃𝗲𝗿𝘁. \n\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /bd (𝑻𝒆𝒙𝒕𝑻𝑶𝑪𝒐𝒏𝒗𝒆𝒓𝒕)")

# Command handler for /garamond
@bot.message_handler(commands=['gad'])
def handle_bodoni(message):
    command_parts = message.text.split(' ', 1)
    text_to_convert = command_parts[1] if len(command_parts) > 1 else ''

    if text_to_convert:
        converted_text = convert_text(text_to_convert, 'garamond')
        bot.send_message(message.chat.id, f"{converted_text}")
    else:
        bot.send_message(message.chat.id, "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘁𝗲𝘅𝘁 𝘁𝗼 𝗰𝗼𝗻𝘃𝗲𝗿𝘁. \n\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /gad (𝑻𝒆𝒙𝒕𝑻𝑶𝑪𝒐𝒏𝒗𝒆𝒓𝒕)")

# Command handler for /futura
@bot.message_handler(commands=['ftr'])
def handle_futura(message):
    command_parts = message.text.split(' ', 1)
    text_to_convert = command_parts[1] if len(command_parts) > 1 else ''

    if text_to_convert:
        converted_text = convert_text(text_to_convert, 'futura')
        bot.send_message(message.chat.id, f"{converted_text}")
    else:
        bot.send_message(message.chat.id, "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘁𝗲𝘅𝘁 𝘁𝗼 𝗰𝗼𝗻𝘃𝗲𝗿𝘁. \n\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /ftr (𝑻𝒆𝒙𝒕𝑻𝑶𝑪𝒐𝒏𝒗𝒆𝒓𝒕)")


# Command handler for /bold
@bot.message_handler(commands=['bo'])
def handle_bold(message):
    command_parts = message.text.split(' ', 1)
    text_to_convert = command_parts[1] if len(command_parts) > 1 else ''

    if text_to_convert:
        converted_text = convert_text(text_to_convert, 'bold')
        bot.send_message(message.chat.id, f"{converted_text}")
    else:
        bot.send_message(message.chat.id, "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘁𝗲𝘅𝘁 𝘁𝗼 𝗰𝗼𝗻𝘃𝗲𝗿𝘁. \n\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /bo (𝑻𝒆𝒙𝒕𝑻𝑶𝑪𝒐𝒏𝒗𝒆𝒓𝒕)")

# Command handler for /italic
@bot.message_handler(commands=['it'])
def handle_italic(message):
    command_parts = message.text.split(' ', 1)
    text_to_convert = command_parts[1] if len(command_parts) > 1 else ''

    if text_to_convert:
        converted_text = convert_text(text_to_convert, 'italic')
        bot.send_message(message.chat.id, f"{converted_text}")
    else:
        bot.send_message(message.chat.id, "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘁𝗲𝘅𝘁 𝘁𝗼 𝗰𝗼𝗻𝘃𝗲𝗿𝘁. \n\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /it (𝑻𝒆𝒙𝒕𝑻𝑶𝑪𝒐𝒏𝒗𝒆𝒓𝒕)")

# Command handler for /bold_italic
@bot.message_handler(commands=['boit'])
def handle_bold_italic(message):
    command_parts = message.text.split(' ', 1)
    text_to_convert = command_parts[1] if len(command_parts) > 1 else ''

    if text_to_convert:
        converted_text = convert_text(text_to_convert, 'bold_italic')
        bot.send_message(message.chat.id, f"{converted_text}")
    else:
        bot.send_message(message.chat.id, "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘁𝗲𝘅𝘁 𝘁𝗼 𝗰𝗼𝗻𝘃𝗲𝗿𝘁. \n\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /boit (𝑻𝒆𝒙𝒕𝑻𝑶𝑪𝒐𝒏𝒗𝒆𝒓𝒕)")

# Command handler for /small_caps
@bot.message_handler(commands=['sc'])
def handle_small_caps(message):
    command_parts = message.text.split(' ', 1)
    text_to_convert = command_parts[1] if len(command_parts) > 1 else ''

    if text_to_convert:
        converted_text = convert_text(text_to_convert, 'small_caps')
        bot.send_message(message.chat.id, f"{converted_text}")
    else:
        bot.send_message(message.chat.id, "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘁𝗲𝘅𝘁 𝘁𝗼 𝗰𝗼𝗻𝘃𝗲𝗿𝘁. \n\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /sc (𝑻𝒆𝒙𝒕𝑻𝑶𝑪𝒐𝒏𝒗𝒆𝒓𝒕)")

# Command handler for /broadcast
@bot.message_handler(commands=['broadcast'])
def handle_broadcast(message):
    # Check if the user is a sudo user
    if message.from_user.id == sudo_user_id:
        # Check if the message is a reply to another message
        if message.reply_to_message:
            # Check if the replied message contains text or photo with or without caption
            if message.reply_to_message.text:
                # Extract the broadcast message from the replied message
                broadcast_text = message.reply_to_message.text
                # Retrieve all user IDs from the database
                user_ids = [doc['user_id'] for doc in users_collection.find({}, {'_id': 0, 'user_id': 1})]
                # Retrieve all group IDs from the database
                group_ids = [doc['group_id'] for doc in groups_collection.find({}, {'_id': 0, 'group_id': 1})]

                # Send the broadcast message to users
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, broadcast_text)
                    except Exception as e:
                        print(f"Error sending message to user {user_id}: {e}")

                # Send the broadcast message to groups
                for group_id in group_ids:
                    try:
                        bot.send_message(group_id, broadcast_text)
                    except Exception as e:
                        print(f"Error sending message to group {group_id}: {e}")

                # Calculate the total count of users and groups
                total_count = len(user_ids) + len(group_ids)

                # Send confirmation message to the sudo user with total count
                confirmation_message = f"Broadcast sent successfully!\n\nMessages sent to {total_count} users and groups."
                bot.send_message(message.chat.id, confirmation_message)
            elif message.reply_to_message.photo:
                # Extract the photo file ID and caption from the replied message
                photo_file_id = message.reply_to_message.photo[-1].file_id
                caption = message.reply_to_message.caption
                
                # Save the photo and caption to the database (temporarily)
                photo_data = {'file_id': photo_file_id, 'caption': caption}
                db.temp_photos.insert_one(photo_data)

                # Retrieve all user IDs from the database
                user_ids = [doc['user_id'] for doc in users_collection.find({}, {'_id': 0, 'user_id': 1})]
                # Retrieve all group IDs from the database
                group_ids = [doc['group_id'] for doc in groups_collection.find({}, {'_id': 0, 'group_id': 1})]

                # Send the photo with caption to users
                for user_id in user_ids:
                    try:
                        bot.send_photo(user_id, photo_file_id, caption=caption)
                    except Exception as e:
                        print(f"Error sending photo to user {user_id}: {e}")

                # Send the photo with caption to groups
                for group_id in group_ids:
                    try:
                        bot.send_photo(group_id, photo_file_id, caption=caption)
                    except Exception as e:
                        print(f"Error sending photo to group {group_id}: {e}")

                # Calculate the total count of users and groups
                total_count = len(user_ids) + len(group_ids)

                # Send confirmation message to the sudo user with total count
                confirmation_message = f"Broadcast sent successfully!\n\nPhotos sent to {total_count} users and groups."
                bot.send_message(message.chat.id, confirmation_message)

                # Delete the photo and caption from the database (temporarily)
                db.temp_photos.delete_one({'file_id': photo_file_id})

        else:
            bot.send_message(message.chat.id, "🛑 Please reply to a message containing the text or photo you want to broadcast.")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use the /broadcast command")


bot.polling()
