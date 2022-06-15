import random
from src.consts import FIRST_NAMES
from src.consts import LAST_NAMES
from src.consts import STREET_NAME_ENDINGS
from src.consts import STREET_TYPES
from src.consts import LWORDS
from string import ascii_lowercase, ascii_uppercase, digits
import base64

class Doxxer:
    def __init__(self, seed) -> None:
        random.seed(seed)
        
        self.full_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        self.age = random.randrange(2,130)
        self.gender = random.choice(("Male", "Male", "Male", "Female", "Female", "Female", "Non-binary"))
        self.address = f"{random.randrange(1, 2500)} {random.choice(LWORDS).title()}{random.choice(STREET_NAME_ENDINGS)} {random.choice(STREET_TYPES)}"
        self.ip = f"{random.randrange(0, 256)}.{random.randrange(0, 256)}.{random.randrange(0, 256)}.{random.randrange(0, 256)}"
        
        t1 = ''.join([random.choice(ascii_uppercase + ascii_uppercase + ascii_uppercase + ascii_lowercase + digits) for i in range(24)])
        t2 = ''.join([random.choice(ascii_uppercase + ascii_uppercase + digits) for i in range(6)])
        t3 = ''.join([random.choice(ascii_uppercase + ascii_lowercase + digits) for i in range(11)])
        t4 = ''.join([random.choice(ascii_uppercase + digits) for i in range(5)])
        
        self.token = t1 + t2 + t3 + t4
        random.seed(None)