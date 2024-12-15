import os
import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Fetch environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot
app = Client("link_remover_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Professional messages
START_MESSAGE = """
👋 **Welcome to LinkGuard Bot!**

I help keep your group clean and safe by:
- Removing **all links** and **@ mentions**.
- Sending polite warnings to violators.
- Preventing spam and scams.

**➤ Add me to your group and make me an admin to activate my features.**
"""

HELP_MESSAGE = """
📖 **How to use LinkGuard Bot:**

1. **Add me to your group.**
2. **Make me an admin** (with delete messages permission).
3. I will:
   - Automatically remove all links and mentions.
   - Send warnings to violators.

For further assistance, contact the developer.
"""

DEVELOPER_INFO_MESSAGE = """
👨‍💻 **Developer Info:**

**Name**: Hyperosis Love  
**Username**: [@hyperosislove](https://t.me/hyperosislove)  
**About**: A passionate developer focused on automation and security.  
**Contact**: Reach out to me anytime via [Telegram](https://t.me/hyperosislove).  
"""

WARNING_TEMPLATE = """
🚫 **Warning!**  
Dear {username}, posting links or mentions is not allowed in this group.  
Please follow the rules to avoid further actions. Thank you!  
"""

# Function to check for links or mentions
def contains_prohibited_content(message_text):
    return bool(re.search(r"http[s]?://|www\.|^@[\w\d]+", message_text))

# /start command handler
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    buttons = [
        [
            InlineKeyboardButton("➕ Add me to your group", url="https://t.me/your_bot_username?startgroup=true"),
            InlineKeyboardButton("ℹ️ How to Use", callback_data="help"),
        ],
        [
            InlineKeyboardButton("📞 Contact Developer", url="https://t.me/hyperosislove"),
        ],
    ]
    try:
        await message.reply_text(
            "Welcome to LinkGuard Bot!\n\n"
            "This bot helps you keep your group clean by removing links and mentions.\n"
            "Click the buttons below to get started.",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown",
        )
    except ValueError:
        await message.reply_text(
            "Welcome to LinkGuard Bot!\n\n"
            "This bot helps you keep your group clean by removing links and mentions.\n"
            "Click the buttons below to get started.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

# Callback query handler for help
@app.on_callback_query(filters.regex("help"))
async def help(client, callback_query):
    try:
        await callback_query.message.edit_text(
            HELP_MESSAGE,
            parse_mode="Markdown",
        )
    except ValueError:
        await callback_query.message.edit_text(
            HELP_MESSAGE,
        )

# Callback query handler for developer info
@app.on_callback_query(filters.regex("developer_info"))
async def developer_info(client, callback_query):
    try:
        await callback_query.message.edit_text(
            DEVELOPER_INFO_MESSAGE,
            parse_mode="Markdown",
        )
    except ValueError:
        await callback_query.message.edit_text(
            DEVELOPER_INFO_MESSAGE,
        )

# Group message handler
@app.on_message(filters.group & ~filters.service)
async def check_message(client, message):
    if message.text and contains_prohibited_content(message.text):
        await message.delete()  # Delete prohibited message
        user = message.from_user
        warning_message = await message.reply_text(
            WARNING_TEMPLATE.format(username=f"@{user.username}" if user.username else user.first_name),
            parse_mode="Markdown",
        )
        await asyncio.sleep(10)  # Wait 10 seconds
        await warning_message.delete()  # Delete warning message

# Run the bot
if __name__ == "__main__":
    app.run()
