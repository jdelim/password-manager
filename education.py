import re

class CommandHandler:
    def show_encrypt_info(self):
        pass

    def show_decrypt_info(self):
        pass


def password_suggest(password):
        # Define the criteria for a strong password
        min_length = 12
        has_digit = re.search(r"\d", password)
        has_uppercase = re.search(r"[A-Z]", password)
        has_lowercase = re.search(r"[a-z]", password)
        has_symbol = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

        # Check if the password meets the criteria
        is_strong = (
            len(password) >= min_length
            and has_digit
            and has_uppercase
            and has_lowercase
            and has_symbol
        )

        # Provide suggestions if the password is not strong
        suggestions = []
        if not has_digit:
            suggestions.append("Add at least one digit.")
        if not has_uppercase:
            suggestions.append("Add at least one uppercase letter.")
        if not has_lowercase:
            suggestions.append("Add at least one lowercase letter.")
        if not has_symbol:
            suggestions.append("Add at least one symbol.")
        if len(password) < min_length:
            suggestions.append(f"Make sure the password is at least {min_length} characters long.")

        return is_strong, suggestions
        
def check_password_strength(password):
            # Check for at least one digit
    has_digit = re.search(r'\d', password)

    # Check for at least one symbol
    has_symbol = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

    # Check for at least one uppercase letter
    has_uppercase = re.search(r'[A-Z]', password)

    # Check for at least one lowercase letter
    has_lowercase = re.search(r'[a-z]', password)

    # Check for minimum length of 12 characters
    min_length = 12
    is_length_valid = len(password) >= min_length

    # Store the results in a tuple
    results = (
        has_digit and has_symbol and has_uppercase and has_lowercase and is_length_valid,
        []
    )

    # Provide suggestions if the password is not strong
    if not has_digit:
        results[1].append("Add at least one digit.")
    if not has_uppercase:
        results[1].append("Add at least one uppercase letter.")
    if not has_lowercase:
        results[1].append("Add at least one lowercase letter.")
    if not has_symbol:
        results[1].append("Add at least one symbol.")
    if not is_length_valid:
        results[1].append(f"Make sure the password is at least {min_length} characters long.")

    return results

