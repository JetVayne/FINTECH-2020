# coding: utf-8
import datetime
import os
import time
from pprint import pprint as pp

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser

from ult.outline_tool import OutlineTool
from ult.pdf2md import Pdf2Md
from ult.pr_validator import PRValidator
from ult.save_tool import SaveTool
from ult.text_fix import TextFix


class PaperParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.pdf_name = str(os.path.basename(self.file_path)).split('.')[0]
        self.raw_text = ''
        self.paper_info = dict()
        self.outline_data = list()
        self.sent_data = list()
        self.sentences = list()

        # output dictionary
        self.paper_dict = dict()
        self.paper_dict['Title'] = ''
        self.paper_dict['Author'] = ''
        self.paper_dict['Subject'] = ''
        self.paper_dict['KeyWords'] = list()
        self.paper_dict['Outlines'] = list()
        self.paper_dict['Text'] = ''
        self.paper_dict['Date'] = datetime.datetime(1, 1, 1, 0, 0)
        self.paper_dict['HasInfo'] = True
        self.paper_dict['HasOLF'] = True
        self.paper_dict['ForceSplit'] = False

    def parse(self):
        self.load_doc()
        self.get_paper_info()


        self.extract_outlines_from_sent()

        self.load_text()

        self.save_paper_json()

    def load_doc(self):
        self.fetch_text_data()
        self.fetch_raw_outline()

    def fetch_raw_outline(self):
        with open(self.file_path, 'rb') as f:
            parser = PDFParser(f)
            doc = PDFDocument(parser)

            try:
                self.paper_info = doc.info[0]
            except Exception as e:
                self.paper_dict['HasInfo'] = False
                print('No paper-info. ERROR: {}'.format(e))

            raw_outlines = list()
            try:
                raw_outlines = list(doc.get_outlines())
            except Exception as e:
                self.paper_dict['HasOLF'] = False
                print('[WARN] The file does not contain outline-frame.'.format(e))

            if raw_outlines:
                self.meta_helper(doc)
            else:
                self.add_manual_title()
                self.gen_outlines()

    def meta_helper(self, doc):
        # get outlines
        outlines = list(doc.get_outlines())
        # self.add_manual_title()

        # if OutlineTool.ol_has_title(self.paper_dict['Title'], outlines):
        #     self.paper_dict['Title'] = OutlineTool.get_paper_title(outlines)

        self.paper_dict['Title'] = OutlineTool.get_paper_title(outlines)

        for olt in outlines:
            outline_info = dict()
            outline_info['name'] = OutlineTool.get_name(olt)  # get name
            outline_info['type'] = OutlineTool.get_type(outline_info['name'])  # get type
            outline_info['level'] = OutlineTool.get_level(outline_info['type'])  # get level
            outline_info['detail'] = OutlineTool.get_detail(olt)  # get detail
            self.outline_data.append(outline_info)

    def add_manual_title(self):
        title = self.paper_info['Title']
        if isinstance(title, bytes):
            title = title.decode('utf-8', 'ignore')

        elif title == b'':
            self.paper_dict['Title'] = title

    def gen_outlines(self):
        OutlineTool.fix_outlines(self.sent_data)
        for sent in self.sent_data:
            if sent[0:3] == '## ':
                outline_info = dict()
                outline_info['name'] = sent[3:len(sent)]  # get name
                outline_info['type'] = OutlineTool.get_type(outline_info['name'])  # get type
                outline_info['level'] = OutlineTool.get_level(outline_info['type'])  # get level
                outline_info['detail'] = ''  # get detail
                self.outline_data.append(outline_info)

    def fetch_text_data(self):
        print(self.file_path)
        pdf_to_md = Pdf2Md(self.file_path)
        self.raw_text = pdf_to_md.convert()

        # validate the parse-result and fix
        prv = PRValidator(self.raw_text)
        prv.check()

        if prv.result:
            self.sent_data = self.raw_text.split('\n')

        else:
            self.paper_dict['ForceSplit'] = True
            text_fix = TextFix(self.raw_text)
            text_fix.launch()
            self.sent_data = text_fix.sent_list
            self.raw_text = text_fix.text_result

    def get_paper_info(self):
        self.add_manual_title()  # 9527

        # update author
        author = self.paper_info.get('Author')
        if isinstance(author, bytes):
            author = author.decode('utf-8', 'ignore')

        elif author == b'':
            author = ''

        self.paper_dict['Author'] = author

        # update subject
        if self.paper_info.get('doi') and self.paper_info.get('Subject'):
            doi = self.paper_info.get('doi').decode('utf-8', 'ignore')
            subject = self.paper_info.get('Subject').decode('utf-8', 'ignore')
            subject = subject.replace('doi:' + doi, '').strip()
            subject = subject.split(',')[0]
            self.paper_dict['Subject'] = subject

        # update key-words
        key_words = self.paper_info.get('Keywords')
        if key_words:
            key_words = key_words.decode('utf-8', 'ignore')
            key_words = [w.strip() for w in key_words.split(';')]
            self.paper_dict['KeyWords'] = key_words

        # update create date
        date = self.paper_info.get('CreationDate')
        if date:
            date = date.decode('utf-8', 'ignore')[2:-7]
            if len(date) >= 14:
                ts = time.strptime(date, '%Y%m%d%H%M%S')
                self.paper_dict['Date'] = datetime.datetime.fromtimestamp(time.mktime(ts)).strftime('%Y-%m-%d')

            elif len(date) == 8:
                ts = time.strptime(date, '%Y%m%d')
                self.paper_dict['Date'] = datetime.datetime.fromtimestamp(time.mktime(ts)).strftime('%Y-%m-%d')

    def extract_outlines_from_sent(self):

        self.spilt_prologue()

        self.split_outline()


    def spilt_prologue(self):
        prologue = dict()
        first_outline = self.outline_data[0]['name']

        content = list()

        while self.sent_data:
            curr_sent = self.sent_data[0]
            if curr_sent == "```" or curr_sent == "":
                self.sent_data.pop(0)
                continue

            ol_pos_index = OutlineTool.has_outline(first_outline, curr_sent)

            if ol_pos_index:
                if curr_sent != first_outline:

                    ol_st_index = ol_pos_index[0]
                    ol_ed_index = ol_pos_index[1]

                    head_token = curr_sent[0:ol_st_index]
                    if head_token:
                        content.append(head_token)

                    tail_token = curr_sent[ol_ed_index:len(curr_sent)]

                    self.sent_data.pop(0)

                    if tail_token:
                        self.sent_data.insert(0, tail_token)

                    self.sent_data.insert(0, first_outline)
                    break

                else:
                    break

            else:
                content.append(self.sent_data.pop(0))

        text = ''
        for el in content:
            text += el + ' '

        prologue['index'] = 0
        prologue['name'] = 'Prologue'
        prologue['type'] = 'prol'
        prologue['level'] = OutlineTool.get_level(prologue['type'])
        prologue['content'] = text
        prologue['detail'] = ''

        self.paper_dict['Outlines'].append(prologue)

    def split_outline(self):
        for index, outline_info in enumerate(self.outline_data):
            self.outline_helper(index + 1, outline_info)

    def outline_helper(self, index: int, outline_info: dict):
        outline_name = outline_info['name']
        content = list()

        if self.sent_data[0] != outline_name:
            print('開頭不一樣!!!!!!!', self.sent_data[0], outline_name)
            return
        else:
            name = self.sent_data.pop(0)

        if index < len(self.outline_data):
            next_ol_name = self.outline_data[index]['name']
            while self.sent_data:
                curr_sent = self.sent_data[0]
                if curr_sent == "```" or curr_sent == "":
                    self.sent_data.pop(0)
                    continue

                ol_pos_index = OutlineTool.has_outline(next_ol_name, curr_sent)

                # check if current contains outline
                if ol_pos_index:
                    # there are three condition
                    if curr_sent == next_ol_name:  # totally the same
                        break

                    elif curr_sent.strip() == next_ol_name:  # different in ''
                        self.sent_data.pop(0)
                        self.sent_data.insert(0, next_ol_name)
                        break

                    else:  # totally different
                        ol_st_index = ol_pos_index[0]
                        ol_ed_index = ol_pos_index[1]
                        head_token = curr_sent[0:ol_st_index]
                        tail_token = curr_sent[ol_ed_index:len(curr_sent)]
                        if head_token:
                            content.append(head_token)

                        self.sent_data.pop(0)
                        if tail_token:
                            self.sent_data.insert(0, tail_token)

                        self.sent_data.insert(0, next_ol_name)
                        break

                else:
                    content.append(self.sent_data.pop(0).strip().strip('#'))

        else:
            while self.sent_data:
                curr_sent = self.sent_data.pop(0).strip()
                if curr_sent in ["```", '', '  ']:
                    continue
                else:
                    if curr_sent:
                        content.append(curr_sent)

        self.save_outline_dict(index, outline_name, content, outline_info['detail'])

    def save_outline_dict(self, index: int, outline_name: str, content: list, detail: str):
        result = dict()
        result['index'] = index
        result['name'] = outline_name

        if outline_name == 'References':
            result['type'] = 'ref'

        elif 'References' == outline_name.strip():
            result['type'] = 'ref'

        elif 'References' in outline_name:
            print('[Info] Please check the content of Outline - {}'.format(outline_name))
            result['type'] = 'ref'

        elif outline_name == 'Acknowledgment':
            result['type'] = 'ack'

        else:
            result['type'] = 'sect'

        result['level'] = OutlineTool.get_level(result['type'])

        if result['type'] == 'ref':
            result['content'] = content
        else:
            text = ''
            for s in content:
                text += s
            result['content'] = text

        result['detail'] = detail

        self.paper_dict['Outlines'].append(result)

    def load_text(self):
        text = ''
        for outline in self.paper_dict['Outlines']:
            name = outline['name']
            text += name + '\n' + '\n'

            content = outline['content']
            if type(content) == list:
                for s in content:
                    text += s + '\n'

        self.paper_dict['Text'] = text

    def save_paper_json(self):
        if not os.path.exists('PaperJson'):
            os.mkdir('PaperJson')

        fp = 'PaperJson/{}.json'.format(self.pdf_name)
        SaveTool.create_json_file(self.paper_dict, fp)
