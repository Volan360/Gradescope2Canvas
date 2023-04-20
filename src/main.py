import os
import csv

CANVAS_FILE_PATH = "../Canvas/"
GRADESCOPE_FILE_PATH = "../Gradescope/"

if __name__ == "__main__":
    #get a list of the file paths in the ../Canvas/ directory
    canvasFileList = os.listdir(CANVAS_FILE_PATH)
    #get a list of the file paths in the ../Gradescope/ directory
    gradescopeFileList = os.listdir(GRADESCOPE_FILE_PATH)
    for gradescopeFile in gradescopeFileList:
        csvFile = open(GRADESCOPE_FILE_PATH + gradescopeFile, 'r')
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:
            print(row['Email'])
        csvFile.close()