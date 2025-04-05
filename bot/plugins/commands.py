import os
import sys
import asyncio
import time
import shutil
import random
from psutil import cpu_percent, virtual_memory, disk_usage
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.db.broadcast_sql import add_user
from bot.db.settings_sql import get_search_settings, change_search_settings
from bot import LOGGER, ADMINS
from bot.utils.util_support import humanbytes, get_db_size
from bot.plugins.serve import get_files


@Client.on_message(filters.command(["start"]))
async def start(bot, update):
    if len(update.command) == 1:
        user_id = update.from_user.id
        name = update.from_user.first_name if update.from_user.first_name else " "
        user_name = (
            "@" + update.from_user.username if update.from_user.username else None
        )
        await add_user(user_id, user_name)

        await update.reply_photo(
            photo=random.choice(PICS),
            caption=f"""<b> Hᴇʏ Tʜᴇʀᴇ {update.from_user.mention} 👋,

I'ᴍ ᴀɴ Aᴡᴇsᴏᴍᴇ Mᴇᴅɪᴀ Sᴇᴀʀᴄʜ Rᴏʙᴏᴛ Sᴘᴇᴄɪᴀʟʟʏ Mᴀᴅᴇ Fᴏʀ Sᴇᴀʀᴄʜɪɴɢ Mᴀʟᴀʏᴀʟᴀᴍ Dᴜʙʙᴇᴅ Mᴏᴠɪᴇs...😉
Jᴜsᴛ Sᴇɴᴅ Tʜᴇ Nᴀᴍᴇ Oғ Tʜᴇ Mᴏᴠɪᴇ Yᴏᴜ Wᴀɴᴛ Aɴᴅ Sᴇᴇ Mʏ Pᴇᴡᴇʀ...✨

✪ Mᴀɪɴᴛᴀɪɴᴇᴅ Bʏ : <a href='https://t.me/MR_TONY_99'>Tᴏɴʏ Sᴛᴀʀᴋ</a> </b>""",
            chat_id=update.chat.id,
            reply_to_message_id=update.reply_to_message_id,
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 📈", url="t.me/MalluCartoonzz"),
                ],[
                InlineKeyboardButton("Hᴇʟᴘ 🛠", callback_data="help_cb"),
                InlineKeyboardButton("Aʙᴏᴜᴛ 😇", callback_data="about_cb"),
                ],[
                InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ 👨🏼‍💻 ", url="t.me/MR_TONY_99")
                ]]
                )
            )
        search_settings = await get_search_settings(user_id)
        if not search_settings:
            await change_search_settings(user_id, link_mode=True)
    elif len(update.command) == 2:
        await get_files(bot, update)


@Client.on_message(filters.command(["help"]))
async def help_m(bot, update):
    await update.reply_photo(
        photo=random.choice(PICS),
        caption=f"""<b> Hᴇʏ {update.from_user.mention} 👋,

Hᴇʀᴇ Yᴏᴜ Cᴀɴ Sᴇᴇ Tʜᴇ Bᴏᴛ's Cᴏᴍᴍᴀɴᴅs...✨

Bᴀsɪᴄ Cᴏᴍᴍᴀɴᴅs :
○ /start - Tᴏ Cʜᴇᴄᴋ I Aᴍ Aʟɪᴠᴇ
○ /help  - Tᴏ Sʜᴏᴡ Tʜɪs Mᴇssᴀɢᴇ
○ /about - Bᴇʜɪɴᴅ Tʜᴇ Bᴏᴛ

Aᴅᴍɪɴ Cᴏᴍᴍᴀɴᴅs :
○ /logs - Gᴇᴛ ʟᴏɢs ᴀs ᴀ ғɪʟᴇ
○ /server - Gᴇᴛ sᴇʀᴠᴇʀ sᴛᴀᴛs
○ /restart - Rᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
○ /stats - Gᴇᴛ ʙᴏᴛ ᴜsᴇʀ sᴛᴀᴛs
○ /broadcast - Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇɴᴅ ᴛʜᴀᴛ ᴛᴏ ᴀʟʟ ʙᴏᴛ ᴜsᴇʀs
○ /index - Sᴛᴀʀᴛ ɪɴᴅᴇxɪɴɢ ᴀ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ
○ /delete - Rᴇᴘʟʏ ᴛᴏ ᴀ ғɪʟᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ ɪᴛ ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ
○ /autodelete - Sᴇᴛ ғɪʟᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ ɪɴ sᴇᴄᴏɴᴅs
○ /repairmode - Eɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ʀᴇᴘᴀɪʀ ᴍᴏᴅᴇ
○ /customcaption - Sᴇᴛ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ғᴏʀ ғɪʟᴇs
○ /adminsettings - Gᴇᴛ ᴄᴜʀʀᴇɴᴛ ᴀᴅᴍɪɴ sᴇᴛᴛɪɴɢs
○ /ban - Bᴀɴ ᴀ ᴜsᴇʀ ғʀᴏᴍ ʙᴏᴛ
○ /unban - Uɴʙᴀɴ ᴀ ᴜsᴇʀ ғʀᴏᴍ ʙᴏᴛ
○ /addfilter - Aᴅᴅ ᴀ ᴛᴇxᴛ ғɪʟᴛᴇʀ
○ /delfilter - Dᴇʟᴇᴛᴇ ᴀ ᴛᴇxᴛ ғɪʟᴛᴇʀ
○ /listfilters - Lɪsᴛ ᴀʟʟ ғɪʟᴛᴇʀs ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴅᴅᴇᴅ ɪɴ ᴛʜᴇ ʙᴏᴛ
○ /forcesub - Sᴇᴛ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴄʜᴀɴɴᴇʟ
○ /checklink - Cʜᴇᴄᴋ ɪɴᴠɪᴛᴇ ʟɪɴᴋ ғᴏʀ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴄʜᴀɴɴᴇʟ
○ /total - Gᴇᴛ ᴄᴏᴜɴᴛ ᴏғ ᴛᴏᴛᴀʟ ғɪʟᴇs ɪɴ DB </b>""",
        chat_id=update.chat.id,
        reply_to_message_id=update.reply_to_message_id,
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("🔙 Bᴀᴄᴋ", callback_data="back_m"),
            InlineKeyboardButton("Aʙᴏᴜᴛ 😇", callback_data="about_cb")
            ]]
            )
        )
    
@Client.on_message(filters.command(["about"]))
async def about_m(bot, update):
    await update.reply_photo(
        photo=random.choice(PICS),
        caption=f"""<b> Hᴇʏ {update.from_user.mention} 👋,

◈ ᴍy ɴᴀᴍᴇ : Rᴇɴᴀᴍᴇʀ 4GB V3
◈ Dᴇᴠᴇʟᴏᴩᴇʀ : <a href='https://t.me/MR_TONY_99'>Tᴏɴʏ Sᴛᴀʀᴋ</a>
◈ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ: <a href='https://t.me/MalluCartoonzz'>Mᴀʟʟᴜ Cᴀʀᴛᴏᴏɴᴢᴢ</a>
◈ Lɪʙʀᴀʀy : <a href='https://github.com/pyrogram'>Pyʀᴏɢʀᴀᴍ</a>
◈ Lᴀɴɢᴜᴀɢᴇ: <a href='www.python.org'>Pʏᴛʜᴏɴ 𝟹</a>
◈ Dᴀᴛᴀ Bᴀꜱᴇ: <a href='https://cloud.mongodb.com/'>Mᴏɴɢᴏ DB</a> </b>""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ 👨🏼‍💻 ", url="t.me/MR_TONY_99")
            ]]
            )
        )
            
@Client.on_callback_query(filters.regex(r"^back_m$"))
async def back(bot, query):
    user_id = query.from_user.id
    name = query.from_user.first_name if query.from_user.first_name else " "
    await query.message.edit_text(
        text=f"""<b> Hᴇʏ Tʜᴇʀᴇ {update.from_user.mention} 👋,

I'ᴍ ᴀɴ Aᴡᴇsᴏᴍᴇ Mᴇᴅɪᴀ Sᴇᴀʀᴄʜ Rᴏʙᴏᴛ Sᴘᴇᴄɪᴀʟʟʏ Mᴀᴅᴇ Fᴏʀ Sᴇᴀʀᴄʜɪɴɢ Mᴀʟᴀʏᴀʟᴀᴍ Dᴜʙʙᴇᴅ Mᴏᴠɪᴇs...😉
Jᴜsᴛ Sᴇɴᴅ Tʜᴇ Nᴀᴍᴇ Oғ Tʜᴇ Mᴏᴠɪᴇ Yᴏᴜ Wᴀɴᴛ Aɴᴅ Sᴇᴇ Mʏ Pᴇᴡᴇʀ...✨

✪ Mᴀɪɴᴛᴀɪɴᴇᴅ Bʏ : <a href='https://t.me/MR_TONY_99'>Tᴏɴʏ Sᴛᴀʀᴋ</a> </b>""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ 📈", url="t.me/MalluCartoonzz"),
            ],[
            InlineKeyboardButton("Hᴇʟᴘ 🛠", callback_data="help_cb"),
            InlineKeyboardButton("Aʙᴏᴜᴛ 😇", callback_data="about_cb"),
            ],[
            InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ 👨🏼‍💻 ", url="t.me/MR_TONY_99")
            ]]
            )
        )
@Client.on_callback_query(filters.regex(r"^help_cb$"))
async def help_cb(bot, query):
    await query.message.edit_text(
        text=f"""<b> Hᴇʏ {update.from_user.mention} 👋,

Hᴇʀᴇ Yᴏᴜ Cᴀɴ Sᴇᴇ Tʜᴇ Bᴏᴛ's Cᴏᴍᴍᴀɴᴅs...✨

Bᴀsɪᴄ Cᴏᴍᴍᴀɴᴅs :
○ /start - Tᴏ Cʜᴇᴄᴋ I Aᴍ Aʟɪᴠᴇ
○ /help  - Tᴏ Sʜᴏᴡ Tʜɪs Mᴇssᴀɢᴇ
○ /about - Bᴇʜɪɴᴅ Tʜᴇ Bᴏᴛ

Aᴅᴍɪɴ Cᴏᴍᴍᴀɴᴅs :
○ /logs - Gᴇᴛ ʟᴏɢs ᴀs ᴀ ғɪʟᴇ
○ /server - Gᴇᴛ sᴇʀᴠᴇʀ sᴛᴀᴛs
○ /restart - Rᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
○ /stats - Gᴇᴛ ʙᴏᴛ ᴜsᴇʀ sᴛᴀᴛs
○ /broadcast - Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇɴᴅ ᴛʜᴀᴛ ᴛᴏ ᴀʟʟ ʙᴏᴛ ᴜsᴇʀs
○ /index - Sᴛᴀʀᴛ ɪɴᴅᴇxɪɴɢ ᴀ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ
○ /delete - Rᴇᴘʟʏ ᴛᴏ ᴀ ғɪʟᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ ɪᴛ ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ
○ /autodelete - Sᴇᴛ ғɪʟᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ ɪɴ sᴇᴄᴏɴᴅs
○ /repairmode - Eɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ʀᴇᴘᴀɪʀ ᴍᴏᴅᴇ
○ /customcaption - Sᴇᴛ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ғᴏʀ ғɪʟᴇs
○ /adminsettings - Gᴇᴛ ᴄᴜʀʀᴇɴᴛ ᴀᴅᴍɪɴ sᴇᴛᴛɪɴɢs
○ /ban - Bᴀɴ ᴀ ᴜsᴇʀ ғʀᴏᴍ ʙᴏᴛ
○ /unban - Uɴʙᴀɴ ᴀ ᴜsᴇʀ ғʀᴏᴍ ʙᴏᴛ
○ /addfilter - Aᴅᴅ ᴀ ᴛᴇxᴛ ғɪʟᴛᴇʀ
○ /delfilter - Dᴇʟᴇᴛᴇ ᴀ ᴛᴇxᴛ ғɪʟᴛᴇʀ
○ /listfilters - Lɪsᴛ ᴀʟʟ ғɪʟᴛᴇʀs ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴅᴅᴇᴅ ɪɴ ᴛʜᴇ ʙᴏᴛ
○ /forcesub - Sᴇᴛ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴄʜᴀɴɴᴇʟ
○ /checklink - Cʜᴇᴄᴋ ɪɴᴠɪᴛᴇ ʟɪɴᴋ ғᴏʀ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴄʜᴀɴɴᴇʟ
○ /total - Gᴇᴛ ᴄᴏᴜɴᴛ ᴏғ ᴛᴏᴛᴀʟ ғɪʟᴇs ɪɴ DB </b>""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("🔙 Bᴀᴄᴋ", callback_data="back_m"),
            InlineKeyboardButton("Aʙᴏᴜᴛ 😇", callback_data="about_cb")
            ]]
            )
        )

@Client.on_callback_query(filters.regex(r"^about_cb$"))
async def about_cb(bot, query):
    await query.message.edit_text(
        text=f"""<b> Hᴇʏ {update.from_user.mention} 👋,

◈ ᴍy ɴᴀᴍᴇ : Rᴇɴᴀᴍᴇʀ 4GB V3
◈ Dᴇᴠᴇʟᴏᴩᴇʀ : <a href='https://t.me/MR_TONY_99'>Tᴏɴʏ Sᴛᴀʀᴋ</a>
◈ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ: <a href='https://t.me/MalluCartoonzz'>Mᴀʟʟᴜ Cᴀʀᴛᴏᴏɴᴢᴢ</a>
◈ Lɪʙʀᴀʀy : <a href='https://github.com/pyrogram'>Pyʀᴏɢʀᴀᴍ</a>
◈ Lᴀɴɢᴜᴀɢᴇ: <a href='www.python.org'>Pʏᴛʜᴏɴ 𝟹</a>
◈ Dᴀᴛᴀ Bᴀꜱᴇ: <a href='https://cloud.mongodb.com/'>Mᴏɴɢᴏ DB</a> </b>""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ 👨🏼‍💻 ", url="t.me/MR_TONY_99")
            ]]
            )
        )


        
@Client.on_message(filters.command(["restart"]) & filters.user(ADMINS))
async def restart(bot, update):
    LOGGER.warning("Rᴇsᴛᴀʀᴛɪɴɢ ʙᴏᴛ ᴜsɪɴɢ /restart ᴄᴏᴍᴍᴀɴᴅ")
    msg = await update.reply_text(text="__Rᴇsᴛᴀʀᴛɪɴɢ.....__")
    await asyncio.sleep(5)
    await msg.edit("__Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ...__")
    os.execv(sys.executable, ["python3", "-m", "bot"] + sys.argv)


@Client.on_message(filters.command(["logs"]) & filters.user(ADMINS))
async def log_file(bot, update):
    logs_msg = await update.reply("__Sᴇɴᴅɪɴɢ ʟᴏɢs, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...__")
    try:
        await update.reply_document("logs@MalluSearchRobot.txt")
    except Exception as e:
        await update.reply(str(e))
    await logs_msg.delete()


@Client.on_message(filters.command(["server"]) & filters.user(ADMINS))
async def server_stats(bot, update):
    sts = await update.reply_text("__Calculating, please wait...__")
    total, used, free = shutil.disk_usage(".")
    ram = virtual_memory()
    start_t = time.time()
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000

    ping = f"{time_taken_s:.3f} ms"
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    t_ram = humanbytes(ram.total)
    u_ram = humanbytes(ram.used)
    f_ram = humanbytes(ram.available)
    cpu_usage = cpu_percent()
    ram_usage = virtual_memory().percent
    used_disk = disk_usage("/").percent
    db_size = get_db_size()

    stats_msg = f"--**BOT STATS**--\n`Ping: {ping}`\n\n--**SERVER DETAILS**--\n`Disk Total/Used/Free: {total}/{used}/{free}\nDisk usage: {used_disk}%\nRAM Total/Used/Free: {t_ram}/{u_ram}/{f_ram}\nRAM Usage: {ram_usage}%\nCPU Usage: {cpu_usage}%`\n\n--**DATABASE DETAILS**--\n`Size: {db_size} MB`"
    try:
        await sts.edit(stats_msg)
    except Exception as e:
        await update.reply_text(str(e))
