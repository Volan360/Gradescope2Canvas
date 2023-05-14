import os
import csv

import canvasapi.util
import py2exe
from canvasapi import Canvas
import yaml

with open("../config.yaml", 'r') as stream:
    CONFIG = yaml.safe_load(stream)

CANVAS_FILE_PATH = CONFIG['CANVAS_FOLDER']
GRADESCOPE_FILE_PATH = CONFIG['GRADESCOPE_FOLDER']
OUTPUT_FILE_PATH = CONFIG['OUTPUT_FOLDER']
API_URL = CONFIG['CANVAS_API']['URL']

#Make a function called "Get Course Info" that takes in a course name and returns the course ID, as well as assignment IDs and names
def getGradescopeScores(assignment, gradescopeColumn):
    gradeScopeScores = {}
    for question in os.listdir(GRADESCOPE_FILE_PATH + assignment):
        csvFile = open(GRADESCOPE_FILE_PATH + assignment + '/' + question, 'r')
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:
            if not row[gradescopeColumn] or not row['Tags']:
                continue
            if '@' in row[gradescopeColumn]:
                userLogin = row[gradescopeColumn].split('@')[0]
            else:
                userLogin = int(row[gradescopeColumn])
            for tag in row['Tags'].split(','):
                if tag not in gradeScopeScores:
                    gradeScopeScores[tag] = {}
                if assignment not in gradeScopeScores[tag]:
                    gradeScopeScores[tag][assignment] = {}
                if userLogin not in gradeScopeScores[tag][assignment].keys():
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
                if int(row[canvasColumn]) in gradeScopeScores[tag][assignment].keys():
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
def removeCanvasAssignmentLocal(assignment):
    assignment = "Points: " + assignment
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
            pass
        fieldNames = []
        skipFields = []
        for field in csvReader.fieldnames:
            if "Posted Score" in field or "Attempt Number" in field or "Rating: " in field or field == assignment:
                skipFields.append(field)
                pass
            else:
                fieldNames.append(field)
        csvWriter = csv.DictWriter(csvOutput, fieldnames=fieldNames)
        csvWriter.writeheader()
        for row in csvReader:
            try:
                for field in skipFields:
                    row.pop(field)
            except KeyError:
                pass
            csvWriter.writerow(row)
        csvInput.close()
        csvOutput.close()
def getCheaters(initialAssignment, resubmissionAssignment, gradescopeColumn):
    cheatingStudents = []
    for question in os.listdir(GRADESCOPE_FILE_PATH + initialAssignment):
        initialReader = csv.DictReader(open(GRADESCOPE_FILE_PATH + initialAssignment + '/' + question, 'r'))
        resubmissionReader = csv.DictReader(open(GRADESCOPE_FILE_PATH + resubmissionAssignment + '/' + question, 'r'))
        initialScores = {}
        resubmissionScores = {}
        for row in initialReader:
            if not row[gradescopeColumn] or not row['Tags']:
                continue
            if '@' in row[gradescopeColumn]:
                userLogin = row[gradescopeColumn].split('@')[0]
            else:
                userLogin = row[gradescopeColumn]
            if not userLogin in initialScores:
                initialScores[userLogin] = {}
            initialScores[userLogin][question] = float(row['Score'])
        for row in resubmissionReader:
            if not row[gradescopeColumn] or not row['Tags']:
                continue
            if '@' in row[gradescopeColumn]:
                userLogin = row[gradescopeColumn].split('@')[0]
            else:
                userLogin = row[gradescopeColumn]
            if not userLogin in resubmissionScores:
                resubmissionScores[userLogin] = {}
            resubmissionScores[userLogin][question] = float(row['Score'])
        for student in resubmissionScores:
            if initialScores[student][question] > 0 and resubmissionScores[student][question] > 0:
                print(student + " cheated on " + question)
                print("Initial Score: " + str(initialScores[student][question]))
                print("Resubmission Score: " + str(resubmissionScores[student][question]))
                cheatingStudents.append(student)
    return cheatingStudents
def getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn):
    initialScores = getGradescopeScores(initialAssignment, gradescopeColumn)
    resubmissionScores = getGradescopeScores(resubmissionAssignment, gradescopeColumn)
    cheatingStudents = getCheaters(initialAssignment, resubmissionAssignment, gradescopeColumn)
    for tag in resubmissionScores:
        for student in resubmissionScores[tag][resubmissionAssignment]:
            if student in cheatingStudents:
                initialScores[tag][initialAssignment][student] = 0
            else:
                initialScores[tag][initialAssignment][student] += resubmissionScores[tag][resubmissionAssignment][student]
    return initialScores

def uploadCanvasScores(assignment, criterionName, assignmentScores, byEmailPrefix=True):
    criterion_id = ""
    for criterion in assignment.rubric:
        if criterion['description'] == criterionName:
            criterion_id = criterion['id']
    submissions = assignment.get_submissions(include=['rubric_assessment', 'user'])
    for submission in submissions:
        if byEmailPrefix:
            matchColumn = submission.user[CONFIG['CANVAS_API']['NET_ID_ENDPOINT']]
        else:
            matchColumn = submission.user[CONFIG['CANVAS_API']['SID_ENDPOINT']]
        try:
            submission.edit(rubric_assessment={criterion_id: {'points': assignmentScores[matchColumn]}})
            print("Successfully uploaded the score for " + submission.user['short_name'] + " for " + assignment.name)
        except:
            print("Could not find the student " + submission.user['short_name'] + " in the Gradescope file for " + assignment.name)
            continue
    print("\nFinished uploading scores for " + assignment.name + "\n")
if __name__ == "__main__":
    #set variables from config
    try:
        apiKey = CONFIG['CANVAS_API']['KEY']
        canvas = Canvas(API_URL, apiKey)
        command = input("Grade, Resubmission, Remove, or Course Info? (G/R/RM/CI): ")
        while command != 'G' and command != 'R' and command != 'RM' and command != 'CI':
            command = input("Invalid command, please enter G, R, RM, or CI: ")
        if command == 'CI':
            courseName = input("Please enter the name of the course you want info on, as displayed on canvas: ")
            yamlInfo = ""
            for course in canvas.get_courses():
                try:
                    if course.name == courseName:
                        yamlInfo += "COURSE_ID: " + str(course.id) + "\nASSIGNMENTS:\n"
                        for assignment in course.get_assignments():
                            yamlInfo += "\t" + assignment.name + ": " + str(assignment.id) + "\n"
                        break
                except:
                    continue
            #write the yaml info into a text file
            yamlFile = open("courseInfo.txt", 'w')
            yamlFile.write(yamlInfo)
            yamlFile.close()
            print("Finished writing course info to courseInfo.txt, located in the same folder as this program (might show up after you close this window)")
            print("Please copy and paste the information into the config.yaml file, indented under the CANVAS_API section")
            print("Please also make sure that all assignments that aren't connected to rubrics (everything that isn't a bundle) are removed from the config file")
        elif command == 'G':
            courseId = CONFIG['CANVAS_API']['COURSE_ID']
            course = canvas.get_course(courseId)

            canvasFileList = os.listdir(CANVAS_FILE_PATH)
            gradescopeAssignmentList = os.listdir(GRADESCOPE_FILE_PATH)
            localOrUpload = input("Save CSV files locally or upload directly to Canvas? (L/U): ")
            while localOrUpload != 'L' and localOrUpload != 'U':
                localOrUpload = input("Invalid command, please enter L for local or U for upload: ")
            if localOrUpload == 'L':
                gradescopeColumn = input("Please enter the name of the column containing the student SID (defaults to SID): ")
                if gradescopeColumn == '':
                    gradescopeColumn = 'SID'
                canvasColumn = input("Please enter the name of the column containing the student SID (defaults to Student ID): ")
                if canvasColumn == '':
                    canvasColumn = 'Student ID'
                for assignment in gradescopeAssignmentList:
                    scores = getGradescopeScores(assignment, gradescopeColumn)
                    updateCanvasScores(scores, canvasColumn)
            else:
                emailOrSID = input("Email or SID (E/S): ")
                while emailOrSID != 'E' and emailOrSID != 'S':
                    gradescopeColumn = input("Invalid column, please enter E for email or S for SID: ")
                if emailOrSID == 'E':
                    gradescopeColumn = input("Please enter the name of the column containing the student emails (defaults to Email): ")
                    if gradescopeColumn == '':
                        gradescopeColumn = 'Email'
                else:
                    gradescopeColumn = input("Please enter the name of the column containing the student SIDs (defaults to SID): ")
                    if gradescopeColumn == '':
                        gradescopeColumn = 'SID'
                for assignment in gradescopeAssignmentList:
                    scores = getGradescopeScores(assignment, gradescopeColumn)
                    for bundle in scores:
                        canvasAssignment = course.get_assignment(CONFIG['CANVAS_API']['ASSIGNMENTS'][bundle])
                        try:
                            rubric = canvasAssignment.rubric
                        except:
                            print("Could not find rubric for assignment " + bundle)
                            continue
                        for criterion in scores[bundle]:
                            if emailOrSID == 'E':
                                uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion])
                            else:
                                uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], False)
        elif command == 'R':
            courseId = CONFIG['CANVAS_API']['COURSE_ID']
            course = canvas.get_course(courseId)
            localOrUpload = input("Save CSV files locally or upload directly to Canvas? (L/U): ")
            while localOrUpload != 'L' and localOrUpload != 'U':
                localOrUpload = input("Invalid command, please enter L for local or U for upload: ")
            initialAssignment = input("Please input the name of the initial assignment: ")
            resubmissionAssignment = input("Please input the name of the resubmission assignment (default is initial assignemnt name with _Resubmission added to the end: ")
            if resubmissionAssignment == '':
                resubmissionAssignment = initialAssignment + "_Resubmission"
            if localOrUpload == 'L':
                gradescopeColumn = input("Please enter the name of the column containing the student SID (defaults to SID): ")
                if gradescopeColumn == '':
                    gradescopeColumn = 'SID'
                canvasColumn = input("Please enter the name of the column containing the student SID (defaults to Student ID): ")
                if canvasColumn == '':
                    canvasColumn = 'Student ID'
                scores = getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn)
                updateCanvasScores(scores, canvasColumn)

            else:
                emailOrSID = input("Email or SID (E/S): ")
                while emailOrSID != 'E' and emailOrSID != 'S':
                    gradescopeColumn = input("Invalid column, please enter E for email or S for SID: ")
                if emailOrSID == 'E':
                    gradescopeColumn = input("Please enter the name of the column containing the student emails (defaults to Email): ")
                    if gradescopeColumn == '':
                        gradescopeColumn = 'Email'
                else:
                    gradescopeColumn = input("Please enter the name of the column containing the student SIDs (defaults to SID): ")
                    if gradescopeColumn == '':
                        gradescopeColumn = 'SID'
                scores = getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn)
                for bundle in scores:
                    canvasAssignment = course.get_assignment(CONFIG['CANVAS_API']['ASSIGNMENTS'][bundle])
                    try:
                        rubric = canvasAssignment.rubric
                    except:
                        print("Could not find rubric for assignment " + bundle)
                        continue
                    for criterion in scores[bundle]:
                        uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion])
        elif command == 'RM':
            removeColumn = input("Please input the assignment name you would like to remove from the Canvas bundles (must match EXACTLY): ")
            removeCanvasAssignmentLocal(removeColumn)
            print("Finished removing assignment " + removeColumn + " from the Canvas bundle, updated CSV files are located in " + OUTPUT_FILE_PATH)
        input("Press enter to exit")
    except Exception as e:
        print(e)
        input("Press enter to exit")
        exit(1)


