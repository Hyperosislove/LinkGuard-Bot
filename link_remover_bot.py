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

# Escape MarkdownV2 characters
def escape_markdown_v2(text):
    escape_chars = r"_|*[]()~`>#+-=|{}.!"
    return "".join("\\" + char if char in escape_chars else char for char in text)

# Messages
START_MESSAGE = escape_markdown_v2("""
👋 **Welcome to LinkGuard Bot!**

I am designed to keep your group safe by:
- Removing **all links** and **mentions**.
- Sending polite warnings to rule violators.
- Ensuring a clean and spam-free environment.

**➤ Add me to your group and make me an admin to activate my features.**

Thank you for choosing a professional group management solution! 🚀
""")

ABOUT_DEVELOPER = escape_markdown_v2("""
👨‍💻 **About the Developer**  
This bot is professionally developed by [@hyperosislove](https://t.me/hyperosislove).

For inquiries, support, or suggestions, feel free to contact the developer.  
Thank you for trusting our services! 🌟
""")

HELP_MESSAGE = escape_markdown_v2("""
📖 **How to Use LinkGuard Bot**  
1. **Add the bot to your group.**
2. **Give the bot admin rights**, including:
   - Message deletion permissions.
   - Ability to restrict users.
3. Once added, the bot will:
   - Automatically delete links or mentions.
   - Warn users about rules.

**Pro Tip**: Use this bot to protect your group from spam, scams, and unsolicited advertisements.
""")

# Function to check for links or mentions
def contains_prohibited_content(message_text):
    return bool(re.search(r"http[s]?://|www\.|^@[\w\d]+", message_text))

# /start command handler
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("➕ Add to Group", url="https://t.me/your_bot_username?startgroup=true")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
        [InlineKeyboardButton("👨‍💻 About Developer", callback_data="about_developer")],
    ]
    await message.reply_text(
        START_MESSAGE,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="MarkdownV2",
    )

# Callback query handler for Help
@app.on_callback_query(filters.regex("help"))
async def help(client, callback_query):
    await callback_query.message.edit_text(
        HELP_MESSAGE,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")],
        ]),
        parse_mode="MarkdownV2",
    )

# Callback query handler for About Developer
@app.on_callback_query(filters.regex("about_developer"))
async def about_developer(client, callback_query):
    await callback_query.message.edit_text(
        ABOUT_DEVELOPER,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")],
        ]),
        parse_mode="MarkdownV2",
    )

# Callback query handler to return to Main Menu
@app.on_callback_query(filters.regex("main_menu"))
async def main_menu(client, callback_query):
    buttons = [
        [InlineKeyboardButton("➕ Add to Group", url="https://t.me/your_bot_username?startgroup=true")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
        [InlineKeyboardButton("👨‍💻 About Developer", callback_data="about_developer")],
    ]
    await callback_query.message.edit_text(
        START_MESSAGE,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="MarkdownV2",
    )

# Group message handler
@app.on_message(filters.group & ~filters.service)
async def check_message(client, message):
    if message.text and contains_prohibited_content(message.text):
        await message.delete()  # Delete prohibited message
        user = message.from_user
        warning_message = await message.reply_text(
            escape_markdown_v2(
                f"🚫 **Warning!**\n\n"
                f"Dear {f'@{user.username}' if user.username else user.first_name}, posting links or mentions is not allowed here. "
                f"Please adhere to the group rules to avoid further actions."
            ),
            parse_mode="MarkdownV2",
        )
        await asyncio.sleep(10)  # Wait 10 seconds
        await warning_message.delete()  # Delete warning message

# Run the bot
if __name__ == "__main__":
    app.run()
