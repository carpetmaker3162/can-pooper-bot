WORD_CHOICES = [
    "bozo",
    "ratio",
    "you are a bozo",
]

FIGURES = [r"""
 |-----
 |    O
 |   /|\
 |   / \
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
 |    |
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
 |    
 |    
 |      
_|_
""",
]

class Hangman:
    def __init__(self, target_word) -> None:
        self.target = target_word
        self.configuration = ["_" if x != " " else " " for x in self.target]
        self.letters = list(target_word)
        self.wrong_guesses = []
        self.life = 0 # 6 = death
    
    def guess(self, guess):
        if len(guess) == 1:
            if guess in self.target:
                self.occurrences_of_letter = [i for i, x in enumerate(self.target) if x == guess]
                for i in self.occurrences_of_letter:
                    self.configuration[i] = guess
                if ''.join(self.configuration) == self.target:
                    return 0 # Win
                return 1 # Correct guess
            else:
                self.life += 1
                if self.life == 6:
                    return -999 # Death
                self.wrong_guesses.append(guess)
                return -1 # Incorrect guess (guessing letter)
        else:
            if guess == self.target:
                self.configuration = list(self.target)
                return 0 # Win
            else:
                self.life += 1
                if self.life == 6:
                    return -999 # Death
                return -2 # Incorrect guess (guessing word)