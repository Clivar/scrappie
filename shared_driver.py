from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class SharedDriver:
    _instance = None

    @staticmethod
    def get_instance():
        if SharedDriver._instance is None:
            options = Options()
            options.add_argument('-headless')
            SharedDriver._instance = webdriver.Firefox(options=options)
        return SharedDriver._instance