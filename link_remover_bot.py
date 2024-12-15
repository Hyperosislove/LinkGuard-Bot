import os
import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Fetch environment variables from Heroku Config Vars
API_ID = int(os.getenv("API_ID"))  # Replace 'your_api_id' with the Config Var
API_HASH = os.getenv("API_HASH")  # Replace 'your_api_hash' with the Config Var
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Replace 'your_bot_token' with the Config Var

# Initialize the bot
app = Client("link_remover_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Professional message templates
START_MESSAGE = """
👋 **Welcome to LinkGuard Bot!**

I help keep your group clean and safe by:
- Removing **all links** and **@ mentions**.
- Sending polite warnings to users who violate rules.
- Preventing spam and scam messages.

**➤ Add me to your group and give admin rights to activate me!**

**Developed by [@hyperosislove](https://t.me/hyperosislove)**  
Thank you for choosing a professional solution for your group management. 🚀
"""

WARNING_TEMPLATE = """
🚫 **Warning!**  
Dear {username}, posting links or mentions is not allowed in this group.  
Please follow the rules to avoid further actions. Thank you!  
"""

# Function to check for links or mentions
def contains_prohibited_content(message_text):
    if re.search(r"http[s]?://|www\.", message_text):  # Check for URLs
        return True
    if re.match(r"^@[\w\d]+", message_text):  # Check for mentions
        return True
    return False

# /start command handler
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    buttons = [
        [
            InlineKeyboardButton("➕ Add me to your group", url="https://t.me/your_bot_username?startgroup=true"),
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        ],
        [
            InlineKeyboardButton("📞 Contact Developer", url="https://t.me/hyperosislove"),
        ]
    ]
    await message.reply_text(
        START_MESSAGE,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="markdown"
    )

# Callback query handler (e.g., Help button)
@app.on_callback_query(filters.regex("help"))
async def help(client, callback_query):
    await callback_query.message.edit_text(
        "**How to use me:**\n\n"
        "- Add me to your group.\n"
        "- Give me admin rights (with message delete permission).\n"
        "- I will automatically remove all links and mentions from your group.\n\n"
        "For further assistance, contact the developer.",
        parse_mode="markdown"
    )

# Group message handler
@app.on_message(filters.group & ~filters.service)
async def check_message(client, message):
    if message.text and contains_prohibited_content(message.text):
        await message.delete()  # Delete prohibited message
        user = message.from_user
        warning_message = await message.reply_text(
            WARNING_TEMPLATE.format(username=f"@{user.username}" if user.username else user.first_name),
            parse_mode="markdown"
        )
        await asyncio.sleep(10)  # Wait 10 seconds
        await warning_message.delete()  # Delete warning message

# Run the bot
if __name__ == "__main__":
    app.run()
