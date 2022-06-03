import requests
import re
from bs4 import BeautifulSoup

IGNORED_TYPES = ['Help:', 'File:', 'Wikipedia:', 'Talk:', '_(disambiguation)', '/upload.wikimedia', 'Category:']
IGNORED_HTML_TAGS = ['i', 'em', 'cite', 'tr', 'sup', 'span', 'small', 'ul']
IGNORED_CLASSES = ['navbox', 'vertical-navbox', 'toc', 'mw-editsection']

class Wikicrawler:
    def __init__(self, url = None) -> None:
        self.url = url
        self.steps = 0
        self.history = []
        self.exit_code = None

    async def crawl(self): # async because i want to implement this in discord bot later
        if not self.url:
            self.url = 'https://en.wikipedia.org/wiki/Special:Random' # Random Wikipedia article if user doesn't specify any

        if not self.url.startswith("https://en.wikipedia.org/wiki/"): # Search for similarly named Wikipedia articles if user only specifies a keyword
            self.url = list(self.url)
            self.url[0] = self.url[0].upper()
            self.url = f"https://en.wikipedia.org/wiki/{''.join(self.url).replace(' ', '_')}"

        r = requests.get(self.url)

        if r.status_code == 404:
            self.url = self.url.replace(" ", "_")
            self.history.append(self.url.removeprefix("https://en.wikipedia.org/wiki/").split("#")[0])
            self.exit_code = 1 # = Page not found
            return self.history

        self.url = r.url

        while self.url != "https://en.wikipedia.org/wiki/Philosophy": # Exit if reached philosophy
            self.history.append(self.url.removeprefix("https://en.wikipedia.org/wiki/").split("#")[0]) # Format "history" list
            self.url = None # Set to None and then change if it can find a URL. If it remains None it will break out
            self.steps += 1
            soup = BeautifulSoup(r.text, 'html.parser').find(id='mw-content-text')
            for tag in soup.find_all(IGNORED_HTML_TAGS): # Delete bad tags
                tag.replace_with("")

            for tag in soup.find_all(class_=IGNORED_CLASSES): # Delete bad classes
                tag.replace_with("")

            paras = soup.find_all(["p", "li"]) # Only check content inside <p> and <li> tags
            for p in paras:
                p = str(p)
                while re.search("[^_]\(", p):
                    p = re.sub("[^_]\(.*?\)", "", p) # Remove everything, including <a> tags, that are inside brackets

                found = None
                for link in BeautifulSoup(p, "html.parser").select("a"):
                    href = link.get('href') # The hyperlink in the <a> HTML tag
                    if re.search('|'.join(IGNORED_TYPES), href): # Check if link is an ignored link
                        continue
                    else:
                        r = requests.get(f"https://en.wikipedia.org{href}") # no need to check for 404 because Wikipedia links are generally not broken
                        self.url = r.url # In case of redirect
                        if self.url in self.history: # Check if the new URL found has already been visited
                            self.exit_code = 2 # = Loop detected
                            return self.history
                        found = True # A valid URL has been found
                        break
                if found:
                    break
            
            if not self.url: # If there is no url in the page
                for p in paras:
                    if "refer" in str(p):
                        self.exit_code = 3 # = Disambiguation page
                        return self.history
                self.exit_code = 4 # = Dead end
                return self.history

        self.exit_code = 0 # = Success
        self.history.append("Philosophy")
        return self.history

    def __repr__(self):
        return "penis"