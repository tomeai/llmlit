import databases

from settings import settings as mysql_settings

# account库
ACCOUNT_DATABASE_URL = f'mysql+aiomysql://{mysql_settings.MYSQL_USERNAME}:{mysql_settings.MYSQL_PASSWORD}@{mysql_settings.MYSQL_HOST}:{mysql_settings.MYSQL_PORT}/ai'
account_database = databases.Database(ACCOUNT_DATABASE_URL, min_size=1, max_size=10)


def get_account_database():
    return account_database
