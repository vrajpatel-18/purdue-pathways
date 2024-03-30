import requests
from bs4 import BeautifulSoup

url = "https://www.purdue.edu/provost/students/s-initiatives/curriculum/courses.html"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

print("Loaded")

courses = []

for i in range(7,23,2):
    el = soup.select_one(f"body > div.content > div > div > div.maincontent.col-lg-9.col-md-9.col-sm-9.col-xs-12.right > div:nth-child({i})")
    items = el.select("p")
    for item in items:
        texts = item.text.split(" ")
        course = texts[0] + " " + texts[1]
        courses.append(course)

def get_courses():
    return courses