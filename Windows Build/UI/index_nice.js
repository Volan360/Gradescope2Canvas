onLoad();

uploadBtn = document.getElementById("uploadBtn");
uploadGradeScreen = document.getElementById("uploadGradeScreen");
uploadRegradeScreen = document.getElementById("uploadRegradeScreen");
uploadBtn.addEventListener("click", () => {
    //add active class if not already there
    hideAllInfoScreen();
    if (regradeBtn.classList.contains("active")) {
        uploadRegradeScreen.classList.remove("hidden");
        setHelpInfo("uploadResubmission");
    } else {
        uploadGradeScreen.classList.remove("hidden");
        setHelpInfo("uploadAssignment");
    }
})

convertBtn = document.getElementById("convertBtn");
convertGradeScreen = document.getElementById("convertGradeScreen");
convertRegradeScreen = document.getElementById("convertRegradeScreen");
convertBtn.addEventListener("click", () => {
    //add active class if not already there
    hideAllInfoScreen();
    if (regradeBtn.classList.contains("active")) {
        convertRegradeScreen.classList.remove("hidden");
        setHelpInfo("convertResubmission");
    } else {
        convertGradeScreen.classList.remove("hidden");
        setHelpInfo("convertAssignment");
    }
})

helpBtn = document.getElementById("helpBtn");
helpBtn.addEventListener("click", () => {
    //add active class if not already there
    let helpInfo = document.getElementsByClassName("helpInfo")[0];
    setHelpInfo("")
    if (!helpBtn.classList.contains("active")) {
        helpBtn.classList.add("active");
        helpInfo.classList.remove("hidden");
    } else {
        helpBtn.classList.remove("active");
        helpInfo.classList.add("hidden");
    }
})

regradeBtn = document.getElementById("regradeBtn");
regradeBtn.addEventListener("click", () => {
    //add active class if not already there
    if (!regradeBtn.classList.contains("active")) {
        regradeBtn.classList.add("active");
    } else {
        regradeBtn.classList.remove("active");
    }
})

courseSetupBtn = document.getElementById("courseSetupBtn");
courseSetupScreen = document.getElementById("courseSetupScreen");
courseSetupBtn.addEventListener("click", () => {
    //add active class if not already there
    hideAllInfoScreen();
    courseSetupScreen.classList.remove("hidden");
    setHelpInfo("courseSetup");
})

removeBtn = document.getElementById("removeBtn");
removeScreen = document.getElementById("removeScreen");
removeBtn.addEventListener("click", () => {
    //add active class if not already there
    hideAllInfoScreen();
    removeScreen.classList.remove("hidden");
    setHelpInfo("removeAssignment");
})


function hideAllInfoScreen() {
    let infoScreenClass = document.getElementsByClassName("infoScreen");
    for (let i = 0; i < infoScreenClass.length; i++) {
        if (!infoScreenClass[i].classList.contains("hidden")){
            infoScreenClass[i].classList.add("hidden");
        }
    }
}

function onLoad() {
    hideAllInfoScreen();
    let uploadGradeScreen = document.getElementById("uploadGradeScreen");
    uploadGradeScreen.classList.remove("hidden");
}

function setHelpInfo(actionName) {
    let helpInfo = document.getElementsByClassName("helpInfo")[0];
    while (helpInfo.firstChild) {
        helpInfo.removeChild(helpInfo.firstChild);
    }
    if (actionName === "") {
        let h1 = document.createElement("h1");
        h1.textContent = "Initial Setup";
        helpInfo.appendChild(h1);

        let ol = document.createElement("ol");
        let li1 = document.createElement("li");
        li1.textContent = "Open the config.yaml file in a text editor (it's inside the Program folder)";
        let li2 = document.createElement("li");
        li2.textContent = "Open your canvas account in a web browser";
        let li3 = document.createElement("li");
        li3.textContent = "Click on Settings";
        let li4 = document.createElement("li");
        li4.textContent = "Scroll down to \"Approved Integrations\" and click \"+ New Access Token\"";
        let li5 = document.createElement("li");
        li5.textContent = "Type \"Gradescope2Canvas\" in the Purpose field, or some other name";
        let li6 = document.createElement("li");
        li6.textContent = "Click \"Generate Token\"";
        let li7 = document.createElement("li");
        li7.textContent = "Copy the token that appears and paste it into the config.yaml file, after the colon in the KEY field under CANVAS_API";
        let li8 = document.createElement("li");
        li8.textContent = "Save the file";
        ol.appendChild(li1);
        ol.appendChild(li2);
        ol.appendChild(li3);
        ol.appendChild(li4);
        ol.appendChild(li5);
        ol.appendChild(li6);
        ol.appendChild(li7);
        ol.appendChild(li8);
        helpInfo.appendChild(ol);
        //create h1 with text "Select an action for instructions"
        let h2 = document.createElement("h2");
        h2.textContent = "Select an action for specific instructions";
        helpInfo.appendChild(h2);
        return;
    }

    if (actionName === "uploadAssignment"){

        let ol = document.createElement("ol");
        let li1 = document.createElement("li");
        li1.textContent = "On Canvas, add the assignment you want to grade to each of the relevant bundle rubrics";
        let li2 = document.createElement("li");
        li2.textContent = "Download the assignment from Gradescope (export evaluation)";
        let li3 = document.createElement("li");
        li3.textContent = "Unzip the downloaded file in the Gradescope folder. This should create a folder inside it with several .csv files";
        let li4 = document.createElement("li");
        li4.textContent = "Rename the folder to the name of the assignment, exactly as it appears as a criterion in the Canvas rubrics";
        let li5 = document.createElement("li");
        li5.textContent = "Repeat steps 1-4 for each assignment you want to grade";
        ol.appendChild(li1);
        ol.appendChild(li2);
        ol.appendChild(li3);
        ol.appendChild(li4);
        ol.appendChild(li5);
        helpInfo.appendChild(ol);
    }
    else if (actionName === "convertAssignment"){

        let ol = document.createElement("ol");
        let li1 = document.createElement("li");
        li1.textContent = "On Canvas, add the assignment you want to grade to each of the relevant bundle rubrics";
        let li2 = document.createElement("li");
        li2.textContent = "Download the assignment from Gradescope (export evaluation)";
        let li3 = document.createElement("li");
        li3.textContent = "Unzip the downloaded file in the Gradescope folder. This should create a folder inside it with several .csv files";
        let li4 = document.createElement("li");
        li4.textContent = "Rename the folder to the name of the assignment, exactly as it appears as a criterion in the Canvas rubrics";
        let li5 = document.createElement("li");
        li5.textContent = "Repeat steps 1-4 for each assignment you want to grade";
        let li6 = document.createElement("li");
        li6.textContent = "Download the latest version of the Canvas rubrics each bundle (each should be a .csv file)";
        let li7 = document.createElement("li");
        li7.textContent = "Place the rubrics in the Canvas folder, renamed to exactly match the name of the bundle";
        ol.appendChild(li1);
        ol.appendChild(li2);
        ol.appendChild(li3);
        ol.appendChild(li4);
        ol.appendChild(li5);
        ol.appendChild(li6);
        ol.appendChild(li7);
        helpInfo.appendChild(ol);
    }
    else if (actionName === "courseSetup"){

        let ol = document.createElement("ol");
        let li1 = document.createElement("li");
        li1.textContent = "After running this program, open your config.yaml file in a text editor to make sure the course and all bundles are listed";
        ol.appendChild(li1);
        helpInfo.appendChild(ol);
    }
    else if (actionName === "removeAssignment"){

        let ol = document.createElement("ol");
        let li1 = document.createElement("li");
        li1.textContent = "Have the CSV file for each bundle assingment ready in the Canvas folder";
        let li2 = document.createElement("li");
        li2.textContent = "If you wish to repeat this function with another assignment, move the .csv files from the Output folder into the Canvas folder, and run again (you will have to delete the previous .csv files from the Canvas folder before repeating the process)";
        let li3 = document.createElement("li");
        li3.textContent = "Please note that the program does not support removing assignments from Canvas directly, so you will have to upload the .csv files to Canvas manually (after removing the assignment from the rubrics of each bundle)";
        ol.appendChild(li1);
        ol.appendChild(li2);
        ol.appendChild(li3);
        helpInfo.appendChild(ol);
    }
    else if (actionName === "uploadResubmission"){

        let ol = document.createElement("ol");
        let li1 = document.createElement("li");
        li1.textContent = "Download both the original Gradescope assignment and the resubmission assignment (export evaluation)";
        let li2 = document.createElement("li");
        li2.textContent = "Unzip both downloaded files in the Gradescope folder. This should create two folders inside it with several .csv files each";
        let li3 = document.createElement("li");
        li3.textContent = "Rename the original folder to the name of the assignment, exactly as it appears as a criterion in the Canvas rubrics";
        let li4 = document.createElement("li");
        li4.textContent = "Rename the resubmission folder to the name of the assignment, followed by \"_Resubmission\" (no quotation marks)";
        let li5 = document.createElement("li");
        li5.textContent = "Please note that the program only supports regrading 1 assignment at a time, so if you want to regrade multiple assignments, you will have to repeat steps 1-4 for each assignment, deleting the previous assignment from the Gradescope/Output folder before repeating the process";
        ol.appendChild(li1);
        ol.appendChild(li2);
        ol.appendChild(li3);
        ol.appendChild(li4);
        ol.appendChild(li5);
        helpInfo.appendChild(ol);
    }
    else if (actionName === "convertResubmission"){

        let ol = document.createElement("ol");
        let li1 = document.createElement("li");
        li1.textContent = "Download both the original Gradescope assignment and the resubmission assignment (export evaluation)";
        let li2 = document.createElement("li");
        li2.textContent = "Unzip both downloaded files in the Gradescope folder. This should create two folders inside it with several .csv files each";
        let li3 = document.createElement("li");
        li3.textContent = "Rename the original folder to the name of the assignment, exactly as it appears as a criterion in the Canvas rubrics";
        let li4 = document.createElement("li");
        li4.textContent = "Rename the resubmission folder to the name of the assignment, followed by \"_Resubmission\" (no quotation marks)";
        let li5 = document.createElement("li");
        li5.textContent = "Download the latest version of the Canvas rubrics each bundle (each should be a .csv file)";
        let li6 = document.createElement("li");
        li6.textContent = "Place the rubrics in the Canvas folder, renamed to exactly match the name of the bundle";
        let li7 = document.createElement("li");
        li7.textContent = "Please note that the program only supports regrading 1 assignment at a time, so if you want to regrade multiple assignments, you will have to repeat steps 1-4 for each assignment, and also move the .csv files from the Output folder into the Canvas folder each time (you will have to delete the previous .csv files from the Canvas folder)";
        ol.appendChild(li1);
        ol.appendChild(li2);
        ol.appendChild(li3);
        ol.appendChild(li4);
        ol.appendChild(li5);
        ol.appendChild(li6);
        ol.appendChild(li7);
        helpInfo.appendChild(ol);
    }
}