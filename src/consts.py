from string import ascii_lowercase, ascii_uppercase, digits
import random
import yaml

LWORDS = tuple(open("src/words.txt", "r").read().split("\n"))
CHECK_MARK_EMOJI = "\N{WHITE HEAVY CHECK MARK}"
CROSS_MARK_EMOJI = "\N{CROSS MARK}"
HOURGLASS_EMOJI = "\N{HOURGLASS}"
THUMBS_UP_EMOJI = "\N{THUMBS UP SIGN}"
CLOWN_EMOJI = "\N{CLOWN FACE}"
WARNING = "\N{WARNING SIGN}"
ARROW_RIGHT = "➡️"
ARROW_LEFT = "⬅️"
ARROW_UP = "⬆️"
ARROW_DOWN = "⬇️"


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
    "COVID",
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

with open("config.yaml", encoding="UTF-8") as file:
    CONFIG_YAML = yaml.safe_load(file)

class ParseYAML(type):
    subsection = None

    def __getattr__(self, name):
        name = name.lower()

        try:
            if self.subsection is not None:
                return CONFIG_YAML[self.section][self.subsection][name]
            return CONFIG_YAML[self.section][name]
        except KeyError as e:
            dotted_path = '.'.join(
                (self.section, self.subsection, name)
                if self.subsection is not None else (self.section, name)
            )
            print(f"\"{dotted_path}\" doesnt exist in that yaml section/subsection idiot")
            raise AttributeError(repr(name)) from e

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __iter__(self):
        for name in self.__annotations__:
            yield name, getattr(self, name)

class Users(metaclass=ParseYAML):
    section = "users"

class Groups(metaclass=ParseYAML):
    section = "users"
    subsection = "groups"

class Emojis(metaclass=ParseYAML):
    section = "emojis"

class StEndings(metaclass=ParseYAML):
    section = "names"
    subsection = "street_name_endings"

class StTypes(metaclass=ParseYAML):
    section = "names"
    subsection = "street_types"

if __name__ == "__main__":
    print(Users.penis)