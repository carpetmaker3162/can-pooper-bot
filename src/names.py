import requests
from bs4 import BeautifulSoup

async def get_name():
    r = requests.get(f"https://www.behindthename.com/random/random.php?gender=both&number=4&sets=1&surname=&all=yes")
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find_all("div", {"class": "random-results"})[0]
    return " ".join([tag.text for tag in div.find_all("a")])