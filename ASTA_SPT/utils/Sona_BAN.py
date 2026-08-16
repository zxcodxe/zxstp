# =======================================================
# ©️ 2025-26 All Rights Reserved by ASTA SPT (7808531413) 🚀
#
# This source code is under MIT License 📜
# =======================================================

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus


USE_AS_BOT = True


# =======================================================
# SUDO FILTER
# =======================================================

def f_sudo_filter(filt, client, message):
    try:
        return bool(
            (
                (
                    message.from_user
                    and message.from_user.id in SUDO_USERS
                )
                or
                (
                    message.sender_chat
                    and message.sender_chat.id in SUDO_USERS
                )
            )
            and not message.edit_date
        )
    except Exception:
        return False


sudo_filter = filters.create(
    func=f_sudo_filter,
    name="SudoFilter"
)


# =======================================================
# OWNER FILTER
# =======================================================

def onw_filter(filt, client, message):
    if USE_AS_BOT:
        return bool(
            not message.edit_date
        )

    return bool(
        message.from_user
        and message.from_user.is_self
        and not message.edit_date
    )


f_onw_fliter = filters.create(
    func=onw_filter,
    name="OnwFilter"
)


# =======================================================
# ADMIN FILTER
# =======================================================

async def admin_filter_f(filt, client, message):
    if message.edit_date:
        return False

    if not message.from_user:
        return False

    if not message.chat:
        return False

    try:
        member = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )

        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        )

    except Exception:
        return False


admin_filter = filters.create(
    func=admin_filter_f,
    name="AdminFilter"
)


# =======================================================
# ©️ 2025-26 All Rights Reserved by ASTA SPT (7808531413) 😎
#
# 🧑‍💻 Developer : t.me/ixasta1
# 🔗 Source link : GitHub.com/7808531413/Asta-MusicV2
# 📢 Telegram channel : t.me/ixasta1
# =======================================================
