import re
import getpass

class PasswordManagerCLI:
    def __init__(self):
        print(r"""
              
   /\                                                        /\
  |  |                                                      |  |
 /----\                 Welcome to your                    /----\
[______]               Password Manager!                  [______]
 |    |         _____                        _____         |    |
 |[]  |        [     ]                      [     ]        |  []|
 |    |       [_______][ ][ ][ ][][ ][ ][ ][_______]       |    |
 |    [ ][ ][ ]|     |  ,----------------,  |     |[ ][ ][ ]    |
 |             |     |/'    ____..____    '\|     |             |
  \  []        |     |    /'    ||    '\    |     |        []  /
   |      []   |     |   |o     ||     o|   |     |  []       |
   |           |  _  |   |     _||_     |   |  _  |           |
   |   []      | (_) |   |    (_||_)    |   | (_) |       []  |
   |           |     |   |     (||)     |   |     |           |
   |           |     |   |      ||      |   |     |           |
 /''           |     |   |o     ||     o|   |     |           ''\
[_____________[_______]--'------''------'--[_______]_____________]""")
        
    def create_account(self):
        print("Creating a new account")
        
        
    def login(self):
        print("Logging in")
        
    def password_suggest(self, password):
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
        
    def check_password_strength(self, password):
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
        
    
if __name__ == "__main__":
    myPWManager = PasswordManagerCLI()
    
    while True:
        print("\nOptions:")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            myPWManager.create_account()
            usr = input("Enter a username: ")
            while True:
                pwd = getpass.getpass("\nEnter a master password: ")
                print(f"Your master password is: {pwd}")
                if (myPWManager.check_password_strength(pwd)):
                    print("Account created!")
                    break
                else:
                    print("\nPlease retype your password!")
        elif choice == "2":
            myPWManager.login()
            print("Login successful!")
            while True:
                password = getpass.getpass("\nPlease enter a password, or type 'done': ")
                is_strong, suggestions = myPWManager.check_password_strength(password)
                
                if (password == "done"):
                    break
                elif is_strong:
                    print(f"Your password {password} is strong!")
                else:
                    print(f"Your password \"{password}\" is weak, consider the following:")
                    for suggestion in suggestions:
                        print(f"- {suggestion}")
        elif choice == "3":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")