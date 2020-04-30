# coding: utf-8
import wordninja

class TextFix:
    ol_symbol = '## '

    def __init__(self, data: str):
        self.data = data
        self.sentences = data.split('\n')

        self.sent_list = list()
        self.text_result = ''

    @staticmethod
    def has_ol_symbol(s: str) -> bool:
        if s[0:3] == TextFix.ol_symbol:
            return True
        else:
            return False

    def launch(self):
        self.fix()
        self.get_text_result()

    def fix(self):
        while self.sentences:
            curr_sent = self.sentences.pop(0)
            if TextFix.has_ol_symbol(curr_sent):
                self.sent_list.append(curr_sent)
            else:
                tokens = wordninja.split(curr_sent)
                if tokens:
                    text = ''
                    for word in tokens:
                        text += word + ' '

                    self.sent_list.append(text)

    def get_text_result(self):
        for s in self.sent_list:
            self.text_result += s + '\n'
