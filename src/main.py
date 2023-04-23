import os
import csv

CANVAS_FILE_PATH = "../Canvas/"
GRADESCOPE_FILE_PATH = "../Gradescope/"
OUTPUT_FILE_PATH = "../Output/"
def getGradescopeScores(assignment):
    gradeScopeScores = {}
    for question in os.listdir(GRADESCOPE_FILE_PATH + assignment):
        csvFile = open(GRADESCOPE_FILE_PATH + assignment + '/' + question, 'r')
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:
            if(row['Name'] == '' or row['Tags'] == None):
                continue
            for tag in row['Tags'].split(','):
                if tag not in gradeScopeScores:
                    gradeScopeScores[tag] = {}
                if assignment not in gradeScopeScores[tag]:
                    gradeScopeScores[tag][assignment] = {}
                if row['Name'] not in gradeScopeScores[tag][assignment]:
                    gradeScopeScores[tag][assignment][row['Name']] = float(row['Score'])
                else:
                    gradeScopeScores[tag][assignment][row['Name']] += float(row['Score'])
        csvFile.close()
    return gradeScopeScores

def updateCanvasScores(gradeScopeScores):
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
            fieldnames.append(assignment)
        csvWriter = csv.DictWriter(csvOutput, fieldnames=fieldnames)
        csvWriter.writeheader()
        for assignment in gradeScopeScores[tag]:
            for row in csvReader:
                if row['Student Name'] in gradeScopeScores[tag][assignment]:
                    print(row['Student Name'] + " " + tag + " " + assignment + " " + str(gradeScopeScores[tag][assignment][row['Student Name']]))
                    row[assignment] = str(gradeScopeScores[tag][assignment][row['Student Name']])
                csvWriter.writerow(row)
        csvInput.close()
        csvOutput.close()

if __name__ == "__main__":
    #get a list of the file paths in the ../Canvas/ directory
    canvasFileList = os.listdir(CANVAS_FILE_PATH)
    #get a list of the file paths in the ../Gradescope/ directory
    gradescopeAssignmentList = os.listdir(GRADESCOPE_FILE_PATH)
    for assignment in gradescopeAssignmentList:
        scores = getGradescopeScores(assignment)
        print(scores)
        updateCanvasScores(scores)
