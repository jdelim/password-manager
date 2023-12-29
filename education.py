import re

class CommandHandler:
    def show_all_commands(self): # /h
        print("\nCommands list:")
        print("Type /h to show all commands.")
        print("Type /encryption to find out more about the encryption process.")
        print("Type /db to find out more about how database interaction works.")
        print("Type /passwords to find out more about the importance of strong passwords.")
    
    def acc_create_and_login(self): # explains encryption process for master password
        info1 = """\nWhen a user creates an account, a randomly generated symmetric key (RKEY) is created
        alongside with the account. This RKEY is used to encrypt and decrypt the user's data,
        has no connection to the user's master password, and is never stored inside the database.
        """
        
        info2 = """\nA key is then derived from the user's master password (DKEY) which is then used
        to encrypt the RKEY. This gives us the encrypted symmetric key (EKEY).
        """
        info3 = """\nThe EKEY is stored alongside with the username. So, the next time a user logs in,
        their EKEY is retrieved, and a DKEY is generated from the password they enter. The DKEY and
        EKEY are put through a decryption function, and, if the user has entered the correct master password,
        the correct RKEY will be generated from the decryption function granting the user access to their
        data.
        """
        print(info1)
        print(info2)
        print(info3)
        
    def db_explain(self):
        info1 = """\nEach user has a database comprised of 3 tables: the table that stores the websites, the usernames,
        and the passwords. All data stored in the database is encrypted.
        Even the developer cannot retrieve plain-text values from the database.
        Therefore, it is imperative that you do not lose access to your master password as there is no way to retrieve it if lost.
        """
        print(info1)

    def password_explain(self): # explains importance of strong passwords
        info1 = """\nThe longer the password and the utilization of upper and lowercase letters, numbers,
        and symbols make a password extremely difficult to brute force.
        For instance, a 12 character password composed only of lowercase letters will take 14 hours to brute force.
        However, a 12 character password with lowercase, uppercase, numbers, and symbols will take 226 years to brute force!
        """
        print(info1)
    
    def commands(self, input):
        if input == "/h":
            self.show_all_commands()
            return True
        elif input == "/encryption":
            self.acc_create_and_login()
            return True
        elif input == "/db":
            self.db_explain()
            return True
        elif input == "/passwords":
            self.password_explain()
            return True
        else:
            return False
    
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
