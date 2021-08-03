import time
from typing import List

import requests
from telegram import Bot, Update, ParseMode
from telegram.ext import run_async

from tg_bot import dispatcher, StartTime
from tg_bot.modules.disable import DisableAbleCommandHandler

sites_list = {
    "Telegram": "https://api.telegram.org",
    "Kaizoku": "https://animekaizoku.com",
    "Kayo": "https://animekayo.com",
    "Jikan": "https://api.jikan.moe/v3"
}


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""Saya Sedang Online!\n<b>Waktu Online:</b> `{uptime}`""",
        

@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, m: Message):
    start = time()
    m_reply = await m.reply_text("Pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        f"{emoji.PING_PONG} **PONG!!**\n"
        f"`{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@authorized_users_only
async def get_uptime(client: Client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        f"{emoji.ROBOT} Saya Masih Aktif\n"
        f"• **Waktu aktif:** `{uptime}`\n"
        f"• **Waktu mulai:** `{START_TIME_ISO}`"
    )

    update.effective_message.reply_text(reply_msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


__help__ = """
 - /ping - get ping time of bot to telegram server
 - /pingall - get all listed ping time
"""

PING_HANDLER = DisableAbleCommandHandler("ping", ping)
PINGALL_HANDLER = DisableAbleCommandHandler("pingall", pingall)

dispatcher.add_handler(PING_HANDLER)
dispatcher.add_handler(PINGALL_HANDLER)

__mod_name__ = "PING"
__command_list__ = ["ping", "pingall"]
__handlers__ = [PING_HANDLER, PINGALL_HANDLER]
