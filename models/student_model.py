from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import gridfs

client = MongoClient("mongodb://localhost:27017/")
db = client["studentdb"]
collection = db["students"]

fs = gridfs.GridFS(db)

def get_student_by_id(student_id):
    return collection.find_one({"_id": ObjectId(student_id)})

def get_all_students():
    students = list(collection.find())
    return students

def add_student(student_data, image_file=None):
    student_data["enrollment_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if image_file:
        image_id = fs.put(image_file, filename=image_file.filename, content_type=image_file.content_type)
        student_data["image_id"] = str(image_id)
    return collection.insert_one(student_data)

def update_student(student_id, data, new_image_file=None):
    student = get_student_by_id(student_id)
    if new_image_file:
        if student and student.get("image_id"):
            try:
                fs.delete(ObjectId(student["image_id"]))
            except:
                pass

        new_image_id = fs.put(new_image_file, filename=new_image_file.filename, content_type=new_image_file.content_type)
        data["image_id"] = str(new_image_id)
    return collection.update_one({ "_id": ObjectId(student_id)}, {"$set": data})

def delete_student(student_id):
    student = get_student_by_id(student_id)
    if student and student.get("image_id"):
        try:
            fs.delete(ObjectId(student["image_id"]))
        except:
            pass

    return collection.delete_one({"_id": ObjectId(student_id)})