# Scraping NUWorks employment portal using simulated webdriver
# Justin Miller, Northeastern University COE
# Paxton Howard, Northeastern University COS

# Modules
import numpy as np
from selenium import webdriver
import time
import pyautogui

# -------
# |USAGE|
# No real need for oop yet
# Just a slightly jank simulated browser
# Also only runable on my machine and
# Requires manual inputs + logins
# --------------------------------------

# Save html in a text file
def saveTxtFile(postId,html):

    txtName = postId + ".txt"
    file = open("/home/justinmiller/devel/nuworks/rawFiles/" + txtName, "w")
    f = file.write(html)
    file.close()

# Recursively try to get content box
def recurseContent(driver):
    try:
        time.sleep(.25)
        content= driver.find_element_by_css_selector("job-element.ng-isolate-scope")
        content.click()

    except:
        recurseContent(driver)

# Initializing Browser
driver = webdriver.Chrome()

# Link to search
link = "https://northeastern-csm.symplicity.com/students/app/jobs/search?page=1&perPage=1&job_type=5"
# Loading up nuworks
driver.get(link)

# Confirm login
y = input("Confirm Login? y/n: ")
# Don't really need a condition here

# Going to nuworks search link
driver.get(link)

# Confirm load
y = input("Confirm Page Load? y/n: ")
# Don't really need a condition here

# Get number of jobs in this load
num = int(input("Number of Jobs: "))

# Loading up body for calls
body = driver.find_element_by_tag_name("body")

# Declaring the current job num
jobNum = 1

# Looping through each job
for i in range(num):

    # Opening Job Page
    recurseContent(driver)

    # While loading, sleep
    while link == driver.current_url:
        time.sleep(1)

    # Save new url
    newUrl = driver.current_url

    # Get all html
    html = driver.page_source

    # Get post id from url
    postId = newUrl[65:]

    # Update
    print("Iteration " + str(i))
    print(postId)

    # Save text file
    saveTxtFile(postId,html)
    
    # Increasing jobnum
    jobNum = jobNum + 1

    # Setting old link
    oldLink = link
    
    # Getting New link
    link = "https://northeastern-csm.symplicity.com/students/app/jobs/search?page=" + str(jobNum) + "&perPage=1&job_type=5"

    # Get next link
    driver.get(link)

    # While loading, sleep
    while oldLink == driver.current_url:
        time.sleep(1)






