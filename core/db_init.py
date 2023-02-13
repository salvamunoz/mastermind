from pymongo import MongoClient

# TODO: store uri in a OS variable inside Docker.
client = MongoClient("mongodb://localhost:27017/")
db = client["mastermind"]
collection = db["games"]
