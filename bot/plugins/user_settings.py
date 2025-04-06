from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.db.settings_sql import get_search_settings, change_search_settings

SET_MSG = """
**Below are your current settings:**
`Info`
**Precise Mode:** 
- __If Enabled, bot will match the word & return results with only the exact match__
- __If Disabled, bot will match the word & return all the results containing the word__    
**Result Mode:**
- __If HyperLink, bot will return results in hyperlink format__
- __If Button, bot will return results in button format__
- __If List, bot will return results in list format__


__You can toggle with right side buttons__:-"""

@Client.on_message(filters.command(["settings"]))
async def user_settings(bot, update):
    user_id = update.from_user.id
    set_kb = await find_search_settings(user_id)
    await update.reply_photo(
        photo=random.choice(PICS),
        caption=SET_MSG,
        chat_id=user_id,
        reply_markup=set_kb,
    )


@Client.on_callback_query(filters.regex(r"^prec (.+)$"))
async def set_precise_mode(bot, query):
    user_id = query.from_user.id
    prsc_mode = query.data.split()[1]
    if prsc_mode == "on":
        await change_search_settings(user_id, precise_mode=True)
    if prsc_mode == "off":
        await change_search_settings(user_id, precise_mode=False)
    if prsc_mode == "md":
        await query.answer(text="Toggle Precise Search ON/OFF", show_alert=False)
        return

    set_kb = await find_search_settings(user_id)

    await query.message.edit(
        text=SET_MSG,
        reply_markup=set_kb,
    )


@Client.on_callback_query(filters.regex(r"^res (.+)$"))
async def set_list_mode(bot, query):
    user_id = query.from_user.id
    result_mode = query.data.split()[1]
    if result_mode == "btnn":
        await change_search_settings(
            user_id, button_mode=True, link_mode=False, list_mode=False
        )
    if result_mode == "link":
        await change_search_settings(
            user_id, button_mode=False, link_mode=True, list_mode=False
        )
    if result_mode == "list":
        await change_search_settings(
            user_id, button_mode=False, link_mode=False, list_mode=True
        )
    if result_mode == "mode":
        await query.answer(text="Toggle Button/Link/List Mode", show_alert=False)
        return

    set_kb = await find_search_settings(user_id)

    await query.message.edit(
        text=SET_MSG,
        reply_markup=set_kb,
    )


async def find_search_settings(user_id):
    search_settings = await get_search_settings(user_id)

    kb = [
        InlineKeyboardButton("[Precise Mode]:", callback_data="prec md"),
    ]

    on_kb = InlineKeyboardButton("❌ Dɪsᴀʙʟᴇᴅ", callback_data="prec on")
    off_kb = InlineKeyboardButton("✅ Eɴᴀʙʟᴇᴅ", callback_data="prec off")

    if search_settings:
        precise_mode = search_settings.precise_mode
        if precise_mode:
            precise_mode = "Enabled"
            kb.append(off_kb)
        else:
            precise_mode = "Disabled"
            kb.append(on_kb)
    else:
        await change_search_settings(user_id)
        precise_mode = "Disabled"
        kb.append(on_kb)

    bkb = [
        InlineKeyboardButton("[Rᴇsᴜʟᴛ Mᴏᴅᴇ]:", callback_data="res mode"),
    ]

    btn_kb = InlineKeyboardButton("📃 List", callback_data="res btnn")
    link_kb = InlineKeyboardButton("🔳 Button", callback_data="res link")
    list_kb = InlineKeyboardButton("🔗 HyperLink", callback_data="res list")

    if search_settings:
        button_mode = search_settings.button_mode
        link_mode = search_settings.link_mode
        list_mode = search_settings.list_mode
        if button_mode:
            bkb.append(link_kb)
        elif link_mode:
            bkb.append(list_kb)
        elif list_mode:
            bkb.append(btn_kb)
        else:
            await change_search_settings(user_id, link_mode=True)
            bkb.append(list_kb)
    else:
        await change_search_settings(user_id, link_mode=True)
        bkb.append(btn_kb)

    set_kb = InlineKeyboardMarkup([kb, bkb])

    return set_kb
