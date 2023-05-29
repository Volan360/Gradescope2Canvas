onLoad();

uploadBtn = document.getElementById("uploadBtn");
uploadGradeScreen = document.getElementById("uploadGradeScreen");
uploadRegradeScreen = document.getElementById("uploadRegradeScreen");
uploadBtn.addEventListener("click", () => {
    //add active class if not already there
    hideAllInfoScreen();
    if (regradeBtn.classList.contains("active")) {
        uploadRegradeScreen.classList.remove("hidden");
    } else {
        uploadGradeScreen.classList.remove("hidden");
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
    } else {
        convertGradeScreen.classList.remove("hidden");
    }
})

helpBtn = document.getElementById("helpBtn");
helpScreen = document.getElementById("helpScreen");
helpBtn.addEventListener("click", () => {
    //add active class if not already there
    hideAllInfoScreen();
    helpScreen.classList.remove("hidden");
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
})

removeBtn = document.getElementById("removeBtn");
removeScreen = document.getElementById("removeScreen");
removeBtn.addEventListener("click", () => {
    //add active class if not already there
    hideAllInfoScreen();
    removeScreen.classList.remove("hidden");
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