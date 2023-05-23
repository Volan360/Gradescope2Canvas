const courseInfoBtn = document.getElementById("courseInfoBtn")
const courseInfo = document.getElementById("courseInfoRes")
const portNumber = "7777"
courseNameInput = document.getElementById("courseNameInput")

courseInfoBtn.addEventListener("click", () => {
    fetch(`http://localhost:${portNumber}/courseInfo?courseName=${encodeURIComponent(courseNameInput.value)}`)
        .then(res => {
            //if there are any errors, do a window alert
            if (res.status !== 200) {
                window.alert("There was an error getting the course info, restart the server, check inputs, and try again")
            }
            return res.text()
        })
        .then(res => {
            courseInfo.innerHTML = res + "<br>" + "Please close the server before editing the config.yaml file"
        })
})


const uploadAssignmentsBtn = document.getElementById("uploadAssignmentsBtn")
const matchBy = document.getElementById("uploadAssignmentsMatchBy")
const columnName = document.getElementById("uploadAssignmentsColumnName")
const uploadAssignmentsRes = document.getElementById("uploadAssignmentsRes")
uploadAssignmentsBtn.addEventListener("click", () => {
    var emailOrSID = ""
    var gradescopeColumn = ""
    if (matchBy.value === "None") {
        window.alert("Please select a column to match by")
        return
    }
    else {
        emailOrSID = matchBy.value
    }
    gradescopeColumn = columnName.value ? columnName.value !== "" : emailOrSID
    fetch(`http://localhost:${portNumber}/uploadGrade?emailOrSID=${encodeURIComponent(emailOrSID)}&gradescopeColumn=${encodeURIComponent(gradescopeColumn)}`)
        .then(res => {
            //if there are any errors, do a window alert
            if (res.status !== 200) {
                window.alert("There was an error uploading the grades, restart the server, check inputs, and try again")
            }
            return res.text()
        })
        .then(res => {
            uploadAssignmentsRes.innerHTML = res
        })

})


const localGradesBtn = document.getElementById("localGradesBtn")
const localGradesRes = document.getElementById("localGradesRes")
const gradescopeColumnInput = document.getElementById("localAssignmentsGradescopeColumn")
const canvasColumnInput = document.getElementById("localAssignmentsCanvasColumn")

localGradesBtn.addEventListener("click", () => {
    var gradescopeColumn = ""
    var canvasColumn = ""
    if (gradescopeColumnInput.value === "") {
        gradescopeColumn = "SID"
    }
    else {
        gradescopeColumn = gradescopeColumnInput.value
    }
    if (canvasColumnInput.value === "") {
        canvasColumn = "Student ID"
    }
    else {
        canvasColumn = canvasColumnInput.value
    }
    fetch(`http://localhost:${portNumber}/localGrade?gradescopeColumn=${encodeURIComponent(gradescopeColumn)}&canvasColumn=${encodeURIComponent(canvasColumn)}`)
        .then(res => {
            //if there are any errors, do a window alert
            if (res.status !== 200) {
                window.alert("There was an error outputting the grades, restart the server, check inputs, and try again")
            }
            return res.text()
        })
        .then(res => {
            localGradesRes.innerHTML = res
        })
})


const uploadResubmissionBtn = document.getElementById("uploadResubmissionBtn")
const uploadResubmissionRes = document.getElementById("uploadResubmissionRes")
const uploadResubmissionMatchBy = document.getElementById("uploadResubmissionMatchBy")
const uploadResubmissionInitialAssignment = document.getElementById("uploadResubmissionInitialAssignment")
const uploadResubmissionColumnName = document.getElementById("uploadResubmissionColumnName")
uploadResubmissionBtn.addEventListener("click", () => {
    var emailOrSID = ""
    var gradescopeColumn = ""
    if (uploadResubmissionMatchBy.value === "None") {
        window.alert("Please select a column to match by")
        return
    }
    else {
        emailOrSID = uploadResubmissionMatchBy.value
    }
    if (uploadResubmissionInitialAssignment.value === "") {
        window.alert("Please enter the name of the initial assignment")
        return
    }

    gradescopeColumn = uploadResubmissionColumnName.value ? uploadResubmissionColumnName.value !== "" : emailOrSID
    fetch(`http://localhost:${portNumber}/uploadResubmission?emailOrSID=${encodeURIComponent(emailOrSID)}&gradescopeColumn=${encodeURIComponent(gradescopeColumn)}&initialAssignment=${encodeURIComponent(uploadResubmissionInitialAssignment.value)}`)
        .then(res => {
            //if there are any errors, do a window alert
            if (res.status !== 200) {
                window.alert("There was an error uploading the resubmission, restart the server, check inputs, and try again")
            }
            return res.text()
        })
        .then(res => {
            uploadResubmissionRes.innerHTML = res
        })

})


const localResubmissionBtn = document.getElementById("localResubmissionBtn")
const localResubmissionRes = document.getElementById("localResubmissionRes")
const localResubmissionGradescopeColumn = document.getElementById("localResubmissionGradescopeColumn")
const localResubmissionCanvasColumn = document.getElementById("localResubmissionCanvasColumn")
const localResubmissionInitialAssignment = document.getElementById("localResubmissionInitialAssignment")
localResubmissionBtn.addEventListener("click", () => {
    var gradescopeColumn = ""
    var canvasColumn = ""
    if (localResubmissionGradescopeColumn.value === "") {
        gradescopeColumn = "SID"
    }
    else {
        gradescopeColumn = localResubmissionGradescopeColumn.value
    }
    if (localResubmissionCanvasColumn.value === "") {
        canvasColumn = "Student ID"
    }
    else {
        canvasColumn = localResubmissionCanvasColumn.value
    }
    if (localResubmissionInitialAssignment.value === "") {
        window.alert("Please enter the name of the initial assignment")
        return
    }
    fetch(`http://localhost:${portNumber}/localResubmission?gradescopeColumn=${encodeURIComponent(gradescopeColumn)}&canvasColumn=${encodeURIComponent(canvasColumn)}&initialAssignment=${encodeURIComponent(localResubmissionInitialAssignment.value)}`)
        .then(res => {
            //if there are any errors, do a window alert
            if (res.status !== 200) {
                window.alert("There was an error outputting the resubmission, restart the server, check inputs, and try again")
            }
            return res.text()
        })
        .then(res => {
            localResubmissionRes.innerHTML = res
        })
})


const localRemoveBtn = document.getElementById("localRemoveBtn")
const localRemoveRes = document.getElementById("localRemoveRes")
const localRemoveAssignment = document.getElementById("localRemoveAssignment")
localRemoveBtn.addEventListener("click", () => {
    if (localRemoveAssignment.value === "") {
        window.alert("Please enter the name of the assignment to remove")
        return
    }
    fetch(`http://localhost:${portNumber}/localRemove?removeColumn=${encodeURIComponent(localRemoveAssignment.value)}`)
        .then(res => {
            //if there are any errors, do a window alert
            if (res.status !== 200) {
                window.alert("There was an error removing the assignment, restart the server, check inputs, and try again")
            }
            return res.text()
        })
        .then(res => {
            localRemoveRes.innerHTML = res
        })
})
