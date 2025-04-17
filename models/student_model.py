from time import strftime

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


client = MongoClient("mongodb://localhost:27017/")
db = client["studentdb"]
collection = db["students"]

def get_all_students():
    students = list(collection.find())
    return students

def add_student(student_data):
    student_data["enrollment_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return collection.insert_one(student_data)

def update_student(student_id, data):
    return collection.update_one({ "_id": ObjectId(student_id)}, {"$set": data})