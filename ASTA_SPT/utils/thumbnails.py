# =======================================================
# ©️ 2025-26 All Rights Reserved by ASTA SPT (7808531413) 🚀

# This source code is under MIT License 📜 Unauthorized forking, importing, or using this code without giving proper credit will result in legal action ⚠️

# 📩 DM for permission : @ixasta1
# =======================================================

import os
import re
import random
import aiohttp
import aiofiles
import traceback

from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageOps,
)

from youtubesearchpython.__future__ import VideosSearch
from config import TELEGRAM_AUDIO_URL


def changeImageSize(maxWidth, maxHeight, image):
    ratio = min(
        maxWidth / image.size[0],
        maxHeight / image.size[1],
    )

    newSize = (
        int(image.size[0] * ratio),
        int(image.size[1] * ratio),
    )

    return image.resize(newSize, Image.LANCZOS)


def truncate(text, max_chars=50):
    words = text.split()
    text1, text2 = "", ""

    for word in words:
        if len(text1 + " " + word) <= max_chars and not text2:
            text1 += " " + word
        else:
            text2 += " " + word

    return [text1.strip(), text2.strip()]


def fit_text(draw, text, max_width, font_path, start_size, min_size):
    size = start_size

    while size >= min_size:
        font = ImageFont.truetype(font_path, size)

        if draw.textlength(text, font=font) <= max_width:
            return font

        size -= 1

    return ImageFont.truetype(font_path, min_size)


def get_overlay_content_box(overlay_img: Image.Image) -> tuple:
    alpha = overlay_img.getchannel("A")
    threshold = 20

    binary = alpha.point(
        lambda p: 255 if p > threshold else 0
    )

    bbox = binary.getbbox()

    # If overlay is completely transparent,
    # use the complete image area instead of returning None.
    if bbox is None:
        return (
            0,
            0,
            overlay_img.width,
            overlay_img.height,
        )

    return bbox


async def get_thumb(videoid: str):
    url = f"https://www.youtube.com/watch?v={videoid}"

    try:
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = re.sub(
            r"\W+",
            " ",
            result.get("title", "Unsupported Title"),
        ).title()

        duration = result.get("duration", "00:00")

        thumbnail = (
            result["thumbnails"][0]["url"]
            .split("?")[0]
        )

        views = result.get(
            "viewCount",
            {}
        ).get(
            "short",
            "Unknown Views",
        )

        channel = result.get(
            "channel",
            {}
        ).get(
            "name",
            "Unknown Channel",
        )

        thumb_path = f"cache/thumb{videoid}.png"

        os.makedirs(
            "cache",
            exist_ok=True,
        )

        # Download YouTube thumbnail
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail) as resp:

                    if resp.status == 200:
                        async with aiofiles.open(
                            thumb_path,
                            mode="wb",
                        ) as f:
                            await f.write(
                                await resp.read()
                            )

            youtube = Image.open(
                thumb_path
            ).convert("RGBA")

        except Exception as e:
            print(
                f"[Thumbnail Download Failed] "
                f"Using default image. Error: {e}"
            )

            # Fallback thumbnail
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    TELEGRAM_AUDIO_URL
                ) as resp:

                    if resp.status == 200:
                        async with aiofiles.open(
                            thumb_path,
                            mode="wb",
                        ) as f:
                            await f.write(
                                await resp.read()
                            )

            youtube = Image.open(
                thumb_path
            ).convert("RGBA")

        # Resize background image
        image1 = changeImageSize(
            1280,
            720,
            youtube,
        ).convert("RGBA")

        # Background
        gradient = Image.new(
            "RGBA",
            image1.size,
            (0, 0, 0, 255),
        )

        enhancer = ImageEnhance.Brightness(
            image1.filter(
                ImageFilter.GaussianBlur(5)
            )
        )

        blurred = enhancer.enhance(0.3)

        background = Image.alpha_composite(
            gradient,
            blurred,
        )

        draw = ImageDraw.Draw(background)

        font_path = (
            "ASTA_SPT/assets/font3.ttf"
        )

        # ASTA overlay
        player = Image.open(
            "ASTA_SPT/assets/asta.png"
        ).convert("RGBA").resize(
            (1280, 720)
        )

        overlay_box = get_overlay_content_box(
            player
        )

        content_x1, content_y1, content_x2, content_y2 = (
            overlay_box
        )

        background.paste(
            player,
            (0, 0),
            player,
        )

        # Thumbnail size
        thumb_size = int(
            (content_y2 - content_y1) * 0.55
        )

        # Safety check
        if thumb_size <= 0:
            thumb_size = 300

        thumb_x = content_x1 + 76

        thumb_y = (
            content_y1
            + (
                (
                    content_y2
                    - content_y1
                    - thumb_size
                )
                // 2
            )
            + 40
        )

        # Rounded thumbnail mask
        mask = Image.new(
            "L",
            (thumb_size, thumb_size),
            0,
        )

        draw_mask = ImageDraw.Draw(mask)

        radius = int(
            thumb_size * 0.25
        )

        draw_mask.rounded_rectangle(
            [
                (0, 0),
                (
                    thumb_size,
                    thumb_size,
                ),
            ],
            radius=radius,
            fill=255,
        )

        thumb_square = youtube.resize(
            (thumb_size, thumb_size)
        )

        thumb_square.putalpha(mask)

        background.paste(
            thumb_square,
            (thumb_x, thumb_y),
            thumb_square,
        )

        # Text positions
        text_x = (
            thumb_x
            + thumb_size
            + 30
        )

        title_y = thumb_y + 10

        info_y = (
            title_y
            + int(thumb_size * 0.33)
        )

        duration_y = (
            info_y
            + int(thumb_size * 0.28)
            - 10
        )

        icons_y = duration_y + 40

        def truncate_text(
            text,
            max_chars=30,
        ):
            return (
                text[:max_chars - 3] + "..."
                if len(text) > max_chars
                else text
            )

        short_title = truncate_text(
            title,
            max_chars=20,
        )

        short_channel = truncate_text(
            channel,
            max_chars=20,
        )

        # Fonts
        title_font = fit_text(
            draw,
            short_title,
            600,
            font_path,
            42,
            28,
        )

        info_font = ImageFont.truetype(
            "ASTA_SPT/assets/font.ttf",
            22,
        )

        duration_font = ImageFont.truetype(
            "ASTA_SPT/assets/font.ttf",
            20,
        )

        # Title
        draw.text(
            (text_x, title_y),
            short_title,
            (255, 255, 255),
            font=title_font,
        )

        # Channel + views
        info_text = (
            f"{short_channel} • {views}"
        )

        draw.text(
            (text_x, info_y),
            info_text,
            (200, 200, 200),
            font=info_font,
        )

        # Duration
        duration_text = (
            duration
            if ":" in duration
            else f"00:{duration.zfill(2)}"
        )

        # Progress bar
        bar_length = 260
        bar_height = 5

        bar_x = text_x
        bar_y = duration_y

        draw.line(
            [
                (bar_x, bar_y),
                (
                    bar_x + bar_length,
                    bar_y,
                ),
            ],
            fill="gray",
            width=bar_height,
        )

        draw.line(
            [
                (bar_x, bar_y),
                (
                    bar_x + bar_length // 3,
                    bar_y,
                ),
            ],
            fill="red",
            width=bar_height,
        )

        # Circle on progress
        draw.ellipse(
            [
                (
                    bar_x
                    + bar_length // 3
                    - 5,
                    bar_y - 5,
                ),
                (
                    bar_x
                    + bar_length // 3
                    + 5,
                    bar_y + 5,
                ),
            ],
            fill="red",
        )

        # Time
        draw.text(
            (
                bar_x,
                bar_y + 10,
            ),
            "00:00",
            fill=(200, 200, 200),
            font=duration_font,
        )

        draw.text(
            (
                bar_x
                + bar_length
                - 40,
                bar_y + 10,
            ),
            duration_text,
            fill=(200, 200, 200),
            font=duration_font,
        )

        # Play icons
        icons_path = (
            "ASTA_SPT/assets/play_icons.png"
        )

        if os.path.isfile(icons_path):
            icons_img = Image.open(
                icons_path
            ).convert("RGBA")

            icons_w, icons_h = (
                icons_img.size
            )

            scale_factor = 0.4

            new_size = (
                int(icons_w * scale_factor),
                int(icons_h * scale_factor),
            )

            icons_img = icons_img.resize(
                new_size,
                Image.LANCZOS,
            )

            icons_x = text_x

            background.paste(
                icons_img,
                (icons_x, icons_y),
                icons_img,
            )

        # Remove downloaded thumbnail
        try:
            os.remove(
                f"cache/thumb{videoid}.png"
            )
        except Exception:
            pass

        # Save final thumbnail
        tpath = (
            f"cache/{videoid}.png"
        )

        background.save(tpath)

        return tpath

    except Exception as e:
        print(
            f"[get_thumb Error] {e}"
        )

        traceback.print_exc()

        return None


# ======================================================
# ©️ 2025-26 All Rights Reserved by ASTA SPT (7808531413) 😎

# 🧑‍💻 Developer : t.me/ixasta1
# 🔗 Source link : GitHub.com/7808531413/Asta-MusicV2
# 📢 Telegram channel : t.me/ixasta1
# =======================================================
