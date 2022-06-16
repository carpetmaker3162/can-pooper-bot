import requests
import re
from bs4 import BeautifulSoup

IGNORED_TYPES = ['Help:', 'File:', 'Wikipedia:', 'Talk:', '_(disambiguation)', '/upload.wikimedia', 'Category:']
IGNORED_HTML_TAGS = ['i', 'em', 'cite', 'tr', 'sup', 'span', 'small', 'ul']
IGNORED_CLASSES = ['navbox', 'vertical-navbox', 'toc', 'mw-editsection']

"""r = requests.get("https://en.wikipedia.org/wiki/Trump")
soup = BeautifulSoup(r.text, "html.parser").find(class_="mw-parser-output")

for i in soup.find_all("a"):
    href = i.get('href')
    if href.startswith("/wiki/"):
        print(href)

for i in soup.find_all("p"):
    txt = re.sub("(\[\d*\])", "", i.text)
    print(txt)"""


class Crawler:
    def __init__(self, url) -> None:
        self.url = url
        self.r = requests.get(self.url)
        self.soup = BeautifulSoup(self.r.text, "html.parser").find(class_="mw-parser-output")
        self.notable = self.soup
        self.results = []
        self.disambiguation = False
        for table in self.notable.find_all("table"):
            table.decompose()
    
    def search_paragraphs(self):
        paras = self.notable.find_all("p")
        for i in paras:
            if i.text == "\n":
                paras.remove(i)

        for i in paras[:3]:
            txt = re.sub("(\[.*\])", "", i.text)
            txt = txt.replace("\n", "")
            if ("also refer" in txt) or ("commonly refer" in txt) or ("may refer" in txt):
                self.disambiguation = True
                self.results = []
                self.search_hrefs()
                break
            self.results.append(txt)
    
    def search_hrefs(self):
        for i in self.soup.find_all("a")[:4]:
            href = i.get('href')
            if href.startswith("/wiki/"):
                href = href.replace("/wiki/", "").replace("_", r"\_")
                self.results.append(href)

if __name__ == "__main__":
    # Testing purposes
    c = Crawler("https://en.wikipedia.org/wiki/Trump")
    c.search_paragraphs()
    print(c.results)
    print(c.disambiguation)