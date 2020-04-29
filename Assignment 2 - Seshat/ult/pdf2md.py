# coding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Pdf2Md:
    sever_url = 'https://pdf2md.morethan.io/'
    loading_css_query = '#main > div > div > div > div > div.btn-toolbar > div > button:nth-child(1)'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')

    def __init__(self, pdf_abs_path: str):
        self.file_path = pdf_abs_path
        self.driver = None

    def convert(self) -> str:
        self.driver = webdriver.Chrome(options=Pdf2Md.chrome_options)
        self.driver.get(Pdf2Md.sever_url)
        self.driver.find_element_by_css_selector('input[type="file"]').send_keys(self.file_path)

        # wait for uploading pdf file
        self.wait_for_uploading()

        self.driver.find_element_by_css_selector(Pdf2Md.loading_css_query).click()

        result = self.driver.find_element_by_css_selector('textarea').text
        self.driver.close()

        return result

    def wait_for_uploading(self) -> bool:
        flag = True
        while flag:
            try:
                check = self.driver.find_element_by_css_selector(Pdf2Md.loading_css_query)
                if check:
                    flag = False
            except:
                pass

        return True
