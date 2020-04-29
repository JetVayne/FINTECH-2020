# coding: utf-8
import re
import unicodedata


class Nrlz:
    replace_list = ['', '\xa0/\xa0', '「', '」', '。', ',', '.', '"', ':', ')', '(', '-', '!', '！', '?', '|', ';', "'",
                    '$', '&', '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•', '~', '@', '£',
                    '·', '_', '{', '}', '©', '^', '®', '`', '<', '→', '°', '€', '™', '›', '♥️', '←', '×', '§', '″',
                    '′', 'Â', '█', '½', 'à', '…',
                    '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦',
                    '║', '―', '¥', '▓', '—', '‹', '─',
                    '▒', '：', '¼', '⊕', '▼', '▪️', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦️', '¤', '▲',
                    'è', '¸', '¾', 'Ã', '⋅', '‘', '∞',
                    '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤️',
                    'ï', 'Ø', '¹', '≤', '‡', '√', '#', '—–', '\u0000',
                    '【', '】', '？', '％', '____', '\r', '\t', '\n', ' ']

    @staticmethod
    def light_normalize(s: str) -> str:
        return unicodedata.normalize('NFKC', s.strip()).replace('\n', '').replace('\t', '')

    @staticmethod
    def clean_content(raw_content: str) -> str:
        for rc in Nrlz.replace_list:
            raw_content = raw_content.replace(rc, '')

        return raw_content

    @staticmethod
    def is_full_eng(text: str) -> str:
        for c in text:
            if not Nrlz.is_english(c):
                return False
        return True

    @staticmethod
    def is_english(char: str) -> bool:
        pattern = re.compile(r'[a-zA-Z]')
        check = pattern.search(char)
        if check:
            return True
        else:
            return False
