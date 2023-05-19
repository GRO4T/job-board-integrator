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

# ---------------------------------------------------------------------------- #
#                           Iterate through listings                           #
# ---------------------------------------------------------------------------- #
listings = driver.find_elements(By.CLASS_NAME, job_title_element_class)

for listing in listings:
    print(listing.text)
