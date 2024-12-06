"""
Orig Author: Viet Nguyen <nhviet1009@gmail.com>
Maintainer: brightsunshine0917 <https://github.com/brightsunshine0917>
"""

import json
from collections.abc import Generator

import numpy as np
from cv2.typing import MatLike
from PIL import Image, ImageDraw, ImageFont, ImageOps

from .consts import ALPHABETS_PATH, FONT_FOLDER


def sort_chars(char_list, font, language) -> str:
    if language == "chinese":
        char_width, char_height = get_size(font, "制")
    elif language == "korean":
        char_width, char_height = get_size(font, "ㅊ")
    elif language == "japanese":
        char_width, char_height = get_size(font, "あ")
    elif (
        language in ("english", "german", "french", "spanish", "italian", "portuguese", "polish")
        or language == "russian"
    ):
        char_width, char_height = get_size(font, "A")
    num_chars = min(len(char_list), 100)
    out_width = char_width * len(char_list)
    out_height = char_height
    out_image = Image.new("L", (out_width, out_height), 255)
    draw = ImageDraw.Draw(out_image)
    draw.text((0, 0), char_list, fill=0, font=font)
    cropped_image = ImageOps.invert(out_image).getbbox()
    out_image = out_image.crop(cropped_image)
    brightness = [np.mean(np.array(out_image)[:, 10 * i : 10 * (i + 1)]) for i in range(len(char_list))]
    char_list = list(char_list)
    zipped_lists = zip(brightness, char_list, strict=False)
    zipped_lists = sorted(zipped_lists)
    result = []
    counter = 0
    incremental_step = (zipped_lists[-1][0] - zipped_lists[0][0]) / num_chars
    current_value = zipped_lists[0][0]
    for value, char in zipped_lists:
        if value >= current_value:
            result.append(char)
            counter += 1
            current_value += incremental_step
        if counter == num_chars:
            break
    if result[-1] != zipped_lists[-1][1]:
        result.append(zipped_lists[-1][1])
    return "".join(result)


def get_data(language, mode):
    with open(ALPHABETS_PATH, "rb") as f:
        lang_charinfo = json.load(f)

    charinfo = lang_charinfo.get(language)
    if charinfo is None:
        raise ValueError(f"Invalid language: expected one of {', '.join(lang_charinfo)}, got {language}")
    font = ImageFont.truetype(FONT_FOLDER / charinfo["font-name"], size=charinfo["font-size"])
    sample_character = charinfo["sample_character"]
    scale = charinfo["scale"]

    if mode not in charinfo["modes"]:
        raise ValueError(
            f"Invalide mode: expected one of {', '.join(charinfo['modes'])} for {language}, got {mode}"
        )
    chars = charinfo["modes"][mode]

    if language != "general":
        chars = sort_chars(chars, font, language)

    return chars, font, sample_character, scale


def get_size(font: ImageFont.FreeTypeFont, char: str) -> tuple[float, float]:
    char_bbox = font.getbbox(char)
    return char_bbox[2] - char_bbox[0], char_bbox[3]


def gen_rowchars(
    image: MatLike,
    candidate_chars: str,
    *,
    height: float,
    width: float,
    cell_width: float,
    cell_height: float,
    num_chars: int,
    num_rows: int,
    num_cols: int,
) -> Generator[list[str], None, None]:
    row_chars = []
    for rowno in range(num_rows):
        for colno in range(num_cols):
            block = image[
                int(rowno * cell_height) : min(int((rowno + 1) * cell_height), height),
                int(colno * cell_width) : min(int((colno + 1) * cell_width), width),
            ]
            avg_brightness = np.mean(block) / 255 * num_chars
            row_chars.append(candidate_chars[min(int(avg_brightness), num_chars - 1)])

        yield row_chars
        row_chars.clear()


def gen_colored_char(
    image: MatLike,
    candidate_chars: str,
    *,
    height: float,
    width: float,
    cell_width: float,
    cell_height: float,
    num_chars: int,
    num_rows: int,
    num_cols: int,
) -> Generator[tuple[str, int, int, tuple], None, None]:
    for rowno in range(num_rows):
        for colno in range(num_cols):
            partial_image = image[
                int(rowno * cell_height) : min(int((rowno + 1) * cell_height), height),
                int(colno * cell_width) : min(int((colno + 1) * cell_width), width),
                :,
            ]
            partial_avg_color = np.sum(np.sum(partial_image, axis=0), axis=0) / (cell_height * cell_width)
            partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
            char = candidate_chars[min(int(np.mean(partial_image) * num_chars / 255), num_chars - 1)]
            yield char, rowno, colno, partial_avg_color
