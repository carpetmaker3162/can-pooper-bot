import requests
from bs4 import BeautifulSoup

def get_name():
    r = requests.get(f"http://www.behindthename.com/random/random.php?gender=both&number=4&sets=1&surname=&norare=yes&nodiminutives=yes&all=yes/")
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find_all("div", {"class": "random-results"})[0]
    name = " ".join([tag.text for tag in div.find_all("a")])
    return name[:32]

if __name__ == "__main__":
    print(get_name())