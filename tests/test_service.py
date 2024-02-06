import unittest
import mongomock
from database.service import DatabaseService
from bson import ObjectId


class TestDatabaseService(unittest.TestCase):

    def test_create_workspace(self):
        db = mongomock.MongoClient()['database']
        service = DatabaseService(db)
        workspace_id = service.create_workspace('AI assistant', '')

        self.assertEqual(1, service.workspace_collection.count_documents(
            {'_id': ObjectId(workspace_id)}))


if __name__ == '__main__':
    unittest.main()
