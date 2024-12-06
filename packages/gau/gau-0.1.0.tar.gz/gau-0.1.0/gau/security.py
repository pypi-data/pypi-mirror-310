from hashlib import pbkdf2_hmac
from strings import generate_random_string


def hash_password(password: str, salt: str, iterations: int = 100_000) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256.

    Args:
        password (str): The password to hash
        salt (str): Salt for hashing
        iterations (int, optional): Number of hash iterations. Defaults to 100,000.

    Returns:
        str: Hexadecimal string of the hashed password
    """
    return pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), iterations).hex()


def stringify_password(password: str, salt: str = "", iterations: int = 100_000, sep: str = '$') -> str:
    """
    Create a string representation of a hashed password with its parameters.

    Args:
        password (str): The password to hash and stringify
        salt (str, optional): Salt for hashing. Defaults to "".
        iterations (int, optional): Number of hash iterations. Defaults to 100,000.
        sep (str, optional): Separator for components. Defaults to '$'.

    Returns:
        str: Formatted string containing salt, iterations, and hashed password
            in the format: "salt$iterations$hashed_password"
    """
    if salt == "" or not salt or salt is None:
        salt = generate_random_string(
            16, digits=True, lowers=True, uppers=True, punctuations=False)
    if not isinstance(iterations, int) or iterations < 1:
        iterations = 100_000
    return sep.join([salt, str(iterations), hash_password(password, salt, iterations)])


def verify_password(password: str, stringified_password: str, sep: str = '$') -> bool:
    """
    Verify if a password matches its hashed version.

    Args:
        password (str): The password to verify
        stringified_password (str): The stored password string in format "salt$iterations$hash"
        sep (str, optional): Separator used in stringified password. Defaults to '$'.

    Returns:
        bool: True if password matches, False otherwise
    """
    salt, iterations, hashed_password = stringified_password.split(sep)
    return hashed_password == hash_password(password, salt, int(iterations))
