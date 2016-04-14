"""Text related utilities."""
import random


def create_random_string(length=7, chars='ABCDEFGHJKMNPQRSTUVWXYZ23456789',
                         repetitions=False):
    """
    Returns a random string, based on the provided arguments.

    It returns capital letters and numbers by default.
    Ambiguous characters are left out, repetitions will be avoided.

    """
    if repetitions:
        return ''.join(random.choice(chars) for _ in range(length))
    return ''.join(random.sample(chars, length))
