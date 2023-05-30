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
    for assignment in gradescopeAssignmentList:
        scores = gradescopeUtil.getGradescopeScores(assignment, gradescopeColumn, canvasServer.GRADESCOPE_FILE_PATH)
        for bundle in scores:
            if bundle not in canvasServer.CONFIG['CANVAS_API']['ASSIGNMENTS']:
                print("Assignment " + bundle + " not found in config.yaml (meaning it has no rubric on canvas)")
                returnMsg += "Assignment " + bundle + " not found in config.yaml (meaning it has no rubric on canvas)\n"
                continue
            canvasAssignment = course.get_assignment(canvasServer.CONFIG['CANVAS_API']['ASSIGNMENTS'][bundle])
            try:
                rubric = canvasAssignment.rubric
                print("Rubric found for assignment: " + canvasAssignment.name)
                returnMsg += "Rubric found for assignment: " + canvasAssignment.name + "\n"
            except:
                print("Rubric not found for assignment: " + canvasAssignment.name)
                returnMsg += "Rubric not found for assignment: " + canvasAssignment.name + "\n"
                continue
            for criterion in scores[bundle]:
                if emailOrSID == "Email":
                    gradescopeUtil.uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], True,
                                                      canvasServer.CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                      canvasServer.CONFIG['CANVAS_API']['SID_ENDPOINT'])
                else:
                    gradescopeUtil.uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], False,
                                                      canvasServer.CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                      canvasServer.CONFIG['CANVAS_API']['SID_ENDPOINT'])

    return "Done!"

@app.route('/localGrade')
def localGrade():
    print("Outputting scores to local CSV files...")
    canvasServer.loadConfig()
    gradescopeAssignmentList = os.listdir(canvasServer.GRADESCOPE_FILE_PATH)
    gradescopeColumn = request.args.get('gradescopeColumn')
    canvasColumn = request.args.get('canvasColumn')
    for assignment in gradescopeAssignmentList:
        scores = gradescopeUtil.getGradescopeScores(assignment, gradescopeColumn, canvasServer.GRADESCOPE_FILE_PATH)
        gradescopeUtil.updateCanvasScores(scores, canvasColumn, canvasServer.CANVAS_FILE_PATH, canvasServer.OUTPUT_FILE_PATH)
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
    scores = gradescopeUtil.getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn, canvasServer.GRADESCOPE_FILE_PATH)
    for bundle in scores:
        if bundle not in canvasServer.CONFIG['CANVAS_API']['ASSIGNMENTS']:
            print("Assignment " + bundle + " not found in config.yaml")
            continue
        canvasAssignment = course.get_assignment(canvasServer.CONFIG['CANVAS_API']['ASSIGNMENTS'][bundle])
        try:
            rubric = canvasAssignment.rubric
            print("Rubric found for assignment: " + canvasAssignment.name)
        except:
            print("Rubric not found for assignment: " + canvasAssignment.name)
            continue
        for criterion in scores[bundle]:
            if emailOrSID == "Email":
                gradescopeUtil.uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], True,
                                                  canvasServer.CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                  canvasServer.CONFIG['CANVAS_API']['SID_ENDPOINT'])
            else:
                gradescopeUtil.uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], False,
                                                  canvasServer.CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                  canvasServer.CONFIG['CANVAS_API']['SID_ENDPOINT'])

    return "Done!"

@app.route('/localResubmission')
def localResubmission():
    print("Outputting resubmission scores to local CSV files...")
    canvasServer.loadConfig()
    initialAssignment = request.args.get('initialAssignment')
    resubmissionAssignment = initialAssignment + "_Resubmission"
    gradescopeColumn = request.args.get('gradescopeColumn')
    canvasColumn = request.args.get('canvasColumn')
    scores = gradescopeUtil.getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn, canvasServer.GRADESCOPE_FILE_PATH)
    gradescopeUtil.updateCanvasScores(scores, canvasColumn, canvasServer.CANVAS_FILE_PATH, canvasServer.OUTPUT_FILE_PATH)
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
                    if assignment.rubric:
                        print(assignment.name + ": " + str(assignment.id))
                        yamlInfo += "    " + assignment.name + ": " + str(assignment.id) + "\n"
                break
        except:
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
    return "Done!"

@app.route('/localRemove')
def localRemove():
    print("Removing assignment from local CSV files...")
    canvasServer.loadConfig()
    removeColumn = request.args.get('removeColumn')
    gradescopeUtil.removeCanvasAssignmentLocal(removeColumn, canvasServer.CANVAS_FILE_PATH, canvasServer.OUTPUT_FILE_PATH)
    return "Done!"


if __name__ == '__main__':
    from waitress import serve
    print("Now serving on port 7777...")
    try:
        serve(app, host="127.0.0.1", port=7777)
    except Exception as e:
        print(e)
        input("Error: Press enter to exit.")
