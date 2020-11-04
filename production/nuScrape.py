# Scraping NUWorks employment portal using simulated webdriver
# Justin Miller, Northeastern University COE
# Paxton Howard, Northeastern University COS

# Modules
import numpy as np
from selenium import webdriver

# -------
# |USAGE|
# No real need for oop yet
# Just a slightly jank simulated browser
# --------------------------------------


# Initializing Browser
driver = webdriver.Chrome()

# Link to search
link = "https://northeastern-csm.symplicity.com/students/app/jobs/search?perPage=10000&job_type=5"

# Loading up browser
driver.get(link)

# Loading up body for calls
body = driver.find_element_by_tag_name("body")

def initPosition(body,driver):


