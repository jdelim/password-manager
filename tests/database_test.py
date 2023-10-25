from database import *

def main():
    conn_database = "ekeys"
    conn_user = "postgres"
    conn_password = "password"
    conn_host = "localhost"
    conn_port = "5432"
    DB_name = "my_DB"
    
    conn = establish_conn(conn_database, conn_user, conn_password, conn_host, conn_port)
        
    
    username = input("Please enter a username: ")
    
    # check if username is unique in database
    check_user(username, conn)
    
    #myPassword = input("Please enter a password: ")
    
    
    
    #insert_ekey(username, myPassword, conn)
    
if __name__ ==  "__main__":
    main()