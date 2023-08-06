import random
import string


def gen_str(length) -> str:
    """
    Generate a random string of length `length`
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))
