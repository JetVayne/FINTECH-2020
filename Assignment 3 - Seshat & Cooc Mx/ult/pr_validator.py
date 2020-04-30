# coding: utf-8
from ult.nrlz import Nrlz
import enchant


class PRValidator:
    def __init__(self, data: str):
        self.data = data
        self.standard = 70
        self.candidate = list()
        self.dictionary = enchant.Dict('en_US')

        self.score = 0
        self.result = True

    def check(self):
        self.get_candidate()
        if self.candidate:
            self.validate()
            self.get_result()

    def get_candidate(self):
        paragraphs = self.data.split('```')
        for part in paragraphs:
            word_list = part.split(' ')
            for word in word_list:
                if word not in Nrlz.replace_list and Nrlz.is_full_eng(word) and len(word) > 1:
                    self.candidate.append(Nrlz.clean_content(word))

    def validate(self):
        invalid = 0
        for w in self.candidate:
            if not self.dictionary.check(w):
                invalid += 1

        self.score = round((len(self.candidate) - invalid) / len(self.candidate), 2) * 100

    def get_result(self):
        if self.score < self.standard:
            self.result = False
        else:
            self.result = True
