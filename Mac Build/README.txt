INITIAL SETUP (once at the start of the quarter):
I. Setting up the command file
    1. Copy the absolute path of the Program folder in this directory (drag and drop that folder into the Terminal app)
    2. Open the Gradescope2Canvas.command file in a text editor
    3. Replace the path in the first line with the path you copied
        - The first line should now be something like `cd /Path/To/Program/Folder` (without quotes and with your actual path)
    4. Save the file

II.Setting up the basic config.yaml file
    1. Open the config.yaml file in a text editor (it's inside the Program folder)
    2. Copy the absolute paths of the Canvas, Gradescope, and Output folders and paste them into the corresponding
       config.yaml fields, after the colon
            - Example:
              CANVAS_FOLDER: \\wsl$\Ubuntu\home\abdel\repos\Gradescope2Canvas\Canvas
              GRADESCOPE_FOLDER: \\wsl$\Ubuntu\home\abdel\repos\Gradescope2Canvas\Gradescope
              OUTPUT_FOLDER: \\wsl$\Ubuntu\home\abdel\repos\Gradescope2Canvas\Output
    3. Open your canvas account in a web browser
    4. Click on Settings
    5. Scroll down to "Approved Integrations" and click "+ New Access Token"
    6. Type "Gradescope2Canvas" in the Purpose field, or some other name
    7. Click "Generate Token"
    8. Copy the token that appears and paste it into the config.yaml file, after the colon in the KEY field under CANVAS_API
    9. Save the file

III. Adding a course
    1. Open the config.yaml file in a text editor
    2. If there are any lines under the KEY field in CANVAS_API, delete them
        -Config.yaml should now look something like this (with actual values)
        CANVAS_FOLDER: example\path
        GRADESCOPE_FOLDER: example\path
        OUTPUT_FOLDER: example\path
        CANVAS_API:
          URL: https://canvas.instructure.com
          NET_ID_ENDPOINT: login_id
          SID_ENDPOINT: sis_user_id
          KEY: example_key
    3. Save the file
    4. Double-Click the Gradescope2Canvas.command file to run the program
    5. Type "CI" and press enter (no quotation marks)
    6. Type the name of the class you want to add and press enter (exactly as it appears in Canvas)
    7. This will output a courseInfo.txt file
    8. Open the courseInfo.txt file in a text editor, delete all assignments that aren't bundles
    8. Copy-paste the contents of the courseInfo.txt file into the config.yaml file, underneath the KEY field, like so:
          CANVAS_FOLDER: example\path
          GRADESCOPE_FOLDER: example\path
          OUTPUT_FOLDER: example\path
          CANVAS_API:
            URL: https://canvas.instructure.com
            NET_ID_ENDPOINT: login_id
            SID_ENDPOINT: sis_user_id
            KEY: example_key
            COURSE_ID: 44070000000049233
            ASSIGNMENTS:
              Safety and Format: 44070000001166714
              Objective or Purpose or Concepts: 44070000001166700
              Exit Quizzes: 44070000001166680
              Procedure: 44070000001166705
              Observations: 44070000001166701
              Data Analysis: 44070000001166677
              Argumentation: 44070000001166674
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
    7. Type "G" and press enter (no quotation marks), and follow the prompts
        - If you select local grading, the program will output a .csv file in the Output folder for each
          bundle, that you can upload to Canvas manually
        - If you select online grading, the program will upload the grades to Canvas automatically

V. Processing Resubmissions
   1. Download both the original Gradescope assignment and the resubmission assignment (export evaluation)
   2. Unzip both downloaded files in the Gradescope folder. This should create two folders inside it with several
      .csv files each
   3. Rename the original folder to the name of the assignment (exactly as it appears in Canvas)
   4. Rename the resubmission folder to the name of the assignment, followed by "_Resubmission" (no quotation marks)
   5. Double-Click the Gradescope2Canvas.command file to run the program
   6. Type "R" and press enter (no quotation marks), and follow the prompts
        - If you select local grading, the program will output a .csv file in the Output folder for each
          bundle, that you can upload to Canvas manually
        - If you select online grading, the program will upload the grades to Canvas automatically
   7. Please note that the program only supports regrading 1 assignment at a time, so if you want to regrade
      multiple assignments, you will have to repeat steps 1-6 for each assignment

V. Removing an assignment from a Canvas bundles
    1. Have the CSV file for each bundle assingment ready in the Canvas folder
    2. Double-Click the Gradescope2Canvas.command file to run the program
    3. Type "RM" and press enter (no quotation marks), and follow the prompts
    4. This will output a .csv file in the Output folder for each bundle, that you can upload to Canvas manually
       - If you wish to repeat this process with other assignments, move the .csv files from the Output
         folder into the Canvas folder, and repeat steps 2-4 (you will have to delete the previous .csv files
         from the Canvas folder before repeating the process)
    5. Please note that the program does not support removing assignments from Canvas directly, so you will have
       to upload the .csv files to Canvas manually (after removing the assignment from the rubrics of each bundle)
