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
        
    def create_account_flow(self):
        # ask user to create a username with PostgreSQL user reqs
        username = input("Please enter a username: ")
        userBool = self.filter_username(username)
        pass
        # ask user to create and confirm a master password
        
        # welcome message
        
    def filter_username(self, username):
         # Check if the username starts with a letter or underscore
        if not re.match(r'^[a-zA-Z_]', username):
            print("Username must start with a letter (a-z, A-Z) or an underscore (_).")
            return False
        
        # Check if subsequent characters are letters, numbers, or underscores
        if not re.match(r'^[a-zA-Z0-9_]*$', username):
            print("Username must contain only letters, numbers, or underscores.")
            return False
        
        # Check if the length of the username is within the limit
        if len(username) > 63:
            print("Username exceeds the maximum length of 63 characters.")
            return False

        # All requirements met
        return True
        
        
        
    def login_flow(self):
        print("Logging in")
        
        
    
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