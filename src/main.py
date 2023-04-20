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
            if row['Name'] not in gradeScopeScores:
                gradeScopeScores[row['Name']] = {}
            if gradescopeFile not in gradeScopeScores[row['Name']]:
                gradeScopeScores[row['Name']][gradescopeFile] = {}
            for tag in row['Tags'].split(','):
                if tag not in gradeScopeScores[row['Name']][gradescopeFile]:
                    gradeScopeScores[row['Name']][gradescopeFile][tag] = float(row['Score'])
                else:
                    gradeScopeScores[row['Name']][gradescopeFile][tag] += float(row['Score'])
        csvFile.close()

    #for student in gradeScopeScores:
        # for assignment in gradeScopeScores[student]:
        #     for tag in gradeScopeScores[student][assignment]:
        #         #open the Canvas file Rubric Scores [tag].csv
        #         csvFile = open(CANVAS_FILE_PATH + "Rubric Scores " + tag + ".csv", 'r')
        #         csvReader = csv.DictReader(csvFile)
        #         #check if the assignment is one of the columns
        #         if assignment not in csvReader.fieldnames:
        #             #if not, add it
        #             csvReader.fieldnames.insert(assignment)
        #         #find the row with the student's name
        #         for row in csvReader:
        #             if row['Student'] == student:
        #                 #add the score to the row
        #                 row[assignment] = gradeScopeScores[student][assignment][tag]
        #                 break

