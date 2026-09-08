"""ごはん日記のアプリアイコンを生成する（柿色の地に「食」）。"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
BG = (193, 68, 30)       # #C1441E 柿色
FG = (247, 245, 239)     # #F7F5EF 生成り
GLYPH = "食"
SIZES = [180, 192, 512]

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\meiryob.ttc",
    r"C:\Windows\Fonts\YuGothB.ttc",
    r"C:\Windows\Fonts\meiryo.ttc",
    r"C:\Windows\Fonts\YuGothM.ttc",
    r"C:\Windows\Fonts\msgothic.ttc",
]


def pick_font_path():
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def draw_icon(size, font_path):
    img = Image.new("RGB", (size, size), BG)
    draw = ImageDraw.Draw(img)
    target = int(size * 0.52)

    font = None
    for pt in range(target, 8, -2):
        try:
            candidate = ImageFont.truetype(font_path, pt)
        except OSError:
            return None
        box = draw.textbbox((0, 0), GLYPH, font=candidate)
        if (box[2] - box[0]) <= target and (box[3] - box[1]) <= target:
            font = candidate
            break
    if font is None:
        return None

    box = draw.textbbox((0, 0), GLYPH, font=font)
    x = (size - (box[2] - box[0])) / 2 - box[0]
    y = (size - (box[3] - box[1])) / 2 - box[1]
    draw.text((x, y), GLYPH, font=font, fill=FG)
    return img


def main():
    font_path = pick_font_path()
    if not font_path:
        print("NG: 日本語フォントが見つかりません")
        return 1

    for size in SIZES:
        img = draw_icon(size, font_path)
        if img is None:
            print(f"NG: {size}px の描画に失敗しました")
            return 1
        out = os.path.join(OUT_DIR, f"icon-{size}.png")
        img.save(out, "PNG")
        print(f"OK: icon-{size}.png")
    print(f"font: {font_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
