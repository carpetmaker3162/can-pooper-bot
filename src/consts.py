from string import ascii_lowercase, ascii_uppercase, digits
import random

LWORDS = tuple(open("src/words.txt", "r").read().split("\n"))
CHECK_MARK_EMOJI = "\N{WHITE HEAVY CHECK MARK}"
CROSS_MARK_EMOJI = "\N{CROSS MARK}"
HOURGLASS_EMOJI = "\N{HOURGLASS}"
THUMBS_UP_EMOJI = "\N{THUMBS UP SIGN}"
CLOWN_EMOJI = "\N{CLOWN FACE}"
WARNING = "\N{WARNING SIGN}"


FIRST_NAMES = [
    "Jason",
    "Kyle",
    "Joseph",
    "Neng",
    "Da",
    "Jay",
    "Shiva",
    "Osama",
    "Saddam",
    "Hussein",
    "Adolph",
    "Joey",
    "Nicholas",
    "Alex",
    "Dmitri",
    "Vladimir",
    "Zedong",
    "Jihad",
    "Bob",
    "James",
    "Carl",
    "Raku",
    "Canpooper",
    "Shuva",
    "Stalin",
    "Kim Jong",
    "Vladimir",
    "Volodymyr",
    "Bin Laden",
    "Obama",
    "Joe",
    "Kimberly",
    "Thomas",
    "Johannes",
    "Galileo",
    "Luke",
    "Yan",
    "Washington",
    "George",
    "Ryan",
    "Don",
    "Donald",
    "Riley",
    "Google",
    "Mia",
    "Tony",
    "Anthony",
    "Aly",
    "Alyson",
    "Steven",
    "Stephen",
    "Benito",
    "Tim",
    "Jimmy",
    "Nguyen",
    "Abraham",
    "Jesus",
    "Mohammed",
    "Muhammad",
    "Jack",
    "Jackson",
    "COVID"
]

LAST_NAMES = FIRST_NAMES + [
    "Hitler",
    "Mao",
    "Kim",
    "Hawking",
    "Mardikar",
    "Ghizali",
    "Paolini",
    "Massaquoi",
    "Li",
    "Zhao",
    "Ping",
    "Timers",
    "Wood",
    "Lester",
    "Pablo",
    "Putin",
    "Lenin",
    "Stalin",
    "Mussolini",
    "Mardikar",
    "Sedjiu",
    "Mackenzie",
    "II of Poopland",
    "I of Poopland",
    "III of Poopland",
    "IV of Poopland",
    "V of Poopland",
    "+ ratio",
    ":joy_cat: :joy_cat: :joy_cat:",
    random.choice(LWORDS).title(),
    f"#{random.randrange(0,2000)}",
]

STREET_NAME_ENDINGS = [
    "dale",
    "glen",
    "pass",
    "brooke",
    "pooper",
    "raku",
    "",
    "",
    "",
    random.choice(LWORDS),
    ''.join([random.choice(ascii_lowercase + ascii_uppercase + digits) for i in range(random.randrange(1, 20))])
]

STREET_TYPES = [
    "Avenue",
    "Street",
    "Road",
    "Drive",
    "Pass",
    "Plaza",
    "Court",
    "Circle",
    "Boulevard",
    "Freeway",
    "Highway",
    "Way",
    "Pooper",
]


for i in range(25):
    LAST_NAMES.append(random.choice(LWORDS).title())

def substring(string, length):
    idx = random.randrange(0, len(string) - length + 1)
    return string[idx:idx + length]