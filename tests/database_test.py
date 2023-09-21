from database import *

def main():
    database = "testdb"
    user = "postgres"
    password = "password"
    host = "localhost"
    port = "5432"
    DB_name = "my_DB"
    
    conn = establish_conn(database, user, password, host, port)
    
    #create_database(DB_name, conn)
    
    create_table(conn)
    

if __name__ ==  "__main__":
    main()