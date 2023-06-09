Gradescope2Canvas is a file conversion tool used to update students' grades on Canvas
based on information taken from the corresponding Gradescope course. The software is
designed to work with courses using specification based grading.

Initial Setup:
In order to automatically update Canvas grades, you must provide a valid API key.
This step only needs to be performed once or until the API key you provided is invalid.
1. Login to your Canvas account
2. Click on "Account->Settings" in your sidebar
3. Scroll down to "Approved Integrations"
4. Click on "+ New Access Token"
5. Copy the generated KEY to your clipboard
6. Return to the directory of your Gradescope2Canvas build
7. Open "config.yaml"
8. Paste your KEY after the colon on the line that says "KEY: ", remember to leave a space between
   the colon and key
9. Save "config.yaml"
9.a FOR MAC USERS:
    - Open the terminal (command + spacebar, type "terminal", press enter)
    - Type "cd " (with a space after cd, no quotes)
    - Drag the Gradescope2Canvas folder into the terminal window
        - This should result in something similar to "cd /Users/username/Downloads/Gradescope2Canvas"
    - Press enter
    - Type "chmod +x Gradescope2Canvas.command" (no quotes)
    - Press enter
    - Type "chmod +x Main" (no quotes)
    - Press enter
    - Close the terminal
    - Hold the control key and click on Main
    - Click on "Open"
    - This should open a terminal window, wait a few seconds then close the window
10. Open Gradescope2Canvas by double-clicking "Gradescope2Canvas.bat" or "Gradescope2Canvas.command"

Help:
The help button is included to help you navigate the software. Toggle it on then click
on any other button to learn more about how to use it.

Course Setup:
Specifies which course to upload grades for and what bundles are available. You will need
to take this step at the start of each quarter and whenever you want to change the course.
where grades will be updated.
1. Copy the name of the course you wish to update grades for as it appears on Canvas
2. Open Gradescope2Canvas (double-click "Gradescope2Canvas.bat" or "Gradescope2Canvas.command")
3. Press "Course Setup" under Utilities
4. Paste the the name of the course into Gradescope2Canvas under "Course Name"
5. Click on the "Set Course Info" button
6. Open "config.yaml" to verify changes were made to it
    - You can also click "Current Course" under Utilities to verify the course name and assignments
      at any time

Upload:
Uploads assignments directly to Canvas without manual intervention. Supports multiple
assignments at once. PLEASE NOTE THAT THERE IS A SEPARATE PROCESS FOR UPLOADING RESUBMISSIONS.
1. Open your Canvas course page
2. Add the assignment you want to grade to each relevant bundle rubric
3. Open your Gradescope course page
4. Click on the assignment you want to upload
5. Click on "Export Evaluations"
6. Unzip the downloaded folder to the "Gradescope" directory
7. Rename the unzipped folder to match the name of the assignment as it appears on Canvas
    - Repeat 4-7 for each assignment you want to grade, making sure they're all on the
      Canvas bundle rubrics
8. Open Gradescope2Canvas (double-click "Gradescope2Canvas.bat" or "Gradescope2Canvas.command")
9. Click on "Upload" under Actions
10. Specify whether you want to match by SID or Email under "Upload Assignments"
11. Specify the name of the SID/Email column in the Gradescope CSV files under "Upload Assignments"
    - If you chose to match by SID, specify the SID column name (will default to SID)
    - If you chose to match by Email, specify the Email column name (will default to Email)
12. Click on the "Upload Assignments" button
    - The terminal window should display relevant output or error messages


Convert:
Updates Canvas CSV files with the contents of Gradescope CSV files. PLEASE NOTE THAT THIS ONLY
SUPPORTS 1 ASSIGNMENT AT A TIME.
1. Complete the steps 3-7 of "Upload" for the Gradescope assignment you want to grade
2. Download the latest version of the Canvas rubric for each bundle.
    - You must have the "Export Rubric Scores" TypeMonkey script installed to do this
        - https://oit.colorado.edu/services/teaching-learning-applications/canvas/enhancements-integrations/enhancements
    - Navigate to the Canvas course page
    - Click on "Assignments" in the sidebar
    - Click on the assignment you want to download the rubric for
    - Click on "SpeedGrader" on the right side of the page
    - Click on the "Export Rubric Scores" button
    - Save the downloaded file to the "Canvas" folder (it must be named "Rubric Scores BundleName.csv", no quotes)
        - Replace "BundleName" with the name of the bundle you want to grade
3. Open Gradescope2Canvas (double-click "Gradescope2Canvas.bat" or "Gradescope2Canvas.command")
4. Specify the "Gradescope SID Column" and "Canvas SID Column" under "Convert Assignments"
    - The default values are "SID" for Gradescope and "Student ID" for Canvas
5. Click on the "Convert Assignments" button
    - The terminal window should display relevant output or error messages
6. The converted CSV files will be saved to the "Output" folder
    -If you want to add another assignment, repeat step 1 to place the new Gradescope assignment
     in the "Gradescope" folder (deleting the old one), then replace the CSV files in the
     "Canvas" folder with the converted CSV files in the "Output" folder. Repeat steps 4 and 5.
7. Upload each of the final CSV files  to the corresponding bundle assignments in Canvas
    - You must have the "Import Rubric Scores" TypeMonkey script installed to do this
        - https://oit.colorado.edu/services/teaching-learning-applications/canvas/enhancements-integrations/enhancements
    - Navigate to the Canvas course page
    - Click on "Assignments" in the sidebar
    - Click on the assignment you want to upload the CSV file for
    - Click on "SpeedGrader" on the right side of the page
    - Click on the "Import Rubric Scores" button
    - Select the CSV file you want to upload
    - Click on the "Import" button
    - Repeat for each assignment

Regrade:
Regrades use a different grading algorithm than first time submissions. Press the
"Regrade" button to toggle it on, changing it to a blue color. When toggled on, the
"Convert" and "Upload" buttons will now additionally use regrade functionalities.
1. Toggle on the "Regrade" button
2. Click on the "Convert" or "Upload" button
3. Complete all relevant steps until right before clicking on the "Convert Assignments" or "Upload Assignments" button
4. Specify the "Initial Assignment Name" as it appears in the Canvas folder
5. Click on the "Convert Assignments" button or "Upload Assignments" button
    - The terminal window should display relevant output or error messages
6. Continue with the rest of the steps as normal

Remove:
If you wish to remove an assignment from the conversion use the steps below.
1. Place all bundle assignments in the "Canvas" folder (see "Convert" for more details)
2. Specify the "Name of Assignment" as it appears in the Canvas folder
3. Click on the "Remove from Canvas CSVs" button
    - The terminal window should display relevant output or error messages
4. The resulting CSV files will be saved to the "Output" folder
    - If you wish to remove more than one column, repeat steps 2 and 3, replacing the CSV files in the
      "Canvas" folder with the converted CSV files in the "Output" folder each time
5. Upload each of the final CSV files  to the corresponding bundle assignments in Canvas (see "Convert" for more details)

Running the program from Python:
1. Install Python 3.10 (tested on 3.10.11)
2. Clone the repository
3. Install the required packages by running "pip install -r requirements.txt" in the repository directory
4. Run "python src/server.py" in the repository directory
5. Open the UI by dragging "src/UI/index.html" into a web browser

Building the program:
1. Windows
    - Install Python 3.10 (tested on 3.10.11)
    - Clone the repository
    - Install the required packages by running "pip install -r requirements.txt" in the repository directory
    - Run "pyinstaller --onefile src/server.py" in the repository directory
    - Move the "server.exe" from the newly created "dist" folder to the "Windows-Build" folder
    - Delete the "build" and "dist" folders, as well as the server.spec file
    - Test the program by double-clicking "Gradescope2Canvas.bat" in the "Windows-Build" folder
2. Mac
    - Install Python 3.10 (tested on 3.10.11)
    - Clone the repository
    - Install the required packages by running "pip install -r requirements.txt" in the repository directory
    - Run "sudo pyinstaller src/server.py -n Main --windowed --noconfirm --clean --onefile" in the repository directory
        - You'll need to enter your password
    - Move the "Main" from the newly created "dist" folder to one of the "Mac-Build" folder (NOT Main.app)
        - If you built the program on an Intel Mac, move it to the "Mac-Intel-Build" folder
        - If you built the program on an M1 or M2 Mac, move it to the "Mac-M1-M2-Build" folder
    - Delete the "build" and "dist" folders, as well as the main.spec file
    - Test the program by double-clicking "Gradescope2Canvas.command" in the "Mac-Build" folder you just updated
