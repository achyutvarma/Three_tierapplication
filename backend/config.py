import os

DB_HOST = os.getenv('DB_HOST', 'rds-endpoint')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'passwrd')
DB_NAME = os.getenv('DB_NAME', 'databasename created inside rds')
