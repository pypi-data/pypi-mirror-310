import importlib.resources
import re
from typing import Literal

import requests

from .tsvreader import TSVReader


class TextParser:
    with importlib.resources.path(
        "hg2_item_parser.resources", "TextMap_aio.tsv"
    ) as resource:
        textmap = TSVReader(resource)
    en_re_url = "http://ggz.amaryllisworks.pw:18880/en_re"
    en_re: dict[str, str] = requests.get(en_re_url).json()

    @classmethod
    def parse_text(cls, text_id: str | int) -> str | Literal["XXX"]:
        text_en_re = cls.parse_text_en_re(text_id)
        text_textmap = cls.parse_text_textmap(text_id)

        return text_en_re or text_textmap or "XXX"

    @classmethod
    def parse_text_en_re(cls, text_id: str | int) -> str | None:
        text_en_re = cls.en_re.get(str(text_id))

        return text_en_re

    @classmethod
    def parse_text_textmap(cls, text_id: str | int) -> str | None:
        text_textmap = cls.textmap.get_row_by_column_value("TEXT_ID", text_id)
        if text_textmap is not None:
            return text_textmap["EN"]

        return None

    @staticmethod
    def fill_description_template(
        description_template: str,
        max_lvl_values: list[float],
        max_up_values: list[float],
    ) -> str:
        description = re.sub(r"# ?!?ALB ?\(\d+\)", "", description_template)
        description = description.replace("#n", "")
        description = description.replace(" %", "%")

        for i, max_lvl_value, max_up_value in zip(
            range(1, 7), max_lvl_values, max_up_values, strict=False
        ):
            if f"#{i}%" in description:
                max_lvl_value *= 100
                max_up_value *= 100

            match = re.search(rf"([1-9]+)#{i}", description)
            if match is not None:
                mul = match.group(1)
                max_lvl_value *= int(mul)
                max_up_value *= int(mul)
            else:
                mul = ""

            fill_value = f"{max_lvl_value:g}"
            if max_lvl_value != max_up_value:
                fill_value += f"({max_up_value:g})"

            description = description.replace(f"{mul}#{i}", fill_value)

        description = description.strip()

        return description
