import secrets
import string

def generate_random_password(length=12):
    # Ensure the minimum length is 12
    if length < 12:
        raise ValueError("Password length must be at least 12 characters.")

    # Define character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    symbols = string.punctuation

    # Ensure at least one uppercase letter, one symbol, and one digit
    password_characters = (
        secrets.choice(uppercase_letters) +
        secrets.choice(symbols) +
        secrets.choice(digits) +
        ''.join(secrets.choice(uppercase_letters + lowercase_letters + digits + symbols) for _ in range(length - 3))
    )

    # Shuffle the characters to make the password more random
    password_list = list(password_characters)
    secrets.SystemRandom().shuffle(password_list)

    # Convert the list back to a string
    password = ''.join(password_list)

    return password
