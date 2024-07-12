import re

class UrlFinder():
    
    def __init__(self, raw_html):
        self.raw_html = raw_html
                    
    def search_urls(self):
        if (self.raw_html is not "error"):
            urls = re.findall('"(http[s]?://.*?)"', self.raw_html)
            return urls