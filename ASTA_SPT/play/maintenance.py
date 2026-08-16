# =======================================================
# ©️ 2025-26 All Rights Reserved by ASTA SPT (7808531413) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️
 
# 📩 DM for permission : @ixasta1
# =======================================================

from pyrogram import filters
from pyrogram.types import Message

from ASTA_SPT import app
from ASTA_SPT.misc import SUDOERS
from ASTA_SPT.utils.database import (
    get_lang,
    is_maintenance,
    maintenance_off,
    maintenance_on,
)
from strings import get_string


@app.on_message(filters.command(["maintenance"]) & SUDOERS)
async def maintenance(client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")
    usage = _["maint_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        if await is_maintenance() is False:
            await message.reply_text(_["maint_4"])
        else:
            await maintenance_on()
            await message.reply_text(_["maint_2"].format(app.mention))
    elif state == "disable":
        if await is_maintenance() is False:
            await maintenance_off()
            await message.reply_text(_["maint_3"].format(app.mention))
        else:
            await message.reply_text(_["maint_5"])
    else:
        await message.reply_text(usage)

# ======================================================
# ©️ 2025-26 All Rights Reserved by ASTA SPT (7808531413) 😎

# 🧑‍💻 Developer : t.me/ixasta1
# 🔗 Source link : GitHub.com/7808531413/Asta-MusicV2
# 📢 Telegram channel : t.me/ixasta1
# =======================================================
