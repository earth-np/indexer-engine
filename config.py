import os

class Config:
    DEBUG = False
    TESTING = False
    DATABASE = 'balances.db'
    INTERVAL = 2  # seconds
    START_BLOCK = 12157952
    WINDOW_SIZE = 1000
    TOKEN_ADDRESS= "0x80B3214b38A233FFbd061273C2598B049025f397"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True
    DATABASE = 'test_balances.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def get_config():
    return config[os.getenv('FLASK_ENV', 'development')]