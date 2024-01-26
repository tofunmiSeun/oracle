import pymongo
from pymongo.database import Database
import os
from dotenv import load_dotenv
from database.service import DatabaseService

load_dotenv()

uri = os.getenv('MONGODB_URI')
# Todo: fix TLS certificate validation
mongo_client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
mongo_database: Database = mongo_client.oracle

try:
    mongo_client.admin.command('ping')
except Exception as e:
    print(e)

db_service = DatabaseService(mongo_database)
