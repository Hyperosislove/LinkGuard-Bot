import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot Configuration
API_ID = "your_api_id"  # Get from my.telegram.org
API_HASH = "your_api_hash"  # Get from my.telegram.org
BOT_TOKEN = "your_bot_token"  # Get from BotFather

# Initialize the Bot
app = Client("link_remover_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Professional Message Template
START_MESSAGE = """
👋 **Welcome to Link & Mention Remover Bot!**

I am here to help you maintain a clean and safe environment in your group by:
- Automatically removing **all links** and **@ mentions**.
- Sending polite warnings to users who violate the rules.
- Helping to prevent **spam** and **scam** messages.

**➤ Add me to your group and give me admin rights to get started!**

Thank you for choosing a professional solution for your group management. 🚀
"""

WARNING_TEMPLATE = """
🚫 **Warning!**  
Dear {username}, posting links or mentions is not allowed in this group. Please follow the rules to avoid further actions.  
Thank you!  
"""

# Function to check for links or mentions
def contains_prohibited_content(message_text):
    # Check for URLs or links
    if re.search(r"http[s]?://|www\.", message_text):
        return True
    # Check for @ mentions
    if re.match(r"^@[\w\d]+", message_text):
        return True
    return False

# Handler for the /start command
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    # Professional Start Menu
    buttons = [
        [
            InlineKeyboardButton("➕ Add me to your group", url="https://t.me/your_bot_username?startgroup=true"),
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        ],
        [
            InlineKeyboardButton("📞 Contact Admin", url="https://t.me/your_admin_username"),
        ]
    ]
    await message.reply_text(
        START_MESSAGE,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="markdown"
    )

# Handler for callback queries (e.g., Help button)
@app.on_callback_query(filters.regex("help"))
async def help(client, callback_query):
    await callback_query.message.edit_text(
        "**How to use me:**\n\n"
        "- Add me to your group.\n"
        "- Give me admin rights (with message delete permission).\n"
        "- I will automatically remove all links and mentions from your group.\n\n"
        "For further assistance, contact the admin.",
        parse_mode="markdown"
    )

# Handler for messages in the group
@app.on_message(filters.group & ~filters.service)  # Ignore service messages (e.g., user joined)
async def check_message(client, message):
    if message.text and contains_prohibited_content(message.text):
        # Delete the prohibited message
        await message.delete()

        # Warn the user
        user = message.from_user
        warning_message = await message.reply_text(
            WARNING_TEMPLATE.format(username=f"@{user.username}" if user.username else user.first_name),
            parse_mode="markdown"
        )

        # Wait 10 seconds before deleting the warning
        await asyncio.sleep(10)
        await warning_message.delete()

# Run the bot
if __name__ == "__main__":
    app.run()
