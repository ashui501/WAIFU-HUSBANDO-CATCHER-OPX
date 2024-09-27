import random
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from shivu import user_collection, shivuu as app, LEAVELOGS, JOINLOGS

async def lul_message(chat_id: int, message: str):
    await app.send_message(chat_id=chat_id, text=message)

@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    if (await client.get_me()).id in [user.id for user in message.new_chat_members]:
        added_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        chat_title = message.chat.title
        chat_id = message.chat.id
        member_count = message.chat.members_count

        if message.chat.username:
            chat_username = f"@{message.chat.username}"
            chat_link = chat_username
        else:
            chat_link = f"https://t.me/c/{chat_id}"

        lemda_text = (
            f"<b>🏠 User Added To Group</b>\n\n"
            f"<b>🆔 Group ID:</b> {chat_id}\n"
            f"<b>📛 Group Name:</b> {chat_title}\n"
            f"<b>👤 Added By:</b> {added_by}\n"
            f"<b>👥 Total Members:</b> {member_count}\n"
            f"<b>🔗 Group Link:</b> {chat_link}"
        )
        await lul_message(JOINLOGS, lemda_text)

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(client: Client, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        removed_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        chat_title = message.chat.title
        chat_id = message.chat.id
        member_count = message.chat.members_count

        if message.chat.username:
            chat_username = f"@{message.chat.username}"
            chat_link = chat_username
        else:
            chat_link = f"https://t.me/c/{chat_id}"

        left_text = (
            f"<b>🚪 User Left Group</b>\n\n"
            f"<b>🆔 Group ID:</b> {chat_id}\n"
            f"<b>📛 Group Name:</b> {chat_title}\n"
            f"<b>👤 Removed By:</b> {removed_by}\n"
            f"<b>👥 Total Members:</b> {member_count}\n"
            f"<b>🔗 Group Link:</b> {chat_link}"
        )
        await lul_message(LEAVELOGS, left_text)