import psycopg2
import bcrypt
from encryption import *

# FIXME - will establish class later

# establish connection
def establish_conn(database, user, password, host, port):
    conn = psycopg2.connect(database = database, user = user, password = 
                            password, host = host, port = port)
    conn.autocommit = True
    return conn

# check if username is unique, returns bool
def check_user(username, conn):
    cursor = conn.cursor()
    query = """SELECT username FROM ekeys WHERE username = '%s'"""
    
    print(cursor.execute(query, username))
    

# create db based on user's username

def create_database(name, conn):
    # create cursor
    cursor = conn.cursor()
    
    # sql statement
    sql = f'''CREATE DATABASE {name};'''
    # execute and commit statement
    cursor.execute(sql)
    conn.commit()
    print("DB created successfully!")

def create_table(conn):
    cursor = conn.cursor()
    
    queries = (
    """
    CREATE TABLE credentials (
	    credID INTEGER PRIMARY KEY,
	    website VARCHAR(500)
    )
    """,
    """ 
    CREATE TABLE usernames (
	    userID INTEGER PRIMARY KEY,
	    username VARCHAR(500),
	    credID INTEGER,
        FOREIGN KEY (credID) REFERENCES credentials(credID) 
    )
    """,
    
    """
    CREATE TABLE passwords (
	    passID INTEGER PRIMARY KEY,
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
    print("tables successfully created!")
    
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
    # generate rkey to store as ekey
    rkey = generate_random_key();
    # get dkey from masterpassword
    dkey = generate_derived_key(password, salt)
    ekey = encrypt_symm_key(rkey, dkey)
    
    myItems = (username, ekey, salt)
    
    sql = """INSERT INTO ekeys (
        username, ekey, salt) VALUES (%s, %s, %s)"""
    
    cursor.execute(sql, myItems)
    
    conn.commit()
    
def insert_website(website, conn):
    cursor = conn.cursor()
    
    sql = """ INSERT INTO credentials (
        website) VALUES (%s)"""
    pass

def insert_username(username, conn):
    pass

def insert_password(password, conn):
    pass
    

    
    
    