from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://www.purdue.edu/science/Current_Students/curriculum_and_degree_requirements/Great%20Issues%20Courses.php"

options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

driver.get(url)

html = driver.page_source

driver.close()

soup = BeautifulSoup(html, 'html5lib')
tbody = soup.select_one("#example > tbody")


courses = []
for tr in tbody.select("tr"):
    course_type = tr.select_one("td.sorting_1").text.split(" - ")[0]
    course_num = tr.select_one("td.sorting_2").text
    course = course_type + " " + course_num
    courses.append(course)

def get_courses():
    return courses