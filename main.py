from encryption import *
from database import *
from ui import *
from education import *

def main():
    pwManager = PasswordManagerCLI()
    
    # set up conn to postgres
    db_params = {        
        'host': 'localhost',
        'user': 'postgres',
        'database': 'ekeys',
        'password': 'password',
        'port': '5432'
    }
    
    conn = establish_conn(**db_params)
    
    # list options
    while True:
        print("\nOptions:")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        # FIXME put show all commands command
        
        choice = input("Enter your choice (1, 2, or 3): ")
        
        if choice == "1":
            print("Usernames must only contain numbers, letters, or underscores, and must start with a letter or underscore.")

            # username creation
            while True:
                username = input("Please enter a username: ")
                
                validUser = pwManager.filter_username(username)
                uniqueUser = check_user(username, conn)
                
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
                    
                    # create an ekey
                    ekey = encrypt_symm_key(rkey, dkey)                    
                    
                    # create postgres user, database, and tables (postgres user)
                    create_user(username, dkey, conn)
                    create_database(username, conn)
                    
                    # use user conn before creating tables
                    user_db_params = {        
                        'host': 'localhost',
                        'user': username,
                        'database': username,
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
            break   
        elif choice == "3":
            print("Exiting. Goodbye!")
            break
    

if __name__ == "__main__":
    main()