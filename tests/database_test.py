from database import *

def main():
    database = "ekeys"
    user = "postgres"
    password = "password"
    host = "localhost"
    port = "5432"
    DB_name = "my_DB"
    
    conn = establish_conn(database, user, password, host, port)
        
    #create_ekey_storage(conn)
    
    username = input("Please enter a username: ")
    myPassword = input("Please enter a password: ")
    
    insert_ekey(username, myPassword, conn)
    
if __name__ ==  "__main__":
    main()