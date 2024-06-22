import os
import asyncio
from pymongo import MongoClient
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from shivu import Application, ContextTypes, CommandHandler, CallbackQueryHandler

from shivu import collection, user_collection, application

# ==== 1. Database Setup ====
MONGODB_URI = os.getenv("MONGODB_URI") 
client = MongoClient(MONGODB_URI)
db = client["your_database_name"] 
user_collection = db["users"] 

# ==== 2. Telegram Bot Functions ====

async def fav_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /fav command, asking for confirmation."""
    user_id = update.effective_user.id
    character_id = context.args[0] if context.args else None

    if not character_id:
        await update.message.reply_text("Please provide a character ID: /fav [character_id]")
        return

    # Check if the character already exists in the database (optional)
    # character = await get_character_from_db(character_id)  
    # if not character:
    #     await update.message.reply_text(f"Character with ID {character_id} not found.")
    #     return

    keyboard = [
        [
            InlineKeyboardButton("✅ Yes", callback_data=f"fav_yes_{character_id}"),
            InlineKeyboardButton("❌ No", callback_data=f"fav_no_{character_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Do you want to add character {character_id} to your favorites?", 
        reply_markup=reply_markup
    )

async def handle_fav_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the Yes/No inline button presses."""
    query = update.callback_query
    await query.answer()

    choice, _, character_id = query.data.split("_")
    user_id = update.effective_user.id

    if choice == "favyes":
        user = await user_collection.find_one({"user_id": user_id})
        if not user:
            user = {"user_id": user_id, "favorites": []}
        
        if character_id in user["favorites"]:
            await query.edit_message_text(f"Character {character_id} is already in your favorites!")
        else: 
            user["favorites"].append(character_id)
            await user_collection.update_one({"user_id": user_id}, {"$set": user}, upsert=True)
            await query.edit_message_text(f"Added character {character_id} to your favorites!")

    elif choice == "favno":
        await query.edit_message_text(f"Okay, character {character_id} was not added.")


   

    application.add_handler(CommandHandler("fav", fav_command))
    application.add_handler(CallbackQueryHandler(handle_fav_choice))

    application.run_polling()
