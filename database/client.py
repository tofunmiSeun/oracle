from pymongo.mongo_client import MongoClient
from pymongo.database import Database
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('MONGODB_URI')
# Todo: fix TLS certificate validation
mongo_client = MongoClient(uri, tlsAllowInvalidCertificates=True)
mongo_database: Database = mongo_client.oracle

try:
    mongo_client.admin.command('ping')
except Exception as e:
    print(e)
