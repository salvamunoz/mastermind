import pymongo

try:
    # TODO: store uri in a OS variable inside Docker.
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["mastermind"]
    collection = db["games"]
except pymongo.errors.ConnectionFailure as e:
    print(f"Error: Could not connect to MongoDB: {e}")
    raise
