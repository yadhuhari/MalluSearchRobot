import asyncio
import time
import datetime
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from bot import LOGGER
from bot.db.db_support import users_info
from bot.db.broadcast_sql import query_msg
from bot import ADMINS, OWNER_ID


@Client.on_message(
    filters.private & filters.command("stats") & filters.user(ADMINS)
)
async def get_subscribers_count(bot: Client, message: Message):
    wait_msg = "__Cᴀʟᴄᴜʟᴀᴛɪɴɢ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...__"
    msg = await message.reply_text(wait_msg)
    active, blocked = await users_info(bot)
    stats_msg = f"**Sᴛᴀᴛs**\nSᴜʙsᴄʀɪʙᴇʀs: `{ᴀᴄᴛɪᴠᴇ}`\nBʟᴏᴄᴋᴇᴅ / Dᴇʟᴇᴛᴇᴅ: `{blocked}`"
    await msg.edit(stats_msg)


@Client.on_message(
    filters.private & filters.command("broadcast") & filters.user(OWNER_ID)
)
async def send_text(bot, message: Message):
    user_id = message.from_user.id
    if "broadcast" in message.text and message.reply_to_message is not None:
        start_time = time.time()
        await message.reply_text("Sᴛᴀʀᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ, ᴄᴏɴᴛᴇɴᴛ ʙᴇʟᴏᴡ...")
        await bot.copy_message(
            chat_id=user_id,
            from_chat_id=message.chat.id,
            message_id=message.reply_to_message_id,
            # caption=message.reply_to_message.caption,
            reply_markup=message.reply_to_message.reply_markup,
        )
        query = await query_msg()
        success = 0
        failed = 0
        for row in query:
            chat_id = int(row[0])
            br_msg = bool()
            try:
                br_msg = await bot.copy_message(
                    chat_id=chat_id,
                    from_chat_id=message.chat.id,
                    message_id=message.reply_to_message_id,
                    # caption=message.reply_to_message.caption,
                    reply_markup=message.reply_to_message.reply_markup,
                )
                LOGGER.info("Broadcast sent to %s", chat_id)
            except FloodWait as e:
                LOGGER.warning("Fʟᴏᴏᴅᴡᴀɪᴛ ᴡʜɪʟᴇ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ, sʟᴇᴇᴘɪɴɢ ғᴏʀ %s", e.value)
                await asyncio.sleep(e.value)
            except Exception:
                pass

            if bool(br_msg):
                success += 1
            else:
                failed += 1
        time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
        await message.reply_text(
            f"**Broadcast Completed**\nSent to: `{success}`\nBlocked / Deleted: `{failed}`\nCompleted in `{time_taken}` HH:MM:SS"
        )

    else:
        reply_error = (
            "`Usᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ sᴘᴀᴄᴇs.`"
        )
        msg = await message.reply_text(reply_error, message.id)
        await asyncio.sleep(8)
        await msg.delete()
