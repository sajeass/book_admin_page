import pymongo
from pymongo import MongoClient, UpdateOne
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from bson import ObjectId

class MongoDB:
    def __init__(self, uri=None):
        self.client = None
        self.db = None
        self.uri = uri or "mongodb+srv://aboutb:jEEJqqyNRlr9PsM5@madangs-log-v2.tdcbh.mongodb.net/?retryWrites=true&w=majority&appName=madangs-log-v2"
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(
                self.uri,
                serverSelectionTimeoutMS=10000,  # 10초 타임아웃 설정
                socketTimeoutMS=60000,  # 소켓 타임아웃 설정
                maxPoolSize=50,  # 최대 연결 풀 크기
                minPoolSize=10,  # 최소 연결 풀 크기
            )
            self.client.admin.command('ping')  # 연결 확인
            print("Connected to MongoDB")
        except ServerSelectionTimeoutError as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def set_database(self, db_name):
        self.db = self.client[db_name]

    def set_collection(self, db_name, collection_name):
        self.set_database(db_name)
        return self.db[collection_name]

    # Insert (Single Document with Upsert)
    def insert(self, db_name, collection, data, upsert=True):
        """
        Insert or update a single document.
        """
        coll = self.set_collection(db_name, collection)

        if "_id" not in data:  # Ensure _id is generated for each document
            data["_id"] = ObjectId()

        filter = {"_id": data["_id"]}
        update_data = {"$set": data}

        if upsert:
            result = coll.update_one(filter, update_data, upsert=True)
            return result.upserted_id or data["_id"]
        else:
            result = coll.insert_one(data)
            return result.inserted_id

    # Insert Many (Batch Upsert)
    def insert_many(self, db_name, collection, data_list, upsert=True):
        """
        Insert or update multiple documents using bulk operations.
        """
        coll = self.set_collection(db_name, collection)
        operations = []

        if not isinstance(data_list, list):
            raise ValueError("data_list must be a list of documents.")

        for data in data_list:
            if "_id" not in data:  # Ensure _id is generated for each document
                data["_id"] = ObjectId()

            filter = {"_id": data["_id"]}
            update_data = {"$set": data}
            operations.append(UpdateOne(filter, update_data, upsert=upsert))

        if operations:
            result = coll.bulk_write(operations)
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "upserted_count": result.upserted_count,
                "upserted_ids": result.upserted_ids,
            }

    # Find
    def find(self, db_name, collection, filter={}, options={}):
        coll = self.set_collection(db_name, collection)
        return list(coll.find(filter, **options))
    
    # Find One with Projection
    def find_one(self, db_name, collection, filter={}, projection=None):
        """
        Retrieve a single document that matches the given filter.
        If projection is specified, limit the fields returned.
        """
        coll = self.set_collection(db_name, collection)
        return coll.find_one(filter, projection)
    
    
    # Distinct
    def distinct(self, db_name, collection, field, filter={}):
        coll = self.set_collection(db_name, collection)
        return coll.distinct(field, filter)

    # Update with Upsert Option
    def update(self, db_name, collection, filter, data, upsert=True):
        """
        Update a single document with optional upsert functionality.
        """
        coll = self.set_collection(db_name, collection)
        result = coll.update_one(filter, {'$set': data}, upsert=upsert)
        return result.modified_count
    
    # Delete
    def delete(self, db_name, collection, filter):
        coll = self.set_collection(db_name, collection)
        result = coll.delete_one(filter)
        return result.deleted_count

    # Get by ID
    def get_by_id(self, db_name, collection, id):
        coll = self.set_collection(db_name, collection)
        return coll.find_one({'_id': ObjectId(id)})

    # Aggregate
    def aggregate(self, db_name, collection, pipeline=[], options={}):
        coll = self.set_collection(db_name, collection)
        result = coll.aggregate(pipeline, **options)
        return list(result)

    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")