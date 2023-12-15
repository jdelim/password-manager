from encryption import *
from database import *
from ui import *
from education import *
from password_generation import *

def main():
    pwManager = PasswordManagerCLI()
    myCommands = CommandHandler()
    
    # set up conn to postgres
    db_params = {        
        'host': 'localhost',
        'user': 'postgres',
        'database': 'ekeys',
        'password': 'password',
        'port': '5432'
    }
    
    conn = establish_conn(**db_params)
    login = False
    
    # list options
    while (login is False):
        print("\nOptions:")
        print("1. Create Account")
        print("2. Login")
        print("/h to show other commands")
        print("q. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("Usernames must only contain numbers, letters, or underscores, and must start with a letter or underscore.")

            # username creation
            while True:
                username = input("Please enter a username: ")
                
                validUser = pwManager.filter_username(username)
                uniqueUser = check_user(username, conn)
                
                if (uniqueUser is False):
                    print("Username must be unique!")
                
                if (validUser == True) and (uniqueUser == True):
                    print("Username is valid!")
                    break
                
            # master password creation
            print("Your master password should be at least 12 characters, with at least 1 uppercase and lowercase letter, 1 symbol, and 1 digit.")
            while True:
                
                m_password = getpass.getpass(prompt="Please enter a master password: ")
                
                # check master password strength
                
                if (check_password_strength(m_password) is True):
                
                    # generate rkey, dkey, ekey, and salt values
                    rkey = generate_random_key()
                    
                    # insert ekey, username, password. salt is stored too
                    insert_ekey(username, m_password, conn) # salt is generated and stored here
                    
                    # retrieve salt from table to use for dkey
                    salt = retrieve_salt(username, conn)
                    dkey = generate_derived_key(m_password, salt)                
                    
                    # create postgres user, database, and tables (postgres user)
                    create_user(username, dkey, conn)
                    create_database(username, conn)
                    
                    
                    # use user conn before creating tables
                    user_db_params = {        
                        'host': 'localhost',
                        'user': username.lower(),
                        'database': username.lower(),
                        'password': dkey.hex(),
                        'port': '5432'
                    }
                    user_conn = establish_conn(**user_db_params)
                    create_table(user_conn) # user can create tables since he is the owner of database
                    
                    print("Account created!")
                    break
                else:
                    print("\nPlease enter a valid master password!")
            
        elif choice == "2":
            while True:    
                # prompt for username
                username = input("Please enter your username: ")
                usernameValid = check_user(username, conn) # boolean
                if (usernameValid is True):
                    print("\nUsername does not exist!")
                    break
                # prompt for password
                master_password = getpass.getpass(prompt="Please enter your master password: ")
                # stored_ekey = retrieve_ekey(username, conn)
                # stored_ekey = hex_to_bytes(stored_ekey) # convert from table
                # use derived key to attempt login
                stored_salt = retrieve_salt(username, conn) # did not need to do hex to bytes here idk why

                attempt_dkey = generate_derived_key(master_password, stored_salt)
                
                # attempt login to postgres user 
                try:
                    user_db_params = {        
                        'host': 'localhost',
                        'user': username.lower(),
                        'database': username.lower(),
                        'password': attempt_dkey.hex(),
                        'port': '5432'
                    }
                    user_conn = establish_conn(**user_db_params)
                    login = True # to break out of outer while loop
                    break # break out of inner while loop
                except psycopg2.Error as e:
                    print("\nInvalid master password!")
                    break
                
        elif choice == "/h":
            myCommands.show_all_commands()
        elif choice == "q":
            print("\nExiting. Goodbye!")
            exit(1)
        elif (myCommands.commands(choice)):
            continue
        else:
            print("\nInvalid choice!")
            
            
    # login flow
    print("\nLogin successful!")
    
    while True:
        print(f"\nWelcome {username}!")
        print("1. Add a password")
        print("2. Generate a random password")
        print("3. Display passwords")
        print("4. Edit a credential")
        print("5. Delete a credential")
        print("/h for more commands")
        print("q. Log out")
        
        choice2 = input("\nPlease select a choice: ")
            # retrieve info from ekeys table
        db_params = {        
            'host': 'localhost',
            'user': 'postgres',
            'database': 'ekeys',
            'password': 'password',
            'port': '5432'
        }
        
        conn = establish_conn(**db_params)
        salt = retrieve_salt(username, conn)
        ekey = retrieve_ekey(username, conn)
        dkey = generate_derived_key(master_password, salt)
        rkey = decrypt_symm_key(ekey, dkey)
            
        if choice2 == "1":

            # establish user conn
            user_db_params = {        
                'host': 'localhost',
                'user': username.lower(),
                'database': username.lower(),
                'password': dkey.hex(),
                'port': '5432'
            }
            
            user_conn = establish_conn(**user_db_params)
            
            # ask for website
            website = input("Please enter the name of the website for your password: ")
            enc_website = encrypt_data(website, rkey)
            credID = insert_website(enc_website, user_conn)
            
            # ask for username
            table_username = input("Please enter the username for the website: ")
            enc_username = encrypt_data(table_username, rkey)
            userID = insert_username(enc_username, credID, user_conn)
            
            # ask for password
            table_password = input("Please enter the password for your entered username: ")
            enc_password = encrypt_data(table_password, rkey)
            insert_password(enc_password, credID, userID, user_conn)
            
            print(f"Password for user {table_username} in website {website} created!")
            
        elif choice2 == "2": # generate random password
            print()
            random_pass = generate_random_password(12)
            print(f"Your random password is: {random_pass}")
            
        elif choice2 == "3": # display passwords
            print()
            fetched_info = fetch_and_decrypt_data(rkey, user_conn)
            display_credentials_info(fetched_info)
            
        elif choice2 == "4": # edit a cred
            print()
            edit_credentials(rkey, user_conn)
            
        elif choice2 == "5": # delete a cred
            print()
            delete_credentials(rkey, user_conn)
        
        elif choice2 == "/h":
            myCommands.show_all_commands()
            
        elif (myCommands.commands(choice2)):
            continue
        
        elif choice2 == "q":
            print("Logging out...")
            exit(1)
            
        else:
            print("Invalid choice!")
            
        

if __name__ == "__main__":
    main()