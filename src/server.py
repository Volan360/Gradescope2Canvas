from flask import Flask, render_template, request
import urllib.parse
import os
from flask_cors import CORS
import yaml
from canvasapi import Canvas
import gradescopeUtil

with open("config.yaml", 'r') as stream:
    CONFIG = yaml.safe_load(stream)

CANVAS_FILE_PATH = CONFIG['CANVAS_FOLDER'] + os.sep
GRADESCOPE_FILE_PATH = CONFIG['GRADESCOPE_FOLDER'] + os.sep
OUTPUT_FILE_PATH = CONFIG['OUTPUT_FOLDER']+ os.sep
API_URL = CONFIG['CANVAS_API']['URL']

apiKey = CONFIG['CANVAS_API']['KEY']
canvas = Canvas(API_URL, apiKey)


app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "<h1>Hello!</h1>"

@app.route('/uploadGrade')
def uploadGrade():
    courseId = CONFIG['CANVAS_API']['COURSE_ID']
    course = canvas.get_course(courseId)
    print("Uploading scores...")
    returnMsg = ""
    gradescopeAssignmentList = os.listdir(GRADESCOPE_FILE_PATH)
    emailOrSID = request.args.get('emailOrSID')
    gradescopeColumn = request.args.get('gradescopeColumn')
    for assignment in gradescopeAssignmentList:
        scores = gradescopeUtil.getGradescopeScores(assignment, gradescopeColumn, GRADESCOPE_FILE_PATH)
        for bundle in scores:
            canvasAssignment = course.get_assignment(CONFIG['CANVAS_API']['ASSIGNMENTS'][bundle])
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
                                                      CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                      CONFIG['CANVAS_API']['SID_ENDPOINT'])
                else:
                    gradescopeUtil.uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], False,
                                                      CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                      CONFIG['CANVAS_API']['SID_ENDPOINT'])

    return "Done!"

@app.route('/localGrade')
def localGrade():
    print("Outputting scores to local CSV files...")
    gradescopeAssignmentList = os.listdir(GRADESCOPE_FILE_PATH)
    gradescopeColumn = request.args.get('gradescopeColumn')
    canvasColumn = request.args.get('canvasColumn')
    for assignment in gradescopeAssignmentList:
        scores = gradescopeUtil.getGradescopeScores(assignment, gradescopeColumn, GRADESCOPE_FILE_PATH)
        gradescopeUtil.updateCanvasScores(scores, canvasColumn, CANVAS_FILE_PATH, OUTPUT_FILE_PATH)
    return "Done!"

@app.route('/uploadResubmission')
def uploadResubmission():
    courseId = CONFIG['CANVAS_API']['COURSE_ID']
    course = canvas.get_course(courseId)
    print("Uploading resubmission scores...")
    initialAssignment = request.args.get('initialAssignment')
    emailOrSID = request.args.get('emailOrSID')
    gradescopeColumn = request.args.get('gradescopeColumn')
    resubmissionAssignment = initialAssignment + "_Resubmission"
    scores = gradescopeUtil.getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn, GRADESCOPE_FILE_PATH)
    for bundle in scores:
        canvasAssignment = course.get_assignment(CONFIG['CANVAS_API']['ASSIGNMENTS'][bundle])
        try:
            rubric = canvasAssignment.rubric
            print("Rubric found for assignment: " + canvasAssignment.name)
        except:
            print("Rubric not found for assignment: " + canvasAssignment.name)
            continue
        for criterion in scores[bundle]:
            if emailOrSID == "Email":
                gradescopeUtil.uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], True,
                                                  CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                  CONFIG['CANVAS_API']['SID_ENDPOINT'])
            else:
                gradescopeUtil.uploadCanvasScores(canvasAssignment, criterion, scores[bundle][criterion], False,
                                                  CONFIG['CANVAS_API']['NET_ID_ENDPOINT'],
                                                  CONFIG['CANVAS_API']['SID_ENDPOINT'])

    return "Done!"

@app.route('/localResubmission')
def localResubmission():
    print("Outputting resubmission scores to local CSV files...")
    initialAssignment = request.args.get('initialAssignment')
    resubmissionAssignment = initialAssignment + "_Resubmission"
    gradescopeColumn = request.args.get('gradescopeColumn')
    canvasColumn = request.args.get('canvasColumn')
    scores = gradescopeUtil.getRegradeScores(initialAssignment, resubmissionAssignment, gradescopeColumn, GRADESCOPE_FILE_PATH)
    gradescopeUtil.updateCanvasScores(scores, canvasColumn, CANVAS_FILE_PATH, OUTPUT_FILE_PATH)
    return "Done!"

@app.route('/courseInfo')
def courseInfo():
    print("Getting course info...")
    courseName = request.args.get('courseName')
    yamlInfo = ""
    for course in canvas.get_courses():
        try:
            if course.name == courseName:
                print("Course name: ", course.name)
                yamlInfo += "Course_ID: " + str(course.id) + "\nASSIGNMENTS:\n"
                for assignment in course.get_assignments():
                    print(assignment.name + ": " + str(assignment.id))
                    yamlInfo += "\t" + assignment.name + ": " + str(assignment.id) + "\n"
                break
        except:
            continue
    yamlFile = open("courseInfo.txt", "w")
    yamlFile.write(yamlInfo)
    yamlFile.close()
    return "Done!"

@app.route('/localRemove')
def localRemove():
    print("Removing assignment from local CSV files...")
    removeColumn = request.args.get('removeColumn')
    gradescopeUtil.removeCanvasAssignmentLocal(removeColumn, CANVAS_FILE_PATH, OUTPUT_FILE_PATH)
    return "Done!"


if __name__ == '__main__':
    from waitress import serve
    print("Now serving on port 7777...")
    try:
        serve(app, host="127.0.0.1", port=7777)
    except Exception as e:
        print(e)
        input("Error: Press enter to exit.")
