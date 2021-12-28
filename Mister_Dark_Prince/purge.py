import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from config import HNDLR


@Client.on_message(filters.command("del", prefixes=f"{HNDLR}") & filters.me)
async def del_msg(client: Client, message: Message):
    if message.reply_to_message:
        message_id = message.reply_to_message.message_id
        await message.delete()
        await client.delete_messages(message.chat.id, message_id)


@Client.on_message(filters.command("purge", prefixes=f"{HNDLR}") & filters.me)
async def purge(client: Client, message: Message):
    messages_to_purge = []
    if message.reply_to_message:
        async for msg in client.iter_history(
                chat_id=message.chat.id,
                offset_id=message.reply_to_message.message_id,
                reverse=True,
        ):
            messages_to_purge.append(msg.message_id)
    not_deleted_messages = []
    for msgs in [
        messages_to_purge[i: i + 100] for i in range(0, len(messages_to_purge), 100)
    ]:
        res = await client.delete_messages(message.chat.id, msgs)
        await asyncio.sleep(1)
