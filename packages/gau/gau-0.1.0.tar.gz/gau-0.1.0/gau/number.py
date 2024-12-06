def is_palindrome(x: int) -> bool:
    """
    Check if a given number is a palindrome.

    Parameters:
        x (int): The number to be checked for palindrome property.

    Returns:
        bool: True if the number is a palindrome, False otherwise.
    """
    if x < 10 and x >= 0:
        return True
    if x < 0:
        return False
    chars = [a for a in str(x)]
    l = len(chars)
    i = 0
    j = l - 1
    while i < j:
        if chars[i] != chars[j]:
            return False
        i += 1
        j -= 1
    return True
