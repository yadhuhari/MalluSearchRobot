import shlex
from pyrogram import Client, filters
from mfinder.db.settings_sql import (
    get_admin_settings,
    set_repair_mode,
    set_auto_delete,
    set_custom_caption,
    set_force_sub,
    set_channel_link,
    get_link,
    set_username,
)
from mfinder.db.ban_sql import is_banned, ban_user, unban_user
from mfinder.db.filters_sql import add_filter, rem_filter, list_filters
from mfinder.db.files_sql import count_files
from mfinder import ADMINS, DB_CHANNELS


@Client.on_message(filters.command(["autodelete"]) & filters.user(ADMINS))
async def auto_delete_(bot, update):
    data = update.text.split()
    if len(data) == 2:
        dur = data[-1]
        if dur.lower() == "off":
            dur = 0

        await set_auto_delete(int(dur))

        if dur:
            await update.reply_text(f"Fɪʟᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ sᴇᴛ ᴛᴏ {dur} sᴇᴄᴏɴᴅs")
        else:
            await update.reply_text("Fɪʟᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴅɪsᴀʙʟᴇᴅ")

    else:
        await update.reply_text("Pʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴘʀᴏᴘᴇʀ ғᴏʀᴍᴀᴛ `/autodelete seconds`")


@Client.on_message(filters.command(["repairmode"]) & filters.user(ADMINS))
async def repair_mode_(bot, update):
    data = update.text.split()
    if len(data) == 2:
        toggle = data[-1]
        if toggle.lower() == "off":
            mode = False
        elif toggle.lower() == "on":
            mode = True
        else:
            await update.reply_text(
                "Pʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴘʀᴏᴘᴇʀ ғᴏʀᴍᴀᴛ `/repairmode <on/off>`"
            )
            return

        await set_repair_mode(mode)
        await update.reply_text(f"Rᴇᴘᴀɪʀ ᴍᴏᴅᴇ sᴇᴛ ᴛᴏ `{toggle.upper()}`")

    else:
        await update.reply_text("Pʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴘʀᴏᴘᴇʀ ғᴏʀᴍᴀᴛ `/repairmode on/off`")
        return


@Client.on_message(filters.command(["customcaption"]) & filters.user(ADMINS))
async def custom_caption_(bot, update):
    data = update.text.split()
    caption = " ".join(data[1:])
    if len(data) >= 2:
        if caption.lower() == "off":
            caption = None

        await set_custom_caption(caption)

        if caption:
            await update.reply_text(f"Cᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ sᴇᴛ ᴛᴏ `{caption}`")
        else:
            await update.reply_text("Cᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ᴅɪsᴀʙʟᴇᴅ")

    else:
        await update.reply_text(
            "Pʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴘʀᴏᴘᴇʀ ғᴏʀᴍᴀᴛ `/customcaption caption/off`"
        )
        return


@Client.on_message(filters.command(["adminsettings"]))
async def admin_settings_(bot, update):
    user_id = update.from_user.id
    admin_settings = await get_admin_settings()
    auto_delete = admin_settings.auto_delete
    custom_caption = admin_settings.custom_caption
    fsub_channel = admin_settings.fsub_channel
    caption_uname = admin_settings.caption_uname
    invite_link = admin_settings.channel_link
    repair_mode = admin_settings.repair_mode

    admins = ""
    dbchannel = ""
    for admin in ADMINS:
        admins += "\n" + "`" + str(admin) + "`"
    for channel in DB_CHANNELS:
        dbchannel += "\n" + "`" + str(channel) + "`"

    if auto_delete:
        auto_delete = f"{auto_delete} seconds"
    else:
        auto_delete = "Dɪsᴀʙʟᴇᴅ"

    if not custom_caption:
        custom_caption = "Dɪsᴀʙʟᴇᴅ"

    if not fsub_channel:
        fsub_channel = "Dɪsᴀʙʟᴇᴅ"

    if not caption_uname:
        caption_uname = "Dɪsᴀʙʟᴇᴅ"

    if not invite_link:
        invite_link = "Dɪsᴀʙʟᴇᴅ"

    if repair_mode:
        repair_mode = "Eɴᴀʙʟᴇᴅ"
    else:
        repair_mode = "Dɪsᴀʙʟᴇᴅ"

    await bot.send_message(
        chat_id=user_id,
        text=f"**Bᴇʟᴏᴡ ᴀʀᴇ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs.**\n\n**Rᴇᴘᴀɪʀ ᴍᴏᴅᴇ:** `{repair_mode}`\n**ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ:** `{auto_delete}`\n**Cᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ:** `{custom_caption}`\n**Fᴏʀᴄᴇ Sᴜʙ:** `{fsub_channel}`\n**Cᴀᴘᴛɪᴏɴ Usᴇʀɴᴀᴍᴇ:** `{caption_uname}`\n**Cʜᴀɴɴᴇʟ Lɪɴᴋ:** `{invite_link}`\n**Aᴅᴍɪɴs:** {admins} \n**DB Cʜᴀɴɴᴇʟs:** {dbchannel}",
    )


@Client.on_message(filters.command(["ban"]) & filters.user(ADMINS))
async def banuser(bot, update):
    data = update.text.split()
    if len(data) == 2:
        user_id = data[-1]
        banned = await is_banned(int(user_id))
        if not banned:
            await ban_user(int(user_id))
            await update.reply_text(f"Usᴇʀ {user_id} ʙᴀɴɴᴇᴅ")
        else:
            await update.reply_text(f"Usᴇʀ {user_id} ɪs ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ")

    else:
        await update.reply_text("Pʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴘʀᴏᴘᴇʀ ғᴏʀᴍᴀᴛ `/ban user_id`")


@Client.on_message(filters.command(["unban"]) & filters.user(ADMINS))
async def unbanuser(bot, update):
    data = update.text.split()
    if len(data) == 2:
        user_id = data[-1]
        banned = await is_banned(int(user_id))
        if banned:
            await unban_user(int(user_id))
            await update.reply_text(f"Usᴇʀ {user_id} ᴜɴʙᴀɴɴᴇᴅ")
        else:
            await update.reply_text(f"Usᴇʀ {user_id} ɪs ɴᴏᴛ ɪɴ ʙᴀɴ ʟɪsᴛ")
    else:
        await update.reply_text("Pʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴘʀᴏᴘᴇʀ ғᴏʀᴍᴀᴛ `/unban user_id`")


@Client.on_message(filters.command(["addfilter"]) & filters.user(ADMINS))
async def addfilter(bot, update):
    data = shlex.split(update.text)
    if len(data) >= 3:
        fltr = data[1].strip('"').lower()
        message = " ".join(data[2:])
        add = await add_filter(fltr, message)
        if add:
            await update.reply_text(f"Fɪʟᴛᴇʀ `{fltr}` ᴀᴅᴅᴇᴅ")
        else:
            await update.reply_text(f"Fɪʟᴛᴇʀ `{fltr}` ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛs")
    else:
        await update.reply_text(
            "Pʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴘʀᴏᴘᴇʀ ғᴏʀᴍᴀᴛ `/addfilter filter message`"
        )


@Client.on_message(filters.command(["delfilter"]) & filters.user(ADMINS))
async def delfilter(bot, update):
    data = update.text.split()
    if len(data) >= 2:
        fltr = " ".join(data[1:])
        rem = await rem_filter(fltr)
        if rem:
            await update.reply_text(f"Fɪʟᴛᴇʀ `{fltr}` ʀᴇᴍᴏᴠᴇᴅ")
        else:
            await update.reply_text(f"Fɪʟᴛᴇʀ `{fltr}` ɴᴏᴛ ғᴏᴜɴᴅ")
    else:
        await update.reply_text("Pʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴘʀᴏᴘᴇʀ ғᴏʀᴍᴀᴛ `/delfilter filter`")


@Client.on_message(filters.command(["listfilters"]) & filters.user(ADMINS))
async def list_filter(bot, update):
    fltr = await list_filters()
    fltr_msg = ""
    if fltr:
        for fltrs in fltr:
            fltr_msg += "\n" + "`" + fltrs + "`"
        await update.reply_text(f"**Aᴠᴀɪʟᴀʙʟᴇ Fɪʟᴛᴇʀs:** {fltr_msg}")
    else:
        await update.reply_text("Nᴏ ғɪʟᴛᴇʀs ғᴏᴜɴᴅ")


@Client.on_message(filters.command(["forcesub"]) & filters.user(ADMINS))
async def force_sub(bot, update):
    data = update.text.split()
    if len(data) == 2:
        channel = data[-1]
        if channel.lower() == "off":
            channel = 0

        if channel:
            try:
                link = await bot.create_chat_invite_link(channel)
                await set_channel_link(link.invite_link)
            except Exception as e:
                await update.reply_text(
                    f" Eʀʀᴏʀ ᴡʜɪʟᴇ ᴄʀᴇᴀᴛɪɴɢ ᴄʜᴀɴɴᴇʟ ɪɴᴠɪᴛᴇ ʟɪɴᴋ: {str(e)}"
                )
                return

            await set_force_sub(int(channel))
            await update.reply_text(f"Fᴏʀᴄᴇ Sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴄʜᴀɴɴᴇʟ sᴇᴛ ᴛᴏ `{channel}`")
        else:
            await set_channel_link(None)
            await update.reply_text("Fᴏʀᴄᴇ Sᴜʙsᴄʀɪᴘᴛɪᴏɴ Dɪsᴀʙʟᴇᴅ")

    else:
        await update.reply_text(
            "Pʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴘʀᴏᴘᴇʀ ғᴏʀᴍᴀᴛ `/forcesub channel_id/off`"
        )


@Client.on_message(filters.command(["checklink"]) & filters.user(ADMINS))
async def testlink(bot, update):
    link = await get_link()
    if link:
        await update.reply_text(f"Iɴᴠɪᴛᴇ ʟɪɴᴋ ғᴏʀ ғᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴄʜᴀɴɴᴇʟ: {link}")
    else:
        await update.reply_text(
            "Fᴏʀᴄᴇ Sᴜʙsᴄʀɪᴘᴛɪᴏɴ ɪs ᴅɪsᴀʙʟᴇᴅ, ᴘʟᴇᴀsᴇ ᴇɴᴀʙʟᴇ ɪᴛ ғɪʀsᴛ"
        )


@Client.on_message(filters.command(["setusername"]) & filters.user(ADMINS))
async def caption_username(bot, update):
    data = update.text.split()
    if len(data) == 2:
        username = data[-1]
        if username.lower() == "off":
            username = 0
        elif username.startswith("@"):
            username = username
        else:
            await update.reply_text("Tʜɪs ɪs ɴᴏᴛ ᴀ ᴜsᴇʀɴᴀᴍᴇ, ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ.")
            return

        await set_username(username)

        if username:
            await update.reply_text(f"Fɪʟᴇ ᴄᴀᴘᴛɪᴏɴ ᴜsᴇʀɴᴀᴍᴇ sᴇᴛ ᴛᴏ `{username}`")
        else:
            await update.reply_text("Fɪʟᴇ ᴄᴀᴘᴛɪᴏɴ ᴜsᴇʀɴᴀᴍᴇ ᴅɪsᴀʙʟᴇᴅ")

    else:
        await update.reply_text(
            "Pʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴘʀᴏᴘᴇʀ ғᴏʀᴍᴀᴛ `/setusername username/off`"
        )


@Client.on_message(filters.command(["total"]) & filters.user(ADMINS))
async def count_f(bot, update):
    count = await count_files()
    await update.reply_text(f"**Tᴏᴛᴀʟ ɴᴏ. ᴏғ ғɪʟᴇs ɪɴ DB:** `{count}`")
