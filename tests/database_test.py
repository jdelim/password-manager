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
    
    create_db = False
    
    if (check_user(username, conn)):
        masterPassword = input("Please enter a password: ")
        insert_ekey(username, masterPassword, conn)
        #salt = retrieve_salt(username, conn)
        create_user(username, masterPassword, conn)
        print(f"User {username} created!")
        create_db = True
    if (check_user(username, conn) == False):
        print("Username not available!")
        
    if (create_db):
        

    
    
    # check if username is unique in database
    # if (check_user(username, conn)):
    #     myPassword = input("Please enter a password: ")
    #     insert_ekey(username, myPassword, conn)
    # else:
    #     print("Username already taken!")
    
    
    
    #insert_ekey(username, myPassword, conn)
    
if __name__ ==  "__main__":
    main()