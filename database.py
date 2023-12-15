import psycopg2
import bcrypt
from encryption import *

# establish connection
def establish_conn(database, user, password, host, port):
    conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
    conn.autocommit = True
    return conn

# check if username is unique, returns bool. unique = true
def check_user(username, conn):
    cursor = conn.cursor()
    user_tuple = (username,)
    query = """SELECT username FROM ekeys WHERE username = %s"""
    
    cursor.execute(query, user_tuple)
    row = cursor.fetchone() # ('test@gmail.com',) returns a tuple
    # return true if row is None, meaning that username is unique
    if (row is None):
        return True
    elif (len(row) == 1):
        #print("Username must be unique!")
        return False
    
def hex_to_bytes(hex): # use this when retrieving from postgres table
    hex = hex[2:]
    toBytes = bytes.fromhex(hex)
    return toBytes
    
def retrieve_ekey(username, conn):
    cursor = conn.cursor()
    myTuple = (username,)
    
    query = """SELECT ekey FROM ekeys WHERE username = %s"""
    
    cursor.execute(query, myTuple)
    row = cursor.fetchone()
    
    if row is None:
        return None
    else:
        ekey = ''
        for item in row:
            ekey = ekey + item
        ekey = hex_to_bytes(ekey)
        return ekey
        
def retrieve_salt(username, conn):
    cursor = conn.cursor()
    myTuple = (username,)
    
    query = """SELECT salt FROM ekeys WHERE username = %s"""
    
    cursor.execute(query, myTuple)
    row = cursor.fetchone()
    
    if row is None:
        return None
    else:
        salt = ''
        for item in row:
            salt = salt + item
        salt = salt[2:] #remove \x
        #print(f"Salt is: {salt}")
        salt = bytes.fromhex(salt) #convert hexadecimal to bytes
        #print(f"Bytes salt is: {salt}")
        return salt
    
def create_user(username, dkey, conn):
    cursor = conn.cursor()
    
    # retrieve salt
    #salt = retrieve_salt(username, conn)
    
    # get dkey
    #dkey = generate_derived_key(mPassword, salt)
    
    # change to hexadecimal
    dkey_hex = dkey.hex()
    
    # execute query
    query = f"CREATE USER {username} WITH PASSWORD \'{dkey_hex}\'"
    #query = "CREATE USER %s WITH PASSWORD %s"
    cursor.execute(query)
    conn.commit()
    

# create db based on user's username

def create_database(name, conn):
    # create cursor
    cursor = conn.cursor()
    
    # tuple
    name_tuple = (name, name)
    
    # sql statement
    sql = f'''CREATE DATABASE {name} WITH OWNER {name}'''
    #sql = """CREATE DATABASE (%s) WITH OWNER (%s)"""
    # execute and commit statement
    cursor.execute(sql)
    conn.commit()
    #print("DB created successfully!")

def create_table(conn):
    cursor = conn.cursor()
    
    queries = (
    """
    CREATE TABLE credentials (
	    credID SERIAL PRIMARY KEY,
	    website VARCHAR(500)
    )
    """,
    """ 
    CREATE TABLE usernames (
	    userID SERIAL PRIMARY KEY,
	    username VARCHAR(500),
	    credID INTEGER,
        FOREIGN KEY (credID) REFERENCES credentials(credID) 
    )
    """,
    
    """
    CREATE TABLE passwords (
	    passID SERIAL PRIMARY KEY,
	    password VARCHAR(500),
	    userID INTEGER,
        credID INTEGER,
        FOREIGN KEY (userID) REFERENCES usernames(userID),
	    FOREIGN KEY (credID) REFERENCES credentials(credID)
    )
    """)
    
    # execute queries
    for query in queries:
        cursor.execute(query)
    conn.commit()
    #print("tables successfully created!")
    
# create DB that stores usernames and EKEYS
def create_ekey_storage(conn):
    cursor = conn.cursor()
    
    query = """CREATE TABLE ekeys (
        username VARCHAR(500) PRIMARY KEY,
        ekey VARCHAR(500),
        salt VARCHAR(500)
    )
        """
    cursor.execute(query)
    conn.commit()
    print("ekey storage created successfully!")
    
def insert_ekey(username, password, conn):
    cursor = conn.cursor()
    
    # generate salt to store
    salt = bcrypt.gensalt()
    #print(f"salt in insertekey func is: {salt}")
    # generate rkey to store as ekey
    rkey = generate_random_key()
    # get dkey from masterpassword
    dkey = generate_derived_key(password, salt)
    ekey = encrypt_symm_key(rkey, dkey)
    
    myItems = (username, ekey, salt)
    #print(f"myItems tuples are: {myItems}")
    sql = """INSERT INTO ekeys (
        username, ekey, salt) VALUES (%s, %s, %s)"""
    
    cursor.execute(sql, myItems)
    
    conn.commit()

def list_websites(conn):
    cursor = conn.cursor()
    query = """SELECT website FROM credentials"""
    
    cursor.execute(query)
    row = cursor.fetchall()
    
    return row

def find_website(listOfTuples, website):
    #cursor = conn.cursor()
    #myTuple = (website,)
    #query = """SELECT website FROM credentials WHERE website = %s"""
    
    for myTuple in listOfTuples:
        value = myTuple[0]
        if value == website:
            return value
    return None

def insert_website(website, conn):
    cursor = conn.cursor()
    website_tuple = (website,)
    
    sql = """ INSERT INTO credentials (
        website) VALUES (%s) RETURNING credID"""
    
    cursor.execute(sql, website_tuple)
    cred_id = cursor.fetchone()[0]
    conn.commit()
    return cred_id

def insert_username(username, credID, conn):
    cursor = conn.cursor()
    
    username_tuple = (username, credID)
    
    sql = """INSERT INTO usernames (
            username, credID) VALUES (%s, %s) RETURNING userID"""

    cursor.execute(sql, username_tuple)
    user_id = cursor.fetchone()[0]
    conn.commit()
    return user_id

def insert_password(password, credID, userID, conn):
    cursor = conn.cursor()
    
    password_tuple = (password, credID, userID)
    
    sql = """INSERT INTO passwords (
        password, userID, credID) VALUES (%s, %s, %s)"""
    
    cursor.execute(sql, password_tuple)
    conn.commit()
    
def fetch_and_decrypt_data(rkey, conn):
    query = """
        SELECT c.credID, c.website, u.username, p.password
        FROM credentials c
        LEFT JOIN usernames u ON c.credID = u.credID
        LEFT JOIN passwords p ON u.userID = p.userID
        ORDER BY c.credID, u.userID;
    """

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            credentials_info = {}

            for row in rows:
                credID, website, username, password = row
                if credID not in credentials_info:
                    website = hex_to_bytes(website)
                    credentials_info[credID] = {'website': decrypt_data(website, rkey), 'usernames': []}

                if username and password:
                    username = hex_to_bytes(username)
                    password = hex_to_bytes(password)
                    decrypted_username = decrypt_data(username, rkey)
                    decrypted_password = decrypt_data(password, rkey)
                    credentials_info[credID]['usernames'].append({'username': decrypted_username, 'password': decrypted_password})

            return credentials_info
        
    except psycopg2.Error as e:
        print(f"Error executing SQL query: {e}")
        return None
    
def display_credentials_info(credentials_info):
    if not credentials_info:
        print("No data to display.")
        return

    for credID, data in credentials_info.items():
        print(f"{credID}. Website: {data['website']}")
        for user_data in data['usernames']:
            print(f"  Username: {user_data['username']}, Password: {user_data['password']}\n")

def edit_credentials(rkey, conn):
    # display current credentials
    current_credentials = fetch_and_decrypt_data(rkey, conn)
    display_credentials_info(current_credentials)
    
    try:
        # ask user to select a credID to edit
        selected_credID = int(input("Please select a credential number to edit, or 'q' to go back: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return
    
    # query to check if the entered credID exists in the credentials table
    check_cred_query = "SELECT 1 FROM credentials WHERE credID = %s LIMIT 1;"
    
    try:
        with conn.cursor() as cursor:
            # execute the query with the selected_credID
            cursor.execute(check_cred_query, (selected_credID,))
            
            # fetchone returns None if no match is found
            cred_exists = cursor.fetchone() is not None

            # if credID exists, proceed with the edit
            if cred_exists:
                # Rest of the code...
                new_website = input("Enter a new website: ")
                new_username = input("Enter a new username: ")
                new_password = input("Enter new password: ")

                # encrypt data
                enc_website = encrypt_data(new_website, rkey)
                enc_username = encrypt_data(new_username, rkey)
                enc_password = encrypt_data(new_password, rkey)

                # update database query
                update_query = """
                    UPDATE credentials SET website = %s WHERE credID = %s;
                    UPDATE usernames SET username = %s WHERE credID = %s;
                    UPDATE passwords SET password = %s WHERE userID IN (SELECT userID FROM usernames WHERE credID = %s);
                """

                with conn.cursor() as cursor:
                    cursor.execute(update_query, (enc_website, selected_credID, enc_username, selected_credID, enc_password, selected_credID))
                    conn.commit()

                print("Credentials successfully updated!")

            else:
                print("Invalid credential number selected!")

    except psycopg2.Error as e:
        print(f"Error executing SQL query: {e}")
        
def delete_credentials(rkey, conn):
    # display credentials
    current_credentials = fetch_and_decrypt_data(rkey, conn)
    display_credentials_info(current_credentials)
    
    try: 
        # ask user for credID
        credID_to_delete = int(input("Please select a credential number to delete, or 'q' to go back: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return
    
    # Check if credID is valid
    check_query = """
        SELECT COUNT(*) FROM credentials WHERE credID = %s;
    """
    
    with conn.cursor() as cursor:
        cursor.execute(check_query, (credID_to_delete,))
        count = cursor.fetchone()[0]
        
    if count > 0: # credID exists
        # Delete from passwords and usernames first
        delete_query_passwords = """
            DELETE FROM passwords WHERE userID IN (SELECT userID FROM usernames WHERE credID = %s);
        """
        
        delete_query_usernames = """
            DELETE FROM usernames WHERE credID = %s;
        """

        with conn.cursor() as cursor:
            cursor.execute(delete_query_passwords, (credID_to_delete,))
            cursor.execute(delete_query_usernames, (credID_to_delete,))
            conn.commit()

        # Then delete from credentials
        delete_query_credentials = """
            DELETE FROM credentials WHERE credID = %s;
        """

        with conn.cursor() as cursor:
            cursor.execute(delete_query_credentials, (credID_to_delete,))
            conn.commit()

        print(f"Credential with cred_id {credID_to_delete} deleted successfully!")

        
    else:
        print("Invalid credential number or credential not found!")
    