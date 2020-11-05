# Extracting NUWorks from raw html files
# Justin Miller, Northeastern University COE
# Paxton Howard, Northeastern University COS

# Modules
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import sys
import os
import re
import csv

# Getting all text files in data folder
filePath = sys.path[0][:-10] + "rawFiles/"
fileList = os.listdir(filePath)

# Function to get list of all questions
# Only need to run once... already loaded in to masterQuestions list in nuMake
def getMasterQuestions(filePath,fileList):

    masterQuestions = []
    # Looping through each question
    for i in range(len(fileList)):
        # Open File
        file = open(filePath + fileList[i], 'r')
        content = file.read()
        file.close()

        # Soup
        soup = BeautifulSoup(content)

        # Getting qs
        questions = soup.find_all("div", class_="field-label")

        textQuestions = []
        for tag in questions:
                textQuestions.append(tag.string)

        textQuestions = list(filter((None).__ne__, textQuestions))

        # Looping through each question in here
        for question in textQuestions:

            # If its not in the master list add it
            if question not in masterQuestions:

                masterQuestions.append(question)
                print(i)
                print(masterQuestions)

# Is this school included in posting
def getBySchool(majors):

    # List of colleges
    schoolList = ["Bouve College of Health Sciences","College of Engineering","College of Arts, Media & Design","College of Science","College of Social Science & Humanities","D'Amore-McKim School of Business","Khoury College of Computer Sciences"]

    # Boolean array for the schools above
    schoolBool = []
    for school in schoolList:

        if school in majors:
            schoolBool.append('Yes')

        else:
            schoolBool.append('No')

    return schoolBool

# Function to get data with soup
def nuMake(filePath,fileName):

    # Preloaded list of master questions
    masterQuestions = ['Position Type', 'Number of Openings', 'Location', 'Targeted Academic Majors', 'Hiring Status', 'Job Function', 'Payment Type and Range', 'Hours Per Week', 'Workplace Type', 'Transportation', 'Work Authorization', 'Additional Documents']
    
    # Open File
    file = open(filePath + fileName, 'r')
    content = file.read()
    file.close()

    # Soup
    soup = BeautifulSoup(content)

    # Getting objects for questions, answers, skills, descriptions, and dates
    questions = soup.find_all("div", class_="field-label")
    answers = soup.find_all('div', class_="widget")
    jobSkills = soup.find_all("span", class_='job-skill ajax_pill_readonly')
    jobDescriptions = soup.find('div', class_='job_description widget')
    dates = soup.find_all('div', class_="body-small text-content")
    
    # Getting Title
    title = soup.find_all("h1")
    title = title[1].string
    # Cleaning title
    # TODO add regex
    title = re.sub("\n","",title)
    title = re.sub("    ","",title)
    

    # Getting location (html inconsistencies)
    location = soup.find_all("div", class_="widget jobfld-location")
    location = location[0].text

    # Cleaning location
    location = re.sub("\n","",location)
    location = re.sub(r"(\w)([A-Z])", r"\1 \2", location)
    
 
    # Getting text questions
    textQuestions = []
    for tag in questions:
            textQuestions.append(tag.string)

    textQuestions = list(filter((None).__ne__, textQuestions))
    textQuestions = list(filter(("Desired Skills").__ne__, textQuestions))


    # Getting text answers
    textAnswers = []
    for tag in answers:
        textAnswers.append(tag.string)


    # Cleaning text answers
    for elementNum in range(len(textAnswers)):

        element = textAnswers[elementNum]

        # If element is a nonetype save it as empty string
        try:        
            element = re.sub("\n","",element)
            element = re.sub("\t","",element)

        except:
            element = ""

        textAnswers[elementNum] = element
        

    # Getting job skills
    textJobSkills = []
    for tag in jobSkills:
        textJobSkills.append(tag.string)

    # Creating a string of skills
    try:
        temp = ", "    
        textJobSkills = temp.join(textJobSkills)

    except:
        textJobSkills = ""
    
    # Getting job descriptions
    s = ""
    for tag in jobDescriptions:

        # Keep running if tags are empty
        try:
            s = s + tag.string
        except:
            continue

    # Cleaning job descriptions

    s = re.sub("\t","",s)
    s = re.sub("\xa0","",s)
    s = re.sub("\n","",s)
    s = re.sub("●","",s)


    postedOn = []
    # Getting dates
    for tag in dates:

        post = tag.find_all('p')

        for tag in post:
            postedOn.append(tag.string)


    postDate = postedOn[1]
    deadline = postedOn[3]

    # Making main csv row
    csvRow = []
    # For each question
    for question in masterQuestions:

        if question in textQuestions:

            answer = textAnswers[textQuestions.index(question)]
            csvRow.append(answer)

        else:

            csvRow.append("")

    # Fixing value for location here
    csvRow[2] = location
    
    # Appending skills and description
    csvRow.append(textJobSkills)
    csvRow.append(s)

    # Inserting title and relevant dates up front
    csvRow.insert(0,deadline)
    csvRow.insert(0,postDate)
    csvRow.insert(0,title)

    # Getting schoolBool
    # Note order here for taking major list...
    schoolBool = getBySchool(csvRow[6])
    csvRow = csvRow + schoolBool
    
    return csvRow
    


# Writing to csv
with open("nuworks.csv","w") as csvFile:

    # List of labels
    labels = ['Position','Date Posted','Application Due','Position Type', 'Number of Openings', 'Location', 'Targeted Academic Majors', 'Hiring Status', 'Job Function', 'Payment Type and Range', 'Hours Per Week', 'Workplace Type', 'Transportation', 'Work Authorization', 'Additional Documents','Desired Skills','Description',"Bouve College of Health Sciences","College of Engineering","College of Arts, Media & Design","College of Science","College of Social Science & Humanities","D'Amore-McKim School of Business","Khoury College of Computer Sciences"]
    
        
    csvWriter = csv.writer(csvFile, delimiter = ',')
    csvWriter.writerow(labels)
    
    for i in range(len(fileList)):
        csvRow = nuMake(filePath,fileList[i])
        csvWriter.writerow(csvRow)

        if not i%100:

            print(i)
