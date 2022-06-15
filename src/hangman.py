import random
from src.consts import LWORDS

FIGURES = [
r"""
 |-----
 |    
 |    
 |      
_|_
""",
r"""
 |-----
 |    O
 |    
 |      
_|_
""",
r"""
 |-----
 |    O
 |    |
 |      
_|_
""",
r"""
 |-----
 |    O
 |    |\
 |      
_|_
""",
r"""
 |-----
 |    O
 |   /|\
 |      
_|_
""",
r"""
 |-----
 |    O
 |   /|\
 |     \
_|_
""",
r"""
 |-----
 |    O
 |   /|\
 |   / \
_|_
""",
]

class Hangman:
    def __init__(self, target_word) -> None:
        self.target = target_word
        self.configuration = ["_" if x != " " else " " for x in self.target]
        self.letters = list(target_word)
        self.wrong_guesses = []
        self.life = 0
    
    def guess(self, guess):
        if len(guess) == 1:
            if guess in self.target:
                self.occurrences_of_letter = [i for i, x in enumerate(self.target) if x == guess]
                for i in self.occurrences_of_letter:
                    self.configuration[i] = guess
                if ''.join(self.configuration) == self.target:
                    return 0
                return 1
            else:
                self.life += 1
                if self.life == 6:
                    return -999
                self.wrong_guesses.append(guess)
                return -1
        else:
            if guess == self.target:
                self.configuration = list(self.target)
                return 0
            else:
                self.life += 1
                if self.life == 6:
                    return -999
                return -2

WORD_CHOICES = {
    "people": [
        "anthony huang",
        "mazin ghizali",
        "mazin",
        "can pooper",
        "null",
        "neng li",
        "liangyue zhao",
        "deshpande",
        "shiva",
        "jay mardikar",
        "yue",
        "fhdbot",
        "fhdhgngn",
    ],
    "random": [],
    "food": [
        "deez nuts",
        "hamburger",
        "cheeseburger",
        "tomato",
        "potato",
        "french fries",
        "cock",
        "chicken",
        "beef",
        "abcdefghijklmnopqrstuvwxyz"
    ],
    "countries": [
        "afghanistan",
        "albania",
        "algeria",
        "argentina",
        "armenia",
        "argentina",
        "austria",
        "australia",
        "bahamas",
        "bangladesh",
        "belarus",
        "belgium",
        "bolivia",
        "botswana",
        "brazil",
        "bulgaria",
        "cambodia",
        "canada",
        "chad",
        "chile",
        "china",
        "colombia",
        "costa rica",
        "croatia",
        "cuba",
        "czechia",
        "denmark",
        "dominica",
        "ecuador",
        "egypt",
        "estonia",
        "eritrea",
        "ethiopia",
        "finland",
        "france",
        "georgia",
        "greece",
        "haiti",
        "hungary",
        "iceland",
        "india",
        "indonesia",
        "iran",
        "iraq",
        "iceland",
        "israel",
        "italy",
        "jamaica",
        "japan",
        "jordan",
        "kenya",
        "kuwait",
        "laos",
        "latvia",
        "lebanon",
        "liberia",
        "libya",
        "liechtenstein",
        "lithuania",
        "luxembourg",
        "madagascar",
        "malaysia",
        "maldives",
        "mali",
        "malta",
        "mexico",
        "mongolia",
        "myanmar",
        "nepal",
        "netherlands",
        "new zealand",
        "nigeria",
        "north korea",
        "norway",
        "oman",
        "pakistan",
        "palestine state",
        "panama",
        "papua new guinea",
        "peru",
        "philippines",
        "poland",
        "portugal",
        "romania",
        "russia",
        "saudi arabia",
        "serbia",
        "singapore",
        "slovakia",
        "somalia",
        "south africa",
        "south korea",
        "soviet union",
        "spain",
        "sudan",
        "sri lanka",
        "sweden",
        "switzerland",
        "syria",
        "thailand",
        "russia",
        "turkey",
        "turkmenistan",
        "uganda",
        "ukraine",
        "united arab emirates",
        "united kingdom",
        "united states",
        "venezuela",
        "vietnam",
        "yemen",
        "zambia",
        "zimbabwe",
    ]
}

for i in range(100):
    WORD_CHOICES["random"].append(random.choice(LWORDS))