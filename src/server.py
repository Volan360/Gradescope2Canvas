from flask import Flask, render_template, request
import urllib.parse
import os
from flask_cors import CORS
import yaml
from canvasapi import Canvas
import gradescopeUtil

with open("config.yaml", 'r') as stream:
    CONFIG = yaml.safe_load(stream)

CANVAS_FILE_PATH = CONFIG['CANVAS_FOLDER']
GRADESCOPE_FILE_PATH = CONFIG['GRADESCOPE_FOLDER']
OUTPUT_FILE_PATH = CONFIG['OUTPUT_FOLDER']
API_URL = CONFIG['CANVAS_API']['URL']

apiKey = CONFIG['CANVAS_API']['KEY']
canvas = Canvas(API_URL, apiKey)
courseId = CONFIG['CANVAS_API']['COURSE_ID']
course = canvas.get_course(courseId)


app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "<h1>Hello!</h1>"

@app.route('/uploadGrade')
def uploadGrade():
    return

@app.route('/localGrade')
def localGrade():
    return

@app.route('/uploadResubmission')
def uploadResubmission():
    return

@app.route('/localResubmission')
def localResubmission():
    return

@app.route('/courseInfo')
def courseInfo():
    courseName = request.args.get('courseName')
    yamlInfo = ""
    for course in canvas.get_courses():
        try:
            if course.name == courseName:
                #print("Course name: ", course.name)
                yamlInfo += "Course_ID: " + str(course.id) + "\nASSIGNMENTS:\n"
                for assignment in course.get_assignments():
                    #print(assignment.name + ": " + str(assignment.id))
                    yamlInfo += "\t" + assignment.name + ": " + str(assignment.id) + "\n"
                break
        except:
            continue
    yamlFile = open("courseInfo.txt", "w")
    yamlFile.write(yamlInfo)
    yamlFile.close()
    return yamlInfo

@app.route('/localRemove')
def localRemove():
    return


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="127.0.0.1", port=8675309)
