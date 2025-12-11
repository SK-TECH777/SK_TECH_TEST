from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db

VERIFY_KEY = "VERIFY_MODE"

@Client.on_message(filters.command("verifysettings") & filters.private)
async def verify_settings_cmd(client, message):
    data = await db.get_val(VERIFY_KEY)
    status = "ON" if data else "OFF"

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                "Turn OFF" if data else "Turn ON",
                callback_data="toggle_verify")
            ],
            [InlineKeyboardButton("Close", callback_data="close_verify")]
        ]
    )

    await message.reply(
        f"🔒 VERIFY MODE is currently: **{status}**",
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex("^toggle_verify$"))
async def toggle_verify_cb(client, query):
    current = await db.get_val(VERIFY_KEY)
    new_state = not current

    await db.update_val(VERIFY_KEY, new_state)

    new_text = "ON" if new_state else "OFF"
    new_button = "Turn OFF" if new_state else "Turn ON"

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(new_button, callback_data="toggle_verify")],
            [InlineKeyboardButton("Close", callback_data="close_verify")]
        ]
    )

    await query.message.edit_text(
        f"🔒 VERIFY MODE is now: **{new_text}**",
        reply_markup=keyboard
    )

    await query.answer("Updated!", show_alert=False)


@Client.on_callback_query(filters.regex("^close_verify$"))
async def close_verify_cb(client, query):
    await query.message.delete()
    await query.answer()
