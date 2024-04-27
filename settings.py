import os

from dotenv import load_dotenv

load_dotenv()

storage_path = os.getcwd() + '/storage'
taxonomy_path = storage_path + '/taxonomy'
description_path = storage_path + '/descriptions'

db_database = os.getenv('DB_DATABASE')
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT', '5432')
db_host = os.getenv('DB_HOST', 'postgres')

db_connection = {
    'dbname': db_database,
    'user': db_user,
    'port': db_port,
    'password': db_password,
    'host': db_host
}

SAMPLES_TABLE_NAME = 'samples'
TAXONOMY_TABLE_NAME = 'taxonomy'
RANKS_TABLE_NAME = 'ranks'
DESCRIPTIONS_TABLE_NAME = 'descriptions'

DEFAULT_TAXONOMY = ['silva', 'gtdb', 'gg2']
DEFAULT_SAMPLES = ['Sea plant', 'Sea soil', 'Sea water']
