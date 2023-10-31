from database import *

def main():
    #FIXME
    # username only works when lowercase
    # fix error messages
    db_params = {
        'host': 'localhost',
        'user': 'postgres',
        'database': 'ekeys',
        'password': 'password',
        'port': '5432'
    }
    # conn_database = "ekeys"
    # conn_user = "postgres"
    # conn_password = "password"
    # conn_host = "localhost"
    # conn_port = "5432"
    # DB_name = "my_DB"
    
    #conn = establish_conn(conn_database, conn_user, conn_password, conn_host, conn_port)
    conn = establish_conn(**db_params)    
    username = input("Please enter a username: ")
    
    create_db = False
    
    while True:
        if (check_user(username, conn)):
            masterPassword = getpass.getpass(prompt="Enter your master password: ")
            insert_ekey(username, masterPassword, conn)
            
            salt = retrieve_salt(username, conn)
            ekey = retrieve_ekey(username, conn)
            
            create_user(username, masterPassword, conn)
            print(f"User {username} created!")
            create_db = True
            break
        else:
            print("Username not available!")
            username = input("Please enter a username: ")
        
    if (create_db):
        # create database and tables for user
        create_database(username, conn)
        
        # change connection to user

        user_password_dkey = generate_derived_key(masterPassword, salt).hex()
        new_db_params = {
        'host': 'localhost',
        'user': username,
        'database': username,
        'password': user_password_dkey,
        'port': '5432'
        }
        conn = establish_conn(**new_db_params)
        
        # create tables for user
        create_table(conn)
        
    # ask user to input website 
    # retrieve rkey from dkey and ekey
    dkey = generate_derived_key(masterPassword, salt)
    rkey = decrypt_symm_key(ekey, dkey)
    
    while True:
        user_input = input("Please enter a website, or type \'done\' if done: ")
        if (user_input == 'done'):
            break
        else:
            website = encrypt_data(user_input, rkey)
            insert_website(website, conn)
    
    # print encrypted table
    sql = """SELECT * FROM credentials"""
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    print(f"Your encrypted data is: {row}")
    
    # decryption
    while True:
        masterPassword2 = getpass.getpass(prompt="Please enter your master password again to decrypt your data, or type \'done\': ")
        if (masterPassword2 == "done"):
            break
        else:
            dkey2 = generate_derived_key(masterPassword2, salt)
            rkey2 = decrypt_symm_key(ekey, dkey2)
            second_values = [item[1] for item in row]
            for enc_data in second_values:
                enc_data = hex_to_bytes(enc_data)
                # decrypt data using user input master password
                decrypted_data = decrypt_data(enc_data, rkey2)
                print(decrypted_data)
    
    conn.close()
    
if __name__ ==  "__main__":
    main()