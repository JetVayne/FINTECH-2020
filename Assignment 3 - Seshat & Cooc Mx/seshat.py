# coding: utf-8

import os

from paper_parser import PaperParser


class Seshat:
    def __init__(self, file_path: str, single_mode=None):
        self.single_mode = single_mode
        self.file_path_list = list()
        self.input_path = file_path

    # pre-work function 1
    def load_files_path(self, path: str) -> bool:
        if self.single_mode:
            if os.path.exists(path):
                self.file_path_list.append(os.path.abspath(path))
                return True
            else:
                return False

        else:
            if os.path.isdir(path) and os.path.exists(path):
                for file in os.listdir(path):
                    fp = '{}/{}'.format(path, file)
                    if os.path.isfile(fp):
                        self.file_path_list.append(os.path.abspath(fp))
                return True
            else:
                print('[WARN] Please insert an correct path of paper-directory while using the Default mode.')
                return False

    def launch(self):
        if not self.load_files_path(self.input_path):
            print('Input path error !')
            return

        for file_path in self.file_path_list:
            print(file_path, 'Start parsing...')
            paper_parser = PaperParser(file_path)
            paper_parser.parse()
            print(file_path, 'Finish')
