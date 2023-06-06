import os
import csv
from canvasapi import Canvas
import yaml

with open("config.yaml", 'r', encoding='utf-8-sig') as stream:
    CONFIG = yaml.safe_load(stream)

CANVAS_FILE_PATH = CONFIG['CANVAS_FOLDER']
GRADESCOPE_FILE_PATH = CONFIG['GRADESCOPE_FOLDER']
OUTPUT_FILE_PATH = CONFIG['OUTPUT_FOLDER']
API_URL = CONFIG['CANVAS_API']['URL']

#Make a function called "Get Course Info" that takes in a course name and returns the course ID, as well as assignment IDs and names
def getGradescopeScores(assignment, gradescopeColumn, gradescopeFilePath=GRADESCOPE_FILE_PATH):
    gradeScopeScores = {}
    for question in os.listdir(gradescopeFilePath + assignment):
        csvFile = open(gradescopeFilePath + assignment + os.sep + question, 'r', encoding='utf-8-sig')
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
def updateCanvasScores(gradeScopeScores, canvasColumn,canvasFilePath=CANVAS_FILE_PATH, outputFilePath=OUTPUT_FILE_PATH):
    for tag in gradeScopeScores:
        try:
            csvInput = open(canvasFilePath + "Rubric Scores " + tag + ".csv", 'r', encoding='utf-8-sig')
        except:
            print("Could not find the file: " + canvasFilePath + "Rubric Scores " + tag + ".csv")
            continue
        csvOutput = open(outputFilePath + "Updated Rubric Scores " + tag + ".csv", 'w', newline='')
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
                fieldnames.append("Points: " + assignment)
        csvWriter = csv.DictWriter(csvOutput, fieldnames=fieldnames)
        csvWriter.writeheader()
        for assignment in gradeScopeScores[tag]:
            for row in csvReader:
                try:
                    sid = int(row[canvasColumn])
                except ValueError:
                    print("Could not convert " + row[canvasColumn] + " to an integer")
                    continue
                if sid in gradeScopeScores[tag][assignment].keys():
                    row["Points: " + assignment] = str(int(gradeScopeScores[tag][assignment][sid]))
                else:
                    row["Points: " + assignment] = '0'
                for field in skipFields:
                    row.pop(field)
                csvWriter.writerow(row)
        csvInput.close()
        csvOutput.close()

#CHANGE THIS FUNCTION TO USE THE CANVAS API INSTEAD OF THE CSV FILES
def removeCanvasAssignmentLocal(assignment, canvasFilePath=CANVAS_FILE_PATH, outputFilePath=OUTPUT_FILE_PATH):
    assignment = "Points: " + assignment
    for rubricScoresFile in os.listdir(canvasFilePath):
        try:
            csvInput = open(canvasFilePath + rubricScoresFile, 'r', encoding='utf-8-sig')
        except:
            print("Could not find the file: " + canvasFilePath + rubricScoresFile)
            continue
        csvOutput = open(outputFilePath + "Updated " + rubricScoresFile, 'w', newline='')
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
def getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn, gradescopeFilePath=GRADESCOPE_FILE_PATH):
    gradescopeScores = {}
    for question in os.listdir(gradescopeFilePath + initialAssignment):
        initialReader = csv.DictReader(open(gradescopeFilePath + initialAssignment + os.sep + question, 'r', encoding='utf-8-sig'))
        resubmissionReader = csv.DictReader(open(gradescopeFilePath + resubmissionAssignment + os.sep + question, 'r', encoding='utf-8-sig'))
        initialScores = {}
        resubmissionScores = {}
        tags = []
        for row in initialReader:
            if not row[gradescopeColumn] or not row['Tags']:
                continue
            for tag in row['Tags'].split(','):
                if tag not in gradescopeScores:
                    gradescopeScores[tag] = {}
                if initialAssignment not in gradescopeScores[tag]:
                    gradescopeScores[tag][initialAssignment] = {}
            if '@' in row[gradescopeColumn]:
                userLogin = row[gradescopeColumn].split('@')[0]
            else:
                userLogin = int(row[gradescopeColumn])
            if not userLogin in initialScores:
                initialScores[userLogin] = {}
            initialScores[userLogin][question] = float(row['Score'])
            tags = row['Tags'].split(',')
            break

        for row in initialReader:
            if not row[gradescopeColumn] or not row['Tags']:
                continue
            if '@' in row[gradescopeColumn]:
                userLogin = row[gradescopeColumn].split('@')[0]
            else:
                userLogin = int(row[gradescopeColumn])
            if not userLogin in initialScores:
                initialScores[userLogin] = {}
            initialScores[userLogin][question] = float(row['Score'])
        for row in resubmissionReader:
            if not row[gradescopeColumn] or not row['Tags']:
                continue
            if '@' in row[gradescopeColumn]:
                userLogin = row[gradescopeColumn].split('@')[0]
            else:
                userLogin = int(row[gradescopeColumn])
            if not userLogin in resubmissionScores:
                resubmissionScores[userLogin] = {}
            resubmissionScores[userLogin][question] = float(row['Score'])
        for student in resubmissionScores:
            if student not in initialScores.keys():
                print("Found a student who did not submit the initial assignment: " + str(student) + " on " + question
                      + " adding points for their submission to the initial assignment")
                initialScores[student] = {question: resubmissionScores[student][question]}
                continue
            if initialScores[student][question] > 0 and resubmissionScores[student][question] > 0:
                print(str(student) + " cheated on " + question, "setting resubmission score for this question to 0")
                print("Initial Score: " + str(initialScores[student][question]))
                print("Resubmission Score: " + str(resubmissionScores[student][question]))
            else:
                initialScores[student][question] += resubmissionScores[student][question]

        for student in initialScores:
            for tag in tags:
                if student not in gradescopeScores[tag][initialAssignment]:
                    gradescopeScores[tag][initialAssignment][student] = initialScores[student][question]
                else:
                    gradescopeScores[tag][initialAssignment][student] += initialScores[student][question]
    return gradescopeScores

def uploadCanvasScores(assignment, criterionName, assignmentScores, byEmailPrefix=True,
                       netIDEnpoint=CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],sidEndpoint=CONFIG['CANVAS_API']['SID_ENDPOINT']):
    criterion_id = ""
    for criterion in assignment.rubric:
        if criterion['description'] == criterionName:
            criterion_id = criterion['id']
    for submission in assignment.get_submissions(include=['rubric_assessment', 'user']):
        try:
            if byEmailPrefix:
                matchColumn = submission.user[netIDEnpoint]
            else:
                matchColumn = int(submission.user[sidEndpoint])
        except Exception as e:
            print(e)
            print("Could not find the email prefix or SID for " + submission.user['short_name'] + " for " + assignment.name + ", skipping")
            continue
        try:
            submission.rubric_assessment[criterion_id]['points'] = assignmentScores[matchColumn]
            submission.edit(rubric_assessment=submission.rubric_assessment)
            print("Successfully uploaded the score for " + submission.user['short_name'] + " for " + assignment.name)
        except Exception as e:
            if isinstance(e, KeyError):
                print(submission.user['short_name'] + " did not submit the assignment or this assignment doesn't exist in their submission")
            else:
                print(e)
                print("Failed to upload the score for " + submission.user['short_name'] + " for " + assignment.name + ", setting to 0")
            try:
                submission.rubric_assessment[criterion_id]['points'] = 0
                submission.edit(rubric_assessment=submission.rubric_assessment)
                print("Successfully set the score for " + submission.user['short_name'] + " for " + assignment.name + " to 0, student didn't submit")
            except Exception as e:
                print(e)
                print("Failed to set the score for " + submission.user['short_name'] + " for " + assignment.name + " to 0")
                if "rubric_assessment'" in str(e):
                    print("This is likely because the student has no submission for the bundle, creating an empty submission")
                    try:
                        zeroedRubricAssessment = {}
                        for criterion in assignment.rubric:
                            zeroedRubricAssessment[criterion['id']] = {'points': 0}
                        try:
                            zeroedRubricAssessment[criterion_id]['points'] = assignmentScores[matchColumn]
                        except Exception as a:
                            zeroedRubricAssessment[criterion_id] = {'points': 0}
                        submission.edit(submission={'posted_grade': 0, 'rubric_assessment': zeroedRubricAssessment})
                        print("Successfully created an empty submission for " + submission.user['short_name'] + " for " + assignment.name)
                    except Exception as e:
                        print(e)
                        print("Failed to create an empty submission for " + submission.user['short_name'] + " for " + assignment.name)
                elif isinstance(e, KeyError):
                    print(criterionName + " does not exist in " + submission.user['short_name']+ "'s submission " + ", trying to create it first")
                    try:
                        try:
                            submission.rubric_assessment[criterion_id] = {'points': assignmentScores[matchColumn]}
                        except Exception as a:
                            submission.rubric_assessment[criterion_id] = {'points': 0}
                        submission.edit(rubric_assessment=submission.rubric_assessment)
                        print("Successfully created the criterion " + criterionName + " for " + submission.user['short_name'] + " for " + assignment.name)
                    except Exception as e:
                        print(e)
                        print("Failed to create the criterion " + criterionName + " for " + submission.user['short_name'] + " for " + assignment.name + ", could not upload score")

    for submission in assignment.get_submissions(include=['rubric_assessment', 'user']):
        try:
            totalScore = 0
            for criterion in submission.rubric_assessment:
                if 'points' in submission.rubric_assessment[criterion]:
                    totalScore += submission.rubric_assessment[criterion]['points']
            submission.edit(submission={'posted_grade': totalScore})
            print("Successfully set the total score for " + submission.user['short_name'] + " for " + assignment.name)
        except Exception as e:
            print(e)
            print("Failed set the total score " + submission.user['short_name'] + " setting to 0")
            try:
                submission.edit(submission={'posted_grade': 0})
            except Exception as e:
                print(e)
                print("Failed to set the total score to 0 for " + submission.user['short_name'])
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


