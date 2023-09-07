import psycopg2

# FIXME - will establish class later

# establish connection
def establish_conn(database, user, password, host, port):
    conn = psycopg2.connect(database = database, user = user, password = 
                            password, host = host, port = port)
    conn.autocommit = True
    
# check if username is unique
# store in .JSON?

# create db based on user's username
# FIXME - usernames must be unique
def create_database(name):
    


def create_table():
    
    