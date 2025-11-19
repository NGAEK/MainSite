import yaml
import os


class DatabaseConfig:
    def __init__(self, host, port, user, password, name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.name = name


class ServerConfig:
    def __init__(self, port):
        self.port = port


class Config:
    def __init__(self, database, server):
        self.database = database
        self.server = server


def load_config(path="config.yml"):
    """Загружает конфигурацию из YAML файла"""
    with open(path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    
    db_config = DatabaseConfig(
        host=data['database']['host'],
        port=data['database']['port'],
        user=data['database']['user'],
        password=data['database']['password'],
        name=data['database']['name']
    )
    
    server_config = ServerConfig(
        port=data['server']['port']
    )
    
    config = Config(db_config, server_config)
    
    if not config.database.password:
        print("Внимание: используется пустой пароль для базы данных")
    
    return config

