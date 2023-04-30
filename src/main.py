import os
import csv
from canvasapi import Canvas
import yaml
#Students can resubit assignments, as a separate Gradescope assignment but this will update the existing Canvas assignment
#For resubmissions, the input folder for Gradescope will have the folder with the original assignment name and then a folder original assignment name + "_Resubmission"
#For resubmissions, if the student has a score of > 0 for a problem they already had a score for, then the score FOR THE ENTIRE ASSINGMENT WILL BE A 0
CANVAS_FILE_PATH = "../Canvas/"
GRADESCOPE_FILE_PATH = "../Gradescope/"
OUTPUT_FILE_PATH = "../Output/"
API_URL = "https://canvas.instructure.com"
#open config.yaml for api key, first line
API_KEY = open("../config.yaml", 'r').readline().split(':')[1].strip()
#open config.yaml for the course id, second line
COURSE_ID = open("../config.yaml", 'r').readlines()[1].split(':')[1].strip()
#open the config.yaml for the assignment id, third line
ASSIGNMENT_ID = int(open("../config.yaml", 'r').readlines()[2].split(':')[1].strip())
RUBRIC_ID = int(open("../config.yaml", 'r').readlines()[3].split(':')[1].strip())
STUDENT_ID = 208075
def getGradescopeScores(assignment, gradescopeColumn):
    gradeScopeScores = {}
    for question in os.listdir(GRADESCOPE_FILE_PATH + assignment):
        csvFile = open(GRADESCOPE_FILE_PATH + assignment + '/' + question, 'r')
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:
            if(row[gradescopeColumn] == '' or row['Tags'] == None):
                continue
            for tag in row['Tags'].split(','):
                if tag not in gradeScopeScores:
                    gradeScopeScores[tag] = {}
                if assignment not in gradeScopeScores[tag]:
                    gradeScopeScores[tag][assignment] = {}
                if row[gradescopeColumn] not in gradeScopeScores[tag][assignment]:
                    gradeScopeScores[tag][assignment][row[gradescopeColumn]] = float(row['Score'])
                else:
                    gradeScopeScores[tag][assignment][row[gradescopeColumn]] += float(row['Score'])
        csvFile.close()
    return gradeScopeScores

def updateCanvasScores(gradeScopeScores, canvasColumn):
    for tag in gradeScopeScores:
        try:
            csvInput = open(CANVAS_FILE_PATH + "Rubric Scores " + tag + ".csv", 'r')
        except:
            print("Could not find the file: " + CANVAS_FILE_PATH + "Rubric Scores " + tag + ".csv")
            continue
        csvOutput = open(OUTPUT_FILE_PATH + "Updated Rubric Scores " + tag + ".csv", 'w', newline='')
        csvReader = csv.DictReader(csvInput)
        fieldnames = []
        skipFields = []
        for field in csvReader.fieldnames:
            if "Posted Score" in field or "Attempt Number" in field or "Rating: " in field:
                skipFields.append(field)
                continue
            fieldnames.append(field)
        for assignment in gradeScopeScores[tag]:
            if "Points: " + assignment not in fieldnames:
                confirmation = input("Would you like to add the assignment " + assignment + " to the Canvas file for " + tag +"? (y/n): ")
                if confirmation == 'y':
                    print("Ok, please make sure the assignment " + assignment + " is added to the Canvas rubric for " + tag)
                    fieldnames.append("Points: " + assignment)
                else:
                    print("Canceling grade conversion, please delete all files in the Output folder and try again")
                    return
            else:
                confirmation = input("The assignment " + assignment + " already exists in the Canvas file for " + tag + ", would you like to modify it? (y/n) ")
                if confirmation == 'n':
                    print("Canceling grade conversion, please delete all files in the Output folder and try again")
                    return
        csvWriter = csv.DictWriter(csvOutput, fieldnames=fieldnames)
        csvWriter.writeheader()
        for assignment in gradeScopeScores[tag]:
            for row in csvReader:
                if row[canvasColumn] in gradeScopeScores[tag][assignment]:
                    #print(row[canvasColumn] + " " + tag + " " + assignment + " " + str(gradeScopeScores[tag][assignment][row[canvasColumn]]))
                    row["Points: " + assignment] = str(int(gradeScopeScores[tag][assignment][row[canvasColumn]]))
                else:
                    row["Points: " + assignment] = '0'
                for field in skipFields:
                    row.pop(field)
                csvWriter.writerow(row)
        csvInput.close()
        csvOutput.close()
def removeCanvasAssignment(assignment):
    for rubricScoresFile in os.listdir(CANVAS_FILE_PATH):
        try:
            csvInput = open(CANVAS_FILE_PATH + rubricScoresFile, 'r')
        except:
            print("Could not find the file: " + CANVAS_FILE_PATH + rubricScoresFile)
            continue
        csvOutput = open(OUTPUT_FILE_PATH + "Updated " + rubricScoresFile, 'w', newline='')
        csvReader = csv.DictReader(csvInput)
        if assignment not in csvReader.fieldnames:
            print("Could not find the assignment " + assignment + " in the file " + rubricScoresFile)
            print("Canceling assignment deletion, please delete all files in the Output folder and try again")
            return
        fieldNames = []
        for field in csvReader.fieldnames:
            if field != assignment:
                fieldNames.append(field)
        csvWriter = csv.DictWriter(csvOutput, fieldnames=fieldNames)
        csvWriter.writeheader()
        for row in csvReader:
            row.pop(assignment)
            csvWriter.writerow(row)
        csvInput.close()
        csvOutput.close()
def getCheaters(initialAssignment, resubmissionAssignment, gradescopeColumn):
    #need logic to find the score of each question to check if they're doubling up
    #if their score on a question was > 0 in the initial assignment, then their score for THE WHOLE resubmission assignment will be 0
    #otherwise, add the scores together
    cheatingStudents = []
    for question in os.listdir(CANVAS_FILE_PATH + initialAssignment):
        initialReader = csv.DictReader(open(CANVAS_FILE_PATH + initialAssignment + '/' + question, 'r'))
        resubmissionReader = csv.DictReader(open(CANVAS_FILE_PATH + resubmissionAssignment + '/' + question, 'r'))
        studentScores = {}
        for row in initialReader:
            if row[gradescopeColumn] == '':
                continue
            studentScores[row[gradescopeColumn]]["Initial"] = float(row['Score'])
        for row in resubmissionReader:
            if row[gradescopeColumn] == '':
                continue
            if row[gradescopeColumn] not in studentScores:
                studentScores[row[gradescopeColumn]] = {}
            studentScores[row[gradescopeColumn]]["Resubmission"] = float(row['Score'])
        for student in studentScores:
            if studentScores[student]["Initial"] > 0 and studentScores[student]["Resubmission"] > 0:
                cheatingStudents.append(student)
    return cheatingStudents
def getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn):
    initialScores = getGradescopeScores(initialAssignment, gradescopeColumn)
    resubmissionScores = getGradescopeScores(resubmissionAssignment, gradescopeColumn)
    cheatingStudents = getCheaters(initialAssignment, resubmissionAssignment, gradescopeColumn)
    for tag in initialScores:
        for assignment in initialScores[tag]:
            for student in initialScores[tag][assignment]:
                if student in cheatingStudents:
                    initialScores[tag][assignment][student] = 0
                else:
                    initialScores[tag][assignment][student] += resubmissionScores[tag][assignment][student]
    return initialScores

if __name__ == "__main__":
    # canvas = Canvas(API_URL, API_KEY)
    # course = canvas.get_course(COURSE_ID)
    # assignment = course.get_assignment(ASSIGNMENT_ID)
    # submissions = assignment.get_submissions()
    # for submission in submissions:
    #     res = submissions[0].edit(rubric_assessment={'Fundamental Skills 1': {'points': 2}})
    #
    canvasFileList = os.listdir(CANVAS_FILE_PATH)
    gradescopeAssignmentList = os.listdir(GRADESCOPE_FILE_PATH)
    command = input("Grade, Resubmission, or Remove? (g/r/rm): ")
    while command != 'g' and command != 'r' and command != 'rm':
        command = input("Invalid command, please enter g, r, or rm: ")
    if command == 'g':
        gradescopeColumn = input("Please input the Gradescope column name you would like to use to match students with. Default is Name: ")
        if gradescopeColumn == '':
            gradescopeColumn = 'Name'
        canvasColumn = input("Please input the Canvas column name you would like to use to match students with. Default is Student Name: ")
        if canvasColumn == '':
            canvasColumn = 'Student Name'
        for assignment in gradescopeAssignmentList:
            scores = getGradescopeScores(assignment, gradescopeColumn)
            print(scores)
            updateCanvasScores(scores, canvasColumn)
    elif command == 'r':
        print("Resubmission")
        initialAssignment = input("Please input the name of the initial assignment: ")
        resubmissionAssignment = input("Please input the name of the resubmission assignment (default is initial assignemnt name with _Resubmission added to the end: ")
        if resubmissionAssignment == '':
            resubmissionAssignment = initialAssignment + "_Resubmission"
        gradescopeColumn = input("Please input the Gradescope column name you would like to use to match students with. Default is Name: ")
        if gradescopeColumn == '':
            gradescopeColumn = 'Name'
        canvasColumn = input("Please input the Canvas column name you would like to use to match students with. Default is Student Name: ")
        if canvasColumn == '':
            canvasColumn = 'Student Name'
        scores = getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn)
        print(scores)
        updateCanvasScores(scores, canvasColumn)

    elif command == 'rm':
        removeColumn = input("Please input the assignment name you would like to remove from the Canvas file: ")
        removeCanvasAssignment(removeColumn)

