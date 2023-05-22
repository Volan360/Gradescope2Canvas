const courseInfoBtn = document.getElementById("courseInfoBtn")
const courseInfo = document.getElementById("courseInfoRes")
const portNumber = "7777"
courseNameInput = document.getElementById("courseNameInput")

courseInfoBtn.addEventListener("click", () => {
    fetch(`http://localhost:${portNumber}/courseInfo?courseName=${encodeURIComponent(courseNameInput.value)}`)
        .then(res => res.text())
        .then(res => {
            courseInfo.innerHTML = res
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
    }
    else {
        emailOrSID = matchBy.value
    }
    gradescopeColumn = columnName.value ? columnName.value !== "" : emailOrSID
    fetch(`http://localhost:${portNumber}/uploadGrade?emailOrSID=${encodeURIComponent(emailOrSID)}&gradescopeColumn=${encodeURIComponent(gradescopeColumn)}`)
        .then(res => res.text())
        .then(res => {
            uploadAssignmentsRes.innerHTML = res
        })

})