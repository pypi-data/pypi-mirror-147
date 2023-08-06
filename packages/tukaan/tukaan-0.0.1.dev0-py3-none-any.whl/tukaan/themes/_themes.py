from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ._tcl import Tcl
from ._theme_base import Button, MainNamespace


@dataclass
class ThemeContainer:
    name: str
    parent_theme: str
    image_resource_path: Path
    rules: dict[tuple[str, ...], dict[str, str]]


class CssThemeParser:
    patterns = {
        "bundle": re.compile(r"([a-z*:,]*\s*){(.*?)}"),
        "comment": re.compile(r"/\*.*?\*/"),
        "parent": re.compile(r"@parent\(['|\"](.*?)['|\"]\);"),
        "property": re.compile(r"([a-z-]*):\s*(.*)"),
        "rule": re.compile(r"[^{; ]+:[^};]+"),
        "source": re.compile(r"@source\(['|\"](.*?)['|\"]\);"),
        "variables": re.compile(r"\$([a-z-]*):\s*(.*?);"),
    }

    @classmethod
    def read_file(cls, path: Path) -> str:
        with open(path) as file:
            return str(file.read())

    @classmethod
    def cleanup(cls, file_content: str) -> str:
        cleaned = file_content.replace("\n", "").replace("\t", "")
        for comment in re.findall(cls.patterns["comment"], cleaned):
            cleaned = cleaned.replace(comment, "")

        return cleaned

    @classmethod
    def get_parent_theme(cls, css_theme_str: str) -> str:
        parent_list = re.findall(cls.patterns["parent"], css_theme_str)
        if parent_list:
            return parent_list[-1]
        return "clam"

    @classmethod
    def get_image_resource_paths(cls, css_theme_str: str) -> Path:
        result = re.findall(cls.patterns["source"], css_theme_str)
        return Path(result[-1]).resolve()

    @classmethod
    def get_variables(cls, css_theme_str: str) -> dict[str, str]:
        result = re.findall(cls.patterns["variables"], css_theme_str)
        variables_dict = {}
        for var_key_value in result:
            variables_dict[var_key_value[0]] = var_key_value[1]
        return variables_dict

    @classmethod
    def parse_bundle(cls, selectors_rules_list: list[str]) -> dict[str, str]:
        selectors = tuple(selectors_rules_list[0].strip().split(","))

        splitted_rules = re.findall(cls.patterns["rule"], selectors_rules_list[1])
        rules_dict = {}
        for property_ in splitted_rules:
            key, value = re.findall(cls.patterns["property"], property_)[0]
            rules_dict[key] = value

        return selectors, rules_dict

    @classmethod
    def get_rules(cls, css_theme_str: str) -> dict[str, dict[str, dict[str, str]]]:
        result = {}
        for bundle in re.findall(cls.patterns["bundle"], css_theme_str):
            selectors, rules_dict = cls.parse_bundle(bundle)
            for selector in selectors:
                element, *other = selector.split(":")
                if element not in result:
                    result[element] = {}

                if element == selector:
                    result[element]["rest"] = rules_dict
                else:
                    result[element][":".join(filter(bool, other))] = rules_dict

        return result

    @classmethod
    def load(cls, filename: Path) -> ThemeContainer:
        file_content = cls.cleanup(cls.read_file(filename))
        parent = cls.get_parent_theme(file_content)
        img_res_path = cls.get_image_resource_paths(file_content)
        rules_dict = cls.get_rules(file_content)
        return ThemeContainer(filename.stem, parent, img_res_path, rules_dict)


class TclThemeConstructor:
    def __init__(self, info: ThemeContainer) -> None:
        self.info = info

    def generate(self) -> str:
        return MainNamespace.generate(
            theme_name=self.info.name,
            parent_theme=self.info.parent_theme,
            theme_body=self.generate_theme_body(),
            img_res_path=self.info.image_resource_path,
        )

    def generate_theme_use(self):
        bg = self.info.rules["*"].get("background")
        fg = self.info.rules["*"].get("color")
        focuscolor = self.info.rules["*"]["focus"].get("color")
        selectbg = self.info.rules["*"]["selection"].get("background")
        selectfg = self.info.rules["*"]["selection"].get("color")
        disabledfg = self.info.rules["*"]["disabled"].get("color")
        caretwidth = self.info.rules["*"]["caret"].get("width")
        caretcolor = self.info.rules["*"]["caret"].get("color")
        fontfamily = self.info.rules["*"].get("font-family")
        fontsize = self.info.rules["*"].get("font-size")

        return f"""
        ttk::style theme use {self.info.name}

        ttk::style configure . \\
            -background {bg} \\
            -foreground {fg} \\
            -troughcolor {bg} \\
            -focuscolor {focuscolor} \\
            -selectbackground {selectbg} \\
            -selectforeground {selectfg} \\
            -insertwidth {caretwidth} \\
            -insertcolor {caretcolor} \\
            -fieldbackground {bg} \\
            -font {{{fontfamily} {fontsize}}} \\
            -borderwidth 0 \\
            -relief flat

        tk_setPalette \
            background [ttk::style lookup . -background] \\
            foreground [ttk::style lookup . -foreground] \\
            highlightColor [ttk::style lookup . -focuscolor] \\
            selectBackground [ttk::style lookup . -selectbackground] \\
            selectForeground [ttk::style lookup . -selectforeground] \\
            activeBackground [ttk::style lookup . -selectbackground] \\
            activeForeground [ttk::style lookup . -selectforeground]
        
        ttk::style map . -foreground [list disabled {disabledfg}]

        option add *font [ttk::style lookup . -font]
        """

    def generate_theme_body(self) -> str:
        settings = []
        settings.append(Button.generate(**self.info.rules["button"]))
        return "".join(settings)


class Theme:
    def __init__(self, theme_name: str, *, _theme_use_scipt: str | None = None) -> None:
        self._name = theme_name
        self._theme_use_scipt = _theme_use_scipt

    def use(self) -> None:
        if self._theme_use_scipt:
            Tcl.eval(None, self._theme_use_scipt)
        Tcl.eval(None, f"ttk::style theme use {self._name}")

    @classmethod
    def from_css(cls, path: Path) -> None:
        tcl_theme = TclThemeConstructor(CssThemeParser.load(path))
        print(tcl_theme.generate())
        Tcl.eval(None, tcl_theme.generate())
        return Theme(tcl_theme.info.name, _theme_use_scipt=tcl_theme.generate_theme_use())
