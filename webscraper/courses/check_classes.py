from pymongo import MongoClient
import os
from dotenv import load_dotenv

unique = []
all_courses = []

with open("all_courses.txt", "r") as f:
    all_courses = f.read().splitlines()
    f.close()
  

load_dotenv()
login_string = os.environ.get("MONGO_LOGIN")
client = MongoClient(login_string)

db = client.get_database('pathways-data')
courses = db.courses

course_list = courses.distinct("course")



for course in all_courses:
    print(f"{course}, {all_courses.index(course) + 1} of {len(all_courses)}")
    if course in course_list:
        continue
    unique.append(course)

print(len(unique))

with open("additional_courses.txt", "w") as f:
    for course in unique:
        f.write(course + "\n")
    f.close()