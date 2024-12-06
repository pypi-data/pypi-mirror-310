import random
import string


def generate_random_string(
    length: int,
    digits: bool = True,
    lowers: bool = True,
    uppers: bool = True,
    punctuations: bool = True,
    exclude: list[str] = None,
) -> str:
    """Generate a random string with specified characteristics.

    Args:
        length (int): Length of the random string to generate
        digits (bool, optional): Include digits. Defaults to True.
        lowers (bool, optional): Include lowercase letters. Defaults to True. 
        uppers (bool, optional): Include uppercase letters. Defaults to True.
        punctuations (bool, optional): Include punctuation characters. Defaults to True.
        exclude (list[str], optional): Characters to exclude from the generated string. Defaults to None.

    Returns:
        str: Random string with the specified length and character types
    """
    runes = ''
    if digits:
        runes += string.digits
    if lowers:
        runes += string.ascii_lowercase
    if uppers:
        runes += string.ascii_uppercase
    if punctuations:
        runes += string.punctuation
    if exclude:
        runes = list(set(runes) - set(exclude))
    return ''.join(random.choice(runes) for _ in range(length))
