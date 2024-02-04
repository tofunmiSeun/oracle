import pymongo
import loaded_env_variables
from database.service import DatabaseService


uri = loaded_env_variables.MONGODB_URI
# Todo: fix TLS certificate validation
mongo_client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)

try:
    mongo_client.admin.command('ping')
except Exception as e:
    print(e)

db_service = DatabaseService(mongo_client.oracle)
