import logging
import os

from pyrogram import Client, filters, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.raw import functions
from pyrogram.types import Message

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

api_hash = os.getenv('API_HASH')
api_id = os.getenv('API_ID')

if not api_hash or not api_id:
    logging.fatal('Missing API_HASH or API_ID')

app = Client(api_hash=api_hash, api_id=int(api_id), name='userbot')


@app.on_message(filters=filters.group & filters.command(['superban', 'megaban']))
async def ban_via_reaction(client: Client, message: Message):
    logging.info(f'Received superban from {message.from_user.id}')

    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        logging.warning('User is not owner/admin')
        return

    await message.delete()

    r = await client.invoke(functions.messages.GetMessageReactionsList(
        peer=await app.resolve_peer(message.chat.id),
        id=message.reply_to_message.id,
        limit=10,
    ))

    if message.command == 'superban':
        if len(r.reactions) > 1:
            await message.reply_text('❌ È presente più di una reazione')
            return
        user_id = r.reactions[0].peer_id.user_id
        await ban(client, message, user_id)
    elif message.command == 'megaban':
        for r in r.reactions:
            user_id = r.peer_id.user_id
            await ban(client, message, user_id)


async def ban(client: Client, message: Message, user_id: int):
    logging.info(f'Banning {user_id}')

    try:
        await client.ban_chat_member(message.chat.id, user_id)
    except:
        logging.exception('Could not ban user')
        await message.reply_text(f'❌ Non sono riuscito a bannare l\'utente `{user_id}`',
                                 parse_mode=enums.ParseMode.MARKDOWN)
        return

    await message.reply_text(f'✅ Utente `{user_id}` bannato', parse_mode=enums.ParseMode.MARKDOWN)


app.run()
