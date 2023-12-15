from config import read_config
from database import *

def main():

    # NOTE: ensure that your database is set to 'postgres' or whatever default db you have!
    
    # initialize config and params
    config_params = read_config()
    
    db_params = {        
    'host': config_params['host'],
    'user': config_params['user'],
    'database': config_params['database'],
    'password': config_params['password'],
    'port': config_params['port']
}
    
    # establish connection
    conn = establish_conn(**db_params)

    # create ekey storage
    create_ekey_storage(conn)
    
    #NOTE: once successfully created, set database to 'ekeys' in database.ini

if __name__ == "__main__":
    main()