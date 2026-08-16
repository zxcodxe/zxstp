# =======================================================
# ©️ 2025-26 All Rights Reserved by ASTA SPT (7808531413) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @ixasta1
# =======================================================

from pyrogram.enums import ParseMode

from ASTA_SPT import app
from ASTA_SPT.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
<b>❖ {app.mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>● ᴄʜᴀᴛ ɪᴅ ➠</b> <code>{message.chat.id}</code>
<b>● ᴄʜᴀᴛ ɴᴀᴍᴇ ➠</b> {message.chat.title}
<b>● ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{message.chat.username}

<b>● ᴜsᴇʀ ɪᴅ ➠</b> <code>{message.from_user.id}</code>
<b>● ɴᴀᴍᴇ ➠</b> {message.from_user.mention}
<b>● ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{message.from_user.username}

<b>● ǫᴜᴇʀʏ ➠</b> {message.text.split(None, 1)[1]}
<b>● sᴛʀᴇᴀᴍᴛʏᴘᴇ ➠</b> {streamtype}"""
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return

# ======================================================
# ©️ 2025-26 All Rights Reserved by ASTA SPT (7808531413) 😎

# 🧑‍💻 Developer : t.me/ixasta1
# 🔗 Source link : GitHub.com/7808531413/Asta-MusicV2
# 📢 Telegram channel : t.me/ixasta1
# =======================================================
