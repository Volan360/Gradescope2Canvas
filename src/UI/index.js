const courseInfoBtn = document.getElementById("courseInfoBtn")
const courseInfo = document.getElementById("courseInfo")
const portNumber = "7777"
courseNameInput = document.getElementById("courseNameInput")

courseInfoBtn.addEventListener("click", () => {
    fetch(`http://localhost:${portNumber}/courseInfo?courseName=${encodeURIComponent(courseNameInput.value)}`)
        .then(res => res.text())
        .then(res => {
            courseInfo.innerHTML = res
        })
})