import course_info_webscraper as ciw
import purdueio_api as pio
import get_jedi_courses as gjc
import get_elective_courses as gec
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv()
login_string = os.environ.get("MONGO_LOGIN")
client = MongoClient(login_string)

db = client.get_database('Pathways-Test')
courses = db.courses

def add_course(course):
    if courses.find_one({"course": course}) != None:
        return
    data = ciw.get_course_info(course)
    if data != None:
        courses.update_one({"course": course}, {"$set": json.loads(data)}, upsert=True)
        unique.append(course)
    else:
        invalid.append(course)
    
    
# courses_list = gjc.get_courses()
courses_list = []

with open("additional_courses.txt", "r") as f:
    courses_list = f.read().splitlines()
    f.close()

invalid = []
unique = []
print(courses_list)
n = 0
skip = True
for course in courses_list:
    n += 1
    print(f'{course}: {n} of {len(courses_list)}')
    add_course(course)
    
print("Done")
print(invalid)
print(len(invalid))
print(str(len(courses_list) - len(invalid)) + " out of " + str(len(courses_list)) + " courses added to the database.")
print("Unique: " + str(len(unique)))
print(unique)