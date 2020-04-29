# coding: utf-8
import unicodedata
from ult.nrlz import Nrlz
import wordninja


class OutlineTool:
    # outline clean
    @staticmethod
    def fix_name(s: str) -> str:
        # References
        if 'References' in s and len(s) != len('References'):
            return 'References'
        else:
            return s

    @staticmethod
    def get_paper_title(ol_data: list) -> str:
        title = ol_data.pop(0)[1]
        return Nrlz.light_normalize(title)

    @staticmethod
    def get_name(olt: tuple) -> str:
        name = olt[1]
        name = Nrlz.light_normalize(name)
        name = OutlineTool.fix_name(name)  # 9527

        return name

    @staticmethod
    def get_type(outline_name: str) -> str:
        if outline_name == 'Acknowledgment':
            return 'ack'

        elif outline_name == 'References':
            return 'ref'

        else:
            return 'sect'

    @staticmethod
    def get_level(outline_type: str) -> int:
        if outline_type == 'ack':
            return 1
        elif outline_type == 'prol':
            return 4

        elif outline_type == 'ref':
            return 3

        elif outline_type == 'sect':
            return 4

    @staticmethod
    def get_detail(olt: tuple) -> str:
        detail = olt[2]
        if detail:
            detail = detail.decode('utf-8', 'ignore')
        else:
            detail = ''

        return Nrlz.light_normalize(detail)

    # find the index of outline in the sentence
    @staticmethod
    def has_outline(target: str, sentence: str) -> list:
        target_token = target.replace(' ', '')
        if target_token not in sentence.replace(' ', ''):
            return []

        last = len(sentence)
        for start in range(last):
            end = start + 1
            while end <= last:
                curr_token = sentence[start:end].replace(' ', '')
                if curr_token == target_token:
                    return [start, end]

                end += 1

        return []

    @staticmethod
    def fix_outlines(data: list) -> list:
        for index in range(len(data)):
            curr_sent = data[index]
            if curr_sent[0:3] == '## ':
                tokens = wordninja.split(curr_sent)
                text = ''
                for word in tokens:
                    text += word + ' '

                data[index] = '## ' + text

        return data

    @staticmethod
    def ol_has_title(title: str, ol: list) -> bool:
        for i in ol:
            if i[1].strip() == title:
                return True
        return False
