import os
import csv
from canvasapi import Canvas
import yaml
CANVAS_FILE_PATH = "../Canvas/"
GRADESCOPE_FILE_PATH = "../Gradescope/"
OUTPUT_FILE_PATH = "../Output/"
API_URL = "https://canvas.instructure.com"

#Make a function called "Get Course Info" that takes in a course name and returns the course ID, as well as assignment IDs and names
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
                    userLogin = row[gradescopeColumn].split('@')[0]
                    gradeScopeScores[tag][assignment][userLogin] = float(row['Score'])
                else:
                    gradeScopeScores[tag][assignment][userLogin] += float(row['Score'])
        csvFile.close()
    return gradeScopeScores

#WE MOST LIKELY WON'T NEED THIS FUNCTION ANYMORE, SINCE WE CAN UPLOAD THE GRADESCOPE SCORES TO CANVAS AUTOMATICALLY
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

#CHANGE THIS FUNCTION TO USE THE CANVAS API INSTEAD OF THE CSV FILES
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

def uploadCanvasScores(assignment, criterionName, assignmentScores):
    criterion_id = ""
    for criterion in assignment.rubric:
        if criterion['description'] == criterionName:
            criterion_id = criterion['id']
    submissions = assignment.get_submissions(include=['rubric_assessment', 'user'])
    for submission in submissions:
        emailPrefix = submission.user['login_id']
        try:
            submission.edit(rubric_assessment={criterion_id: {'points': assignmentScores[emailPrefix]}})
            print("Successfully uploaded the score for " + submission.user['short_name'] + " for " + assignment.name)
        except:
            print("Could not find the student " + submission.user['short_name'] + " in the Gradescope file for " + assignment.name)
            continue
if __name__ == "__main__":
    #read config.yaml with yaml library
    with open("../config.yaml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    #set variables from config
    apiKey = config['API_KEY']
    courseId = config['COURSE_ID']
    canvas = Canvas(API_URL, apiKey)
    course = canvas.get_course(courseId)

    canvasFileList = os.listdir(CANVAS_FILE_PATH)
    gradescopeAssignmentList = os.listdir(GRADESCOPE_FILE_PATH)
    gradescopeColumn = 'Email'
    command = input("Grade, Resubmission, or Remove? (g/r/rm): ")
    while command != 'g' and command != 'r' and command != 'rm':
        command = input("Invalid command, please enter g, r, or rm: ")
    if command == 'g':
        for assignment in gradescopeAssignmentList:
            scores = getGradescopeScores(assignment, gradescopeColumn)
            print(scores)
            for bundle in scores:
                canvasAssignment = course.get_assignment(config['ASSIGNMENTS'][bundle])
                try:
                    rubric = canvasAssignment.rubric
                except:
                    print("Could not find rubric for assignment " + bundle)
                    continue
                for criterion in scores[bundle]:
                    uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion])


    #AS OF YET UNTESTED (NEED TO CHANGE IT TO USE CANVAS API AS WELL, ONCE WE HAVE TESTING DATA)
    # elif command == 'r':
    #     print("Resubmission")
    #     initialAssignment = input("Please input the name of the initial assignment: ")
    #     resubmissionAssignment = input("Please input the name of the resubmission assignment (default is initial assignemnt name with _Resubmission added to the end: ")
    #     if resubmissionAssignment == '':
    #         resubmissionAssignment = initialAssignment + "_Resubmission"
    #     gradescopeColumn = input("Please input the Gradescope column name you would like to use to match students with. Default is Name: ")
    #     if gradescopeColumn == '':
    #         gradescopeColumn = 'Name'
    #     canvasColumn = input("Please input the Canvas column name you would like to use to match students with. Default is Student Name: ")
    #     if canvasColumn == '':
    #         canvasColumn = 'Student Name'
    #     scores = getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn)
    #     print(scores)
    #     updateCanvasScores(scores, canvasColumn)
    #
    # elif command == 'rm':
    #     removeColumn = input("Please input the assignment name you would like to remove from the Canvas file: ")
    #     removeCanvasAssignment(removeColumn)

