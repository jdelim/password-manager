from encryption import *
from database import *

def main():
    db_params = {        
        'host': 'localhost',
        'user': 'postgres',
        'database': 'ekeys',
        'password': 'password',
        'port': '5432'
    }
    conn = establish_conn(**db_params)
    salt = retrieve_salt("Banana_fan888", conn)
    ekey = retrieve_ekey("Banana_fan888", conn)
    dkey = generate_derived_key("Nutella034200!", salt)
    rkey = decrypt_symm_key(ekey, dkey)
    
    #establish conn
    db_params = {        
        'host': 'localhost',
        'user': 'banana_fan888',
        'database': 'banana_fan888',
        'password': dkey.hex(),
        'port': '5432'
    }
    conn = establish_conn(**db_params)
    
    # ask for website
    website = input("Please enter a website: ")
    enc_website = encrypt_data(website, rkey)
    credID = insert_website(enc_website, conn)
    
    # ask for username
    username = input("Please enter a username: ")
    enc_username = encrypt_data(username, rkey)
    userID = insert_username(enc_username, credID, conn)
    
    # ask for password
    password = input("Enter a password: ")
    enc_password = encrypt_data(password, rkey)
    insert_password(enc_password, credID, userID, conn)
    
    fetched_info = fetch_and_decrypt_data(rkey, conn)
    
    display_credentials_info(fetched_info)
    
if __name__ == "__main__":
    main()