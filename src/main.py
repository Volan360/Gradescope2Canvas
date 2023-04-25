import os
import csv
#Add in functionality to choose what column name you will use to match the students on Canvas and Gradescope
#Add in another script/functionality to remove a column from gradescope
#Students can resubit assignments, as a separate Gradescope assignment but this will update the existing Canvas assignment
#For resubmissions, the input folder for Gradescope will have the folder with the original assignment name and then a folder original assignment name + "_Resubmission"
#For resubmissions, if the student has a score of > 0 for a problem they already had a score for, then the score FOR THE ENTIRE ASSINGMENT WILL BE A 0
CANVAS_FILE_PATH = "../Canvas/"
GRADESCOPE_FILE_PATH = "../Gradescope/"
OUTPUT_FILE_PATH = "../Output/"
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
        for field in csvReader.fieldnames:
            fieldnames.append(field)
        for assignment in gradeScopeScores[tag]:
            if assignment not in fieldnames:
                confirmation = input("Would you like to add the assignment " + assignment + " to the Canvas file for " + tag +"? (y/n): ")
                if confirmation == 'y':
                    fieldnames.append(assignment)
                else:
                    print("Canceling grade conversion, please delete all files in the Output folder and try again")
                    return
            else:
                confirmation = input("The assignment " + assignment + " already exists in the Canvas file for " + tag + ", would you like to modify it? (y/n)")
                if confirmation == 'n':
                    print("Canceling grade conversion, please delete all files in the Output folder and try again")
                    return
        csvWriter = csv.DictWriter(csvOutput, fieldnames=fieldnames)
        csvWriter.writeheader()
        for assignment in gradeScopeScores[tag]:
            for row in csvReader:
                if row[canvasColumn] in gradeScopeScores[tag][assignment]:
                    #print(row[canvasColumn] + " " + tag + " " + assignment + " " + str(gradeScopeScores[tag][assignment][row[canvasColumn]]))
                    row[assignment] = str(gradeScopeScores[tag][assignment][row[canvasColumn]])
                csvWriter.writerow(row)
        csvInput.close()
        csvOutput.close()

if __name__ == "__main__":
    #get a list of the file paths in the ../Canvas/ directory
    canvasFileList = os.listdir(CANVAS_FILE_PATH)
    #get a list of the file paths in the ../Gradescope/ directory
    gradescopeAssignmentList = os.listdir(GRADESCOPE_FILE_PATH)
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
