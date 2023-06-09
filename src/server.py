from flask import Flask, request
import os
from flask_cors import CORS
import yaml
from canvasapi import Canvas
import gradescopeUtil

class CanvasServer:
    def __init__(self):
        self.CANVAS = None
        self.CONFIG = None
        self.CANVAS_FILE_PATH = None
        self.GRADESCOPE_FILE_PATH = None
        self.OUTPUT_FILE_PATH = None
        self.API_URL = None
        self.API_KEY = None
    def loadConfig(self):
        with open("config.yaml", 'r') as stream:
            self.CONFIG = yaml.safe_load(stream)

        self.CANVAS_FILE_PATH = self.CONFIG['CANVAS_FOLDER'] + os.sep
        self.GRADESCOPE_FILE_PATH = self.CONFIG['GRADESCOPE_FOLDER'] + os.sep
        self.OUTPUT_FILE_PATH = self.CONFIG['OUTPUT_FOLDER']+ os.sep
        self.API_URL = self.CONFIG['CANVAS_API']['URL']

        self.API_KEY = self.CONFIG['CANVAS_API']['KEY']
        self.CANVAS = Canvas(self.API_URL, self.API_KEY)

canvasServer = CanvasServer()

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "<h1>Hello!</h1>"

@app.route('/uploadGrade')
def uploadGrade():
    print("Uploading scores...")
    canvasServer.loadConfig()
    courseId = canvasServer.CONFIG['CANVAS_API']['COURSE_ID']
    course = canvasServer.CANVAS.get_course(courseId)
    returnMsg = ""
    gradescopeAssignmentList = os.listdir(canvasServer.GRADESCOPE_FILE_PATH)
    emailOrSID = request.args.get('emailOrSID')
    gradescopeColumn = request.args.get('gradescopeColumn')
    print("Found " + str(len(gradescopeAssignmentList)) + " assignments in gradescope folder")
    for assignment in gradescopeAssignmentList:
        if "_Resubmission" in assignment:
            print("Skipping resubmission assignment: " + assignment)
            continue
        try:
            scores = gradescopeUtil.getGradescopeScores(assignment, gradescopeColumn, canvasServer.GRADESCOPE_FILE_PATH)
        except NotADirectoryError:
            print("Skipping " + assignment + " because it is not a directory")
            continue
        print("Found " + str(len(scores)) + " bundles in " + assignment)
        for bundle in scores:
            if bundle not in canvasServer.CONFIG['CANVAS_API']['ASSIGNMENTS']:
                print("Assignment " + bundle + " not found in config.yaml (meaning it has no rubric on canvas)")
                returnMsg += "Assignment " + bundle + " not found in config.yaml (meaning it has no rubric on canvas)\n"
                continue
            try:
                canvasAssignment = course.get_assignment(canvasServer.CONFIG['CANVAS_API']['ASSIGNMENTS'][bundle])
                rubric = canvasAssignment.rubric
                print("Rubric found for assignment: " + canvasAssignment.name)
                returnMsg += "Rubric found for assignment: " + canvasAssignment.name + "\n"
            except Exception as e:
                print(e)
                print("Rubric not found for assignment: " + canvasAssignment.name)
                returnMsg += "Rubric not found for assignment: " + canvasAssignment.name + "\n"
                continue
            for criterion in scores[bundle]:
                try:
                    if emailOrSID == "Email":
                        gradescopeUtil.uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], True,
                                                          canvasServer.CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                          canvasServer.CONFIG['CANVAS_API']['SID_ENDPOINT'])
                    else:
                        gradescopeUtil.uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], False,
                                                          canvasServer.CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                          canvasServer.CONFIG['CANVAS_API']['SID_ENDPOINT'])
                except Exception as e:
                    print(e)
                    print("Error uploading scores for assignment: " + canvasAssignment.name)
                    returnMsg += "Error uploading scores for assignment: " + canvasAssignment.name + "\n"
                    continue
    print("Done!")
    return "Done!"

@app.route('/localGrade')
def localGrade():
    print("Outputting scores to local CSV files...")
    canvasServer.loadConfig()
    gradescopeAssignmentList = os.listdir(canvasServer.GRADESCOPE_FILE_PATH)
    gradescopeColumn = request.args.get('gradescopeColumn')
    canvasColumn = request.args.get('canvasColumn')
    for assignment in gradescopeAssignmentList:
        if "_Resubmission" in assignment:
            print("Skipping resubmission assignment: " + assignment)
            continue
        try:
            scores = gradescopeUtil.getGradescopeScores(assignment, gradescopeColumn, canvasServer.GRADESCOPE_FILE_PATH)
        except NotADirectoryError:
            print("Skipping " + assignment + " because it is not a directory")
            continue
        try:
            gradescopeUtil.updateCanvasScores(scores, canvasColumn, canvasServer.CANVAS_FILE_PATH, canvasServer.OUTPUT_FILE_PATH)
        except Exception as e:
            print(e)
            print("Error outputting scores for assignment: " + assignment)
            continue
    print("Done!")
    return "Done!"

@app.route('/uploadResubmission')
def uploadResubmission():
    print("Uploading resubmission scores...")
    canvasServer.loadConfig()
    courseId = canvasServer.CONFIG['CANVAS_API']['COURSE_ID']
    course = canvasServer.CANVAS.get_course(courseId)
    initialAssignment = request.args.get('initialAssignment')
    emailOrSID = request.args.get('emailOrSID')
    gradescopeColumn = request.args.get('gradescopeColumn')
    resubmissionAssignment = initialAssignment + "_Resubmission"
    try:
        scores = gradescopeUtil.getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn, canvasServer.GRADESCOPE_FILE_PATH)
    except NotADirectoryError:
        print("Skipping " + initialAssignment + " because it is not a directory")
        return "Done!"
    for bundle in scores:
        if bundle not in canvasServer.CONFIG['CANVAS_API']['ASSIGNMENTS']:
            print("Assignment " + bundle + " not found in config.yaml")
            continue
        canvasAssignment = course.get_assignment(canvasServer.CONFIG['CANVAS_API']['ASSIGNMENTS'][bundle])
        try:
            rubric = canvasAssignment.rubric
            print("Rubric found for assignment: " + canvasAssignment.name)
        except Exception as e:
            print("Rubric not found for assignment: " + canvasAssignment.name)
            continue
        for criterion in scores[bundle]:
            try:
                if emailOrSID == "Email":
                    gradescopeUtil.uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], True,
                                                      canvasServer.CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                      canvasServer.CONFIG['CANVAS_API']['SID_ENDPOINT'])
                else:
                    gradescopeUtil.uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], False,
                                                      canvasServer.CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                      canvasServer.CONFIG['CANVAS_API']['SID_ENDPOINT'])
            except Exception as e:
                print(e)
                print("Error uploading scores for assignment: " + canvasAssignment.name)
                continue
    print("Done!")
    return "Done!"

@app.route('/localResubmission')
def localResubmission():
    print("Outputting resubmission scores to local CSV files...")
    canvasServer.loadConfig()
    initialAssignment = request.args.get('initialAssignment')
    resubmissionAssignment = initialAssignment + "_Resubmission"
    gradescopeColumn = request.args.get('gradescopeColumn')
    canvasColumn = request.args.get('canvasColumn')
    try:
        scores = gradescopeUtil.getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn, canvasServer.GRADESCOPE_FILE_PATH)
    except NotADirectoryError:
        print("Skipping " + initialAssignment + " because it is not a directory")
        return "Done!"
    try:
        gradescopeUtil.updateCanvasScores(scores, canvasColumn, canvasServer.CANVAS_FILE_PATH, canvasServer.OUTPUT_FILE_PATH)
    except Exception as e:
        print(e)
        print("Error outputting scores for assignment: " + initialAssignment)
        return "Done!"
    print("Done!")
    return "Done!"

@app.route('/courseInfo')
def courseInfo():
    print("Getting course info...")
    canvasServer.loadConfig()
    courseName = request.args.get('courseName')
    yamlInfo = ""
    for course in canvasServer.CANVAS.get_courses():
        try:
            if course.name == courseName:
                print("Course name: ", course.name)
                #tab indentation is forbidden in yaml files
                yamlInfo += "  COURSE_ID: " + str(course.id) + "\n  ASSIGNMENTS:\n"
                for assignment in course.get_assignments():
                    try:
                        rubric = assignment.rubric
                        print(assignment.name + ": " + str(assignment.id))
                        yamlInfo += "    " + assignment.name + ": " + str(assignment.id) + "\n"
                    except Exception as e:
                        continue
                break
        except Exception as e:
            print(e)
            continue
    with open("config.yaml", "r") as f:
        lines = f.readlines()
    #delete the old file
    os.remove("config.yaml")
    with open("config.yaml", "w") as f:
        for line in lines:
            if "KEY:" in line:
                f.write(line)
                break
            f.write(line)
        f.write("\n" + yamlInfo)
    print("Done!")
    return "Done!"

@app.route('/localRemove')
def localRemove():
    print("Removing assignment from local CSV files...")
    canvasServer.loadConfig()
    removeColumn = request.args.get('removeColumn')
    try:
        gradescopeUtil.removeCanvasAssignmentLocal(removeColumn, canvasServer.CANVAS_FILE_PATH, canvasServer.OUTPUT_FILE_PATH)
    except Exception as e:
        print(e)
        print("Error removing assignment from local CSV files.")
        return "Done!"
    print("Done!")
    return "Done!"

@app.route('/currentCourse')
def currentCourse():
    print("Getting current course...")
    canvasServer.loadConfig()
    try:
        courseId = canvasServer.CONFIG['CANVAS_API']['COURSE_ID']
        course = canvasServer.CANVAS.get_course(courseId)
        courseInfo = course.name + "\n"
        for assignment in canvasServer.CONFIG['CANVAS_API']['ASSIGNMENTS']:
            courseInfo += "\n" + assignment
    except Exception as e:
        print(e)
        print("Error getting current course.")
        return "No course set up yet. Please set up a course first."
    return courseInfo

if __name__ == '__main__':
    from waitress import serve
    print("Now serving on port 7777...")
    try:
        serve(app, host="127.0.0.1", port=7777)
    except Exception as e:
        print(e)
        input("Error: Press enter to exit.")
