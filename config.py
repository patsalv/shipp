import os
from dotenv import load_dotenv
# from cryptography.fernet import Fernet


class Config:

    DEBUG = False
    TESTING = False
    # Default application db
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLITE_URL')
    # Mounted pi-hole db
    SQLALCHEMY_BINDS = {
        "pihole": os.getenv('PIHOLE_DB_URL')
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PIHOLE_DB_URL = os.getenv('PIHOLE_DB_URL')
    PIHOLE_AUTH_TOKEN = os.getenv('PIHOLE_AUTH_TOKEN')
    INFLUXDB_URL = os.getenv('INFLUXDB_URL')
    INFLUXDB_AUTH_TOKEN = os.getenv('INFLUXDB_AUTH_TOKEN')
    INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')
    INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
    SCHEDULER_TIMEINTERVAL = 3600


class DevelopmentConfig(Config):
    DEBUG = True

    def __init__(self):
        super().__init__()
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)


class ProductionConfig(Config):
    pass


class TestConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}
