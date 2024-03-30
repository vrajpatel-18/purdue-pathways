import requests
import json


def get_cs_courses():
    response = requests.get("https://api.purdue.io/odata/Courses?$filter=Subject/Abbreviation eq 'CS'&$orderby=Number asc")

    if response.status_code == 200:
        data = response.json()
        courses = []
        for course in data['value']:
            curr_course = "CS " + course['Number']
            if curr_course not in courses:
                courses.append(curr_course)
        print(courses)
        return courses