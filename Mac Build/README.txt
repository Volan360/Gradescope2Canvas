INITIAL SETUP (once at the start of the quarter):

II.Setting up the basic config.yaml file
    1. Open the config.yaml file in a text editor (it's inside the Program folder)
    2. Open your canvas account in a web browser
    3. Click on Settings
    4. Scroll down to "Approved Integrations" and click "+ New Access Token"
    5. Type "Gradescope2Canvas" in the Purpose field, or some other name
    6. Click "Generate Token"
    7. Copy the token that appears and paste it into the config.yaml file, after the colon in the KEY field under CANVAS_API
    8. Save the file

III. Adding a course
    1. Open the config.yaml file in a text editor
    2. If there are any lines under the KEY field in CANVAS_API, delete them
        -Config.yaml should now look something like this (with actual values)
        CANVAS_FOLDER: Canvas
        GRADESCOPE_FOLDER: Gradescope
        OUTPUT_FOLDER: Output
        CANVAS_API:
          URL: https://canvas.instructure.com
          NET_ID_ENDPOINT: login_id
          SID_ENDPOINT: sis_user_id
          KEY: example_key
    3. Save the file
    4. Double-Click the Gradescope2Canvas.command file to run the program
    5. Thes should open up a website page. Find the Course Info section
    6. Type the name of the class you want to add and click "Get Course Info" (exactly as it appears in Canvas)
    7. This will output a courseInfo.txt file
    8. Open the courseInfo.txt file in a text editor, delete all assignments that aren't bundles
    8. Copy-paste the contents of the courseInfo.txt file into the config.yaml file, underneath the KEY field, like so:
          CANVAS_FOLDER: Canvas
          GRADESCOPE_FOLDER: Gradescope
          OUTPUT_FOLDER: Output
          CANVAS_API:
            URL: https://canvas.instructure.com
            NET_ID_ENDPOINT: login_id
            SID_ENDPOINT: sis_user_id
            KEY: example_key
            COURSE_ID: example_id
            ASSIGNMENTS:
              Safety and Format: example_id
              Objective or Purpose or Concepts: example_id
              Exit Quizzes: example_id
              Procedure: example_id
              Observations: example_id
              Data Analysis: example_id
              Argumentation: example_id
    9. Please note that the program only supports 1 course at a time, so if you want to add another course, you will have to
       delete the previous course's info from the config.yaml file and repeat the process above
            -Alternatively, create a new config.yaml and a new Gradescope2Canvas.command file for each course,
             changing the directory in the first line of the Gradescope2Canvas.command file to the directory of the
             corresponding config.yaml file, and then run the Gradescope2Canvas.command file for each course

GRADING:
REMEMBER TO DELETE ALL PREVIOUS ASSIGNMENTS FROM THE CANVAS, GRADESCOPE, AND OUTPUT FOLDERS BEFORE RUNNING THE PROGRAM
IV. Grading an Assignment
    1. On Canvas, add the assignment you want to grade to each of the relevant bundle rubrics
    2. Download the assignment from Gradescope (export evaluation)
    3. Unzip the downloaded file in the Gradescope folder. This should create a folder inside it with several
       .csv files
    4. Rename the folder to the name of the assignment (exactly as it appears in Canvas)
    5. Repeat steps 1-4 for each assignment you want to grade
    6. Double-Click the Gradescope2Canvas.command file to run the program
    7. Find the "Upload Assignments" or "Output grades to CSV files" section and follow the instructions there

V. Processing Resubmissions
   1. Download both the original Gradescope assignment and the resubmission assignment (export evaluation)
   2. Unzip both downloaded files in the Gradescope folder. This should create two folders inside it with several
      .csv files each
   3. Rename the original folder to the name of the assignment (exactly as it appears in Canvas)
   4. Rename the resubmission folder to the name of the assignment, followed by "_Resubmission" (no quotation marks)
   5. Double-Click the Gradescope2Canvas.command file to run the program
   6. Find the "Upload grades for resubmitted assignments" or "Output grades for resubmitted assignments to CSV Files"
      section and follow the instructions there
   7. Please note that the program only supports regrading 1 assignment at a time, so if you want to regrade
      multiple assignments, you will have to repeat steps 1-6 for each assignment

V. Removing an assignment from a Canvas bundles
    1. Have the CSV file for each bundle assingment ready in the Canvas folder
    2. Double-Click the Gradescope2Canvas.command file to run the program
    3. Find the "Remove grades from Canvas CSV files" section and follow the instructions there
    4. If you wish to repeat this process with other assignments, move the .csv files from the Output
       folder into the Canvas folder, and repeat steps 2-4 (you will have to delete the previous .csv files
       from the Canvas folder before repeating the process)
    5. Please note that the program does not support removing assignments from Canvas directly, so you will have
       to upload the .csv files to Canvas manually (after removing the assignment from the rubrics of each bundle)
