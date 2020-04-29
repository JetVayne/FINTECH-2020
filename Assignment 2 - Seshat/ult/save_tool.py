# coding: utf-8
import json


class SaveTool:
    @staticmethod
    def create_json_file(data, fn):
        with open(fn, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
