from encryption import *
from database import *

def main():
    
    # prompt1 = ""
    # while prompt1 != "1":
    #     prompt1 = input("Type 1 if you want to create an account: ")
    
    # create an account
    username = input("Please create a username: ")
    password = getpass.getpass(prompt="Please create a master password: ")
    
    # establish a connection to DB
    conn_database = "ekeys"
    conn_user = "postgres"
    conn_password = "password"
    conn_host = "localhost"
    conn_port = "5432"
    conn = establish_conn(conn_database, conn_user, conn_password, conn_host, conn_port)
    
    # insert login info to database
    insert_ekey(username, password, conn)
    
    # create user's database
    #create_database(username, conn)
    
    # switch to user's DB
    #conn = establish_conn(username, conn_user, conn_password, conn_host, conn_port)
    # create tables in DB
    #create_table(conn)
    
    # ask user for website, username, and password
    # insert into tables encrypted (prob need to create a func)
    
    # retrieve encrypted info from tables, then decrypt to show the user
    print(f"User {username} created!")
        
    # login to account
    # elif (prompt1 == "2"):
    #     username = input("Please enter your username: ")
    #     password = getpass.getpass(prompt="Please enter your master password: ")
        

if __name__ == "__main__":
    main()