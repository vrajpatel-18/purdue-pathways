from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time


def get_course_info(course):
    course_type = course.split(" ")[0]
    course_num = course.split(" ")[1]
    if len(course_num) == 3:
        course_num = course_num + "00"
    url = "https://selfservice.mypurdue.purdue.edu/prod/bzwsrch.p_catalog_detail?subject=" + course_type + "&term=CURRENT&cnbr=" + course_num

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # time.sleep(5)

    html = driver.page_source

    driver.close()

    soup = BeautifulSoup(html, 'html5lib')
    el = soup.select_one("body > div.pagebodydiv > table:nth-child(2) > tbody > tr:nth-child(2) > td")

    if el == None:
        print(f"Course {course} not found")
        return None

    full_text = el.text

    split = full_text.split("\n")
    split = list(filter(None, split))
    split = [" ".join(i.split()) for i in split]

    # for item in split:
    #     print(item)
    #     print()
        
    title = ""
    prereqs = ""
    department = ""
    description = ""
    outcomes = ""
    restrictions = ""
        
    title_text = soup.select_one("body > div.pagebodydiv > table:nth-child(2) > tbody > tr:nth-child(1) > td").text
    title = title_text.split(" - ")[1]
    # print("Title: " + title)

    if "Prerequisites:" in split:
        try:
            prereqs = split[split.index("Prerequisites:") + 1]
        except IndexError:
            prereqs = ""
        # print("Prerequisites: " + prereqs)
    # else:
    #     print("Prerequisites: None")
        
    for item in split:
        if "Department:" in item:
            try:
                department = item.split("Department: ")[1]
            except IndexError:
                department = ""
            # print("Department: " + department)
            break

    description = split[0]
    # print("Description: " + description)

    if "Learning Outcomes:" in split:
        try:
            outcomes = split[split.index("Learning Outcomes:") + 1]
        except IndexError:
            outcomes = ""
        # print("Learning Outcomes: " + outcomes)
    # else:
    #     print("Learning Outcomes: None")

    if "Restrictions:" in split:
        try:
            restrictions = split[split.index("Restrictions:") + 1]
        except IndexError:
            restrictions = ""
        # print("Restrictions: " + restrictions)
    # else:
    #     print("Restrictions: None")
        
    data = {
        "course": course_type + " " + course_num,
        "title": title,
        "prereqs": prereqs,
        "department": department,
        "description": description,
        "outcomes": outcomes,
        "restrictions": restrictions
    }

    # with open(f'{course_type}{course_num}.json', 'w') as f:
    #     json.dump(data, f, indent=4)
    # print("Data written to " + f"{course_type}{course_num}.json")
    
    return json.dumps(data, indent=4)