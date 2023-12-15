import configparser

def read_config(file_path='database.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['postgresql']