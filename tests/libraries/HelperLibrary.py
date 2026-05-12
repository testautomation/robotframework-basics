import random

from robot.api.deco import keyword, not_keyword


@keyword(tags=["random"])
def generate_random_number(minimum: int, maximum: int):
    """Generates a random number between `minimum` and `maximum`.

    Example:
    | ${random_number}= | Generate Random Number | ${0} | ${100} |
    =>
    | ${random_number}= 87
    """
    validate_range(minimum, maximum)
    return random.randint(minimum, maximum)


@not_keyword
def validate_range(minimum: int, maximum: int):
    if minimum > maximum:
        raise ValueError(
            f"Minimum ({minimum}) must be less than or equal to maximum ({maximum})!"
        )
