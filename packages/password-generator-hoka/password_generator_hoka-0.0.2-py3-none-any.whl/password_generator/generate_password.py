import random
import string


def generate_password(length=12, use_digits=True, use_uppercase=True, use_special_chars=True):
    """
    Generate a random secure password.

    Args:
        length (int): Length of the password.
        use_digits (bool): Whether to include digits.
        use_uppercase (bool): Whether to include uppercase letters.
        use_special_chars (bool): Whether to include special characters.

    Returns:
        str: The generated password.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    # Define character pools
    lower_chars = string.ascii_lowercase
    upper_chars = string.ascii_uppercase if use_uppercase else ""
    digits = string.digits if use_digits else ""
    special_chars = string.punctuation if use_special_chars else ""

    if not (lower_chars + upper_chars + digits + special_chars):
        raise ValueError("At least one character set must be enabled.")

    # Ensure the password contains at least one character from each enabled set
    all_chars = lower_chars + upper_chars + digits + special_chars
    password = [
        random.choice(lower_chars),
        random.choice(upper_chars) if use_uppercase else random.choice(lower_chars),
        random.choice(digits) if use_digits else random.choice(lower_chars),
        random.choice(special_chars) if use_special_chars else random.choice(lower_chars)
    ]

    # Fill the rest of the password length with random choices from all enabled sets
    password += random.choices(all_chars, k=length - len(password))
    random.shuffle(password)

    return ''.join(password)
