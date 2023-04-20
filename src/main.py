import os
import csv

CANVAS_FILE_PATH = "../Canvas/"
GRADESCOPE_FILE_PATH = "../Gradescope/"

if __name__ == "__main__":
    #get a list of the file paths in the ../Canvas/ directory
    canvasFileList = os.listdir(CANVAS_FILE_PATH)
    #get a list of the file paths in the ../Gradescope/ directory
    gradescopeFileList = os.listdir(GRADESCOPE_FILE_PATH)
    gradeScopeScores = {}
    for gradescopeFile in gradescopeFileList:
        csvFile = open(GRADESCOPE_FILE_PATH + gradescopeFile, 'r')
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:
            if(row['Name'] == '' or row['Tags'] == None):
                continue
            if row['Email'] not in gradeScopeScores:
                gradeScopeScores[row['Email']] = {}
            for tag in row['Tags'].split(','):
                if tag not in gradeScopeScores[row['Email']]:
                    gradeScopeScores[row['Email']][tag] = float(row['Score'])
                else:
                    gradeScopeScores[row['Email']][tag] += float(row['Score'])
    for studentScores in gradeScopeScores:
        print(gradeScopeScores[studentScores])

        csvFile.close()