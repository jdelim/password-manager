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
        print("Creating a new account")
        
        
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