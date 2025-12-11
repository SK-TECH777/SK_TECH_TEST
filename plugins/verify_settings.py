# Verify settings toggler
# Accessible only to OWNER_ID

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from config import OWNER_ID, get_verify_mode_value, set_verify_mode_value

@Client.on_message(filters.command("verifysettings") & filters.private & filters.user(OWNER_ID))
async def verify_settings_cmd(client, message: Message):
    mode = get_verify_mode_value()
    kb = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Turn OFF" if mode else "Turn ON", callback_data="toggle_verify")],
            [InlineKeyboardButton("Close", callback_data="close")]
        ]
    )
    await message.reply_text(
        f"🔐 VERIFY MODE is currently: **{'ON' if mode else 'OFF'}**",
        reply_markup=kb,
        parse_mode="html"
    )

@Client.on_callback_query(filters.regex("^toggle_verify$"))
async def toggle_verify_cb(client, query: CallbackQuery):
    mode = get_verify_mode_value()
    new = not mode
    set_verify_mode_value(new)
    kb = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Turn OFF" if new else "Turn ON", callback_data="toggle_verify")]]
    )
    await query.message.edit_text(
        f"✅ VERIFY MODE updated to: **{'ON' if new else 'OFF'}**",
        reply_markup=kb,
        parse_mode="html"
    )
