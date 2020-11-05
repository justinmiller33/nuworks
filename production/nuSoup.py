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
                
    
# Function to get data with soup
def nuMake(filePath,fileName):

    # Preloaded list of master questions
    masterQuestions = ['Position Type', 'Number of Openings', 'Description', 'Job Number', 'Location', 'Targeted Academic Majors', 'Hiring Status', 'Job Function', 'Payment Type and Range', 'Hours Per Week', 'Workplace Type', 'Transportation', 'Work Authorization', 'Additional Documents', 'Desired Skills', 'Division', 'Student Search Tags', 'Attachment(s)', 'Travel Advisory', 'Desired Class Level(s)', 'Period of Employment', 'Schools']
    
    # Open File
    file = open(filePath + fileName, 'r')
    content = file.read()
    file.close()

    # Soup
    soup = BeautifulSoup(content)

    # Getting objects for questions, answers, skills, and descriptions
    questions = soup.find_all("div", class_="field-label")
    answers = soup.find_all('div', class_="widget")
    jobSkills = soup.find_all("span", class_='job-skill ajax_pill_readonly')
    jobDescriptions = soup.find('div', class_='job_description widget')

    # Getting Title
    title = soup.find_all("h1")
    title = title[1].string
    # Cleaning title
    # TODO add regex
    title.strip("\n")
    title.strip("   ")
    
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

        try:        
            element = element.strip("\n")
            element = element.strip("\t")
            element = element.strip("\n")

        except:
            element = ""

        textAnswers[elementNum] = element
        

    # Getting job skills
    textJobSkills = []
    for tag in jobSkills:
        textJobSkills.append(tag.string)

    # Getting job descriptions
    s = ""
    for tag in jobDescriptions:

        # Keep running if tags are empty
        try:
            s = s + tag.string
        except:
            continue

    # Cleaning job descriptions
    s = s.strip("\n")
    s = s.strip("\t")
    s = s.strip("\xa0")
    s = s.strip("\n")
    s = re.sub("\n●","",s)
    

    # Making main csv row
    csvRow = []
    # For each question
    for question in masterQuestions:

        if question in textQuestions:

            answer = textAnswers[textQuestions.index(question)]
            csvRow.append(answer)

        else:

            csvRow.append("")

    csvRow.append(s)

    csvRow.insert(0,title)
    print(csvRow)
    
    # Optional Function: sorting by school
    
    
for i in range(len(fileList)):
    nuMake(filePath,fileList[i])

