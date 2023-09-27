import psycopg2

# FIXME - will establish class later

# establish connection
def establish_conn(database, user, password, host, port):
    conn = psycopg2.connect(database = database, user = user, password = 
                            password, host = host, port = port)
    conn.autocommit = True
    return conn

# check if username is unique
# store in .JSON?

# create db based on user's username
# FIXME - usernames must be unique
def create_database(name, conn):
    # create cursor
    cursor = conn.cursor()
    
    # sql statement
    sql = f'''CREATE DATABASE {name};'''
    # execute statement
    cursor.execute(sql)
    # close connection?
    #conn.close()
    print("DB created successfully!")

def create_table(conn):
    cursor = conn.cursor()
    
    queries = (
    """
    CREATE TABLE credentials (
	    credID INTEGER PRIMARY KEY,
	    website VARCHAR(120)
    )
    """,
    """ 
    CREATE TABLE usernames (
	    userID INTEGER PRIMARY KEY,
	    username VARCHAR(50),
	    credID INTEGER,
        credID FOREIGN KEY REFERENCES credentials(credID) 
    )
    """,
    #FIXME 
    """
    CREATE TABLE passwords (
	    passID INTEGER PRIMARY KEY,
	    password VARCHAR(120),
	    userID INTEGER,
        credID INTEGER,
        userID FOREIGN KEY REFERENCES usernames(userID),
	    credID FOREIGN KEY REFERENCES credentials(credID)
    )
    """)
    #FIXME
    
    # execute queries
    for query in queries:
        cursor.execute(query)
    conn.commit()
    print("tables successfully created!")

    
    
    