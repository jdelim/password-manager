import re

class CommandHandler:
    def show_encrypt_info(self): # explains encryption process
        pass

    def show_decrypt_info(self): # explains decryption process
        pass

    def password_explain(self): # explains importance of strong passwords
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

    # Print suggestions if the password is not strong
    if not has_digit:
        print("Add at least one digit.")
    if not has_uppercase:
        print("Add at least one uppercase letter.")
    if not has_lowercase:
        print("Add at least one lowercase letter.")
    if not has_symbol:
        print("Add at least one symbol.")
    if not is_length_valid:
        print(f"Make sure the password is at least {min_length} characters long.")

    # Return True if all requirements are met, False otherwise
    return has_digit and has_symbol and has_uppercase and has_lowercase and is_length_valid

if __name__ == "__main__":
    #check_password_strength("Test1233412124!!!!!")
    pass