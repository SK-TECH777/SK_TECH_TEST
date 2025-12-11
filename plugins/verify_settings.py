from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from config import OWNER_ID, get_verify_mode_value, set_verify_mode_value


TOGGLE_CALLBACK = "verify_toggle_button_239487"
CLOSE_CALLBACK = "verify_close_button_932748"


@Client.on_message(filters.command("verifysettings") & filters.user(OWNER_ID))
async def verify_settings_cmd(client, message: Message):
    mode = get_verify_mode_value()

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Turn OFF" if mode else "Turn ON", callback_data=TOGGLE_CALLBACK)],
        [InlineKeyboardButton("Close", callback_data=CLOSE_CALLBACK)]
    ])

    await message.reply_text(
        f"🔐 VERIFY MODE is currently: <b>{'ON' if mode else 'OFF'}</b>",
        reply_markup=kb,
        parse_mode=ParseMode.HTML
    )


@Client.on_callback_query(filters.regex(f"^{TOGGLE_CALLBACK}$"))
async def toggle_verify_cb(client, query: CallbackQuery):
    await query.answer()  # stop spinner

    if query.from_user.id != OWNER_ID:
        await query.answer("Only owner can change settings!", show_alert=True)
        return

    mode = get_verify_mode_value()
    new = not mode
    set_verify_mode_value(new)

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Turn OFF" if new else "Turn ON", callback_data=TOGGLE_CALLBACK)]
    ])

    await query.message.edit_text(
        f"✅ VERIFY MODE updated to: <b>{'ON' if new else 'OFF'}</b>",
        reply_markup=kb,
        parse_mode=ParseMode.HTML
    )


@Client.on_callback_query(filters.regex(f"^{CLOSE_CALLBACK}$"))
async def close_cb(client, query: CallbackQuery):
    await query.answer()
    await query.message.delete()
