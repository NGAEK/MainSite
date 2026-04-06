import yaml
import os
from dotenv import load_dotenv


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
    def __init__(self, database, server, admin_api_key: str = "", site=None):
        self.database = database
        self.server = server
        self.admin_api_key = admin_api_key or ""
        self.site = site if isinstance(site, dict) else {}


def load_config(path="config.yml"):
    """Загружает конфигурацию из YAML файла"""
    load_dotenv()
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

    admin_key = ""
    if isinstance(data.get("admin_api"), dict):
        admin_key = str(data["admin_api"].get("key") or "")
    admin_key = os.environ.get("NGAEK_ADMIN_API_KEY", "").strip() or admin_key

    site = {}
    if isinstance(data.get("site"), dict):
        site = data["site"]

    config = Config(db_config, server_config, admin_key, site)
    
    if not config.database.password:
        print("Внимание: используется пустой пароль для базы данных")
    
    return config

