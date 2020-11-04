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
browser = webdriver.Chrome()

# Link to search
link = "https://northeastern-csm.symplicity.com/students/app/jobs/search?perPage=2540&job_type=5"
browser.get(link)
