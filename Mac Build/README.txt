INITIAL SETUP:
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

III. Adding a class
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
    4. Double Click the Gradescope2Canvas.command file to run the program
    5. Type "CI" and press enter (no quotation marks)
    6. Type the name of the class you want to add and press enter (exactly as it appears in Canvas)
