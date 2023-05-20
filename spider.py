import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, filename="spider.log", format=format)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------- #
#                           Initialize browser driver                          #
# ---------------------------------------------------------------------------- #
driver = webdriver.Firefox()
driver.get("https://justjoin.it/")

# ---------------------------------------------------------------------------- #
#              Find class name for elements containing a job role              #
# ---------------------------------------------------------------------------- #
element = driver.find_element(By.XPATH, "//*[contains(text(), 'Developer')]")
job_title_element_class = element.get_attribute("class")

logger.debug(f"Determined that elements containing a job title have class {job_title_element_class}")

# Find scrollable element
scrollable_container = None
find_div_elements_wider_than_200px_xpath = "//div[(@style and contains(@style, 'width') and number(substring-before(substring-after(@style, 'width:'), 'px')) > 200) or (number(substring-before(substring-after(@width, 'px'), 'px')) > 200)]"
elements = driver.find_elements(By.XPATH, find_div_elements_wider_than_200px_xpath)
for elem in elements:
    class_name = elem.get_attribute("class")
    if "css" in class_name:
        scrollable_container = class_name
        logger.debug(f"Found scrollable container: {class_name}")

# ---------------------------------------------------------------------------- #
#                           Iterate through listings                           #
# ---------------------------------------------------------------------------- #
import time

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
#while True:
for i in range(3):
    job_titles = driver.find_elements(By.CLASS_NAME, job_title_element_class)
    salaries = driver.find_elements(By.XPATH, "//div[contains(text(), 'PLN') or contains(text(), 'Undisclosed Salary')]")
    salaries = list(filter(lambda x: x.text and x.text.strip(), salaries))

    columns = ["Job Title", "Salary"]
    format_row = "{:>50}" * len(columns)
    print("-" * 50 * len(columns))
    print(format_row.format(*columns))
    print("-" * 50 * len(columns))
    for (job_title, salary) in zip(job_titles, salaries):
        print(format_row.format(job_title.text, salary.text))

    # Scroll down to bottom
    driver.execute_script(f"document.querySelector('div.{scrollable_container}').scrollBy(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
