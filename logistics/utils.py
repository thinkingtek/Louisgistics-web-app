import random
import string


def create_ref_code():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=15))
