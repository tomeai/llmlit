import os

import databases

# account库
ACCOUNT_DATABASE_URL = os.getenv("ACCOUNT_DATABASE_URL",
                            "mysql+aiomysql://root:A1n9Z*+6S-_wF05J2i@10.6.16.191:31501/ai")
account_database = databases.Database(ACCOUNT_DATABASE_URL, min_size=1, max_size=10)


def get_account_database():
    return account_database
