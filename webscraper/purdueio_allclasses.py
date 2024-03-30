import requests
import json


def get_all_subjects():
    response = requests.get("https://api.purdue.io/odata/Subjects")
    if response.status_code == 200:
        data = response.json()
        subjects = []
        for subject in data['value']:
            subjects.append(subject['Abbreviation'])
        return subjects

print(get_all_subjects())

def get_all_courses(subjects):
    courses = []
    for subject in subjects:
        print(f"{subject}, {subjects.index(subject) + 1} of {len(subjects)}")
        response = requests.get(f"https://api.purdue.io/odata/Courses?$filter=Subject/Abbreviation eq '{subject}'&$orderby=Number asc")
        if response.status_code == 200:
            data = response.json()
            for course in data['value']:
                curr_course = subject + " " + course['Number']
                if curr_course not in courses:
                    courses.append(curr_course)
                    
    return courses

courses = get_all_courses(get_all_subjects())
print(courses)
print(len(courses))

with open("all_courses.txt", "w") as f:
    for course in courses:
        f.write(course + "\n")
    f.close()