const form = document.getElementById("studentForm");
const studentTable = document.getElementById("studentTable");
const searchInput = document.getElementById("search");
const message = document.getElementById("message");
const recordCount = document.getElementById("recordCount");

const fields = {
    studentId: document.getElementById("studentId"),
    name: document.getElementById("name"),
    gender: document.getElementById("gender"),
    age: document.getElementById("age"),
    year: document.getElementById("year"),
    department: document.getElementById("department")
};

let students = [];

try {
    students = JSON.parse(localStorage.getItem("students")) || [];
    if (!Array.isArray(students)) students = [];
} catch {
    students = [];
}

let nextId = students.reduce(
    (max, student) => Math.max(max, Number(student.id) || 0), 0
) + 1;

function saveToStorage() {
    try {
        localStorage.setItem("students", JSON.stringify(students));
        return true;
    } catch {
        showMessage("Could not save records in this browser.", true);
        return false;
    }
}

function showMessage(text, isError = false) {
    message.textContent = text;
    message.style.color = isError ? "#dc2626" : "#15803d";
}

function resetForm() {
    form.reset();
    document.getElementById("editId").value = "";
    document.getElementById("formTitle").textContent = "Add Student";
    document.getElementById("saveButton").textContent = "Add Student";
    document.getElementById("cancelButton").hidden = true;
}

function renderStudents(query = "") {
    studentTable.replaceChildren();

    const term = query.trim().toLowerCase();
    const filtered = students.filter(student =>
        String(student.studentId).toLowerCase().includes(term) ||
        String(student.name).toLowerCase().includes(term)
    );

    recordCount.textContent =
        `Total students: ${students.length} | Displaying: ${filtered.length}`;

    if (filtered.length === 0) {
        const row = studentTable.insertRow();
        const cell = row.insertCell();
        cell.colSpan = 8;
        cell.textContent = "No matching student records.";
        return;
    }

    filtered.forEach(student => {
        const row = studentTable.insertRow();

        [
            student.id,
            student.studentId,
            student.name,
            student.gender,
            student.age,
            `Year ${student.year}`,
            student.department
        ].forEach(value => {
            const cell = row.insertCell();
            cell.textContent = value;
        });

        const actions = row.insertCell();

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.className = "edit";
        editButton.type = "button";
        editButton.addEventListener("click", () => editStudent(student.id));

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete";
        deleteButton.type = "button";
        deleteButton.addEventListener("click", () => deleteStudent(student.id));

        actions.append(editButton, deleteButton);
    });
}

// CREATE and UPDATE
form.addEventListener("submit", event => {
    event.preventDefault();

    const editId = document.getElementById("editId").value;
    const studentId = fields.studentId.value.trim();

    if (!studentId) {
        showMessage("Please enter a Student ID.", true);
        return;
    }

    const duplicate = students.some(student =>
        student.studentId.toLowerCase() === studentId.toLowerCase() &&
        String(student.id) !== editId
    );

    if (duplicate) {
        showMessage("This Student ID already exists.", true);
        return;
    }

    const studentData = {
        studentId,
        name: fields.name.value.trim(),
        gender: fields.gender.value,
        age: Number(fields.age.value),
        year: Number(fields.year.value),
        department: fields.department.value.trim()
    };

    if (
        !studentData.name ||
        !studentData.gender ||
        !studentData.department ||
        !Number.isInteger(studentData.age) ||
        studentData.age < 1 ||
        studentData.age > 120 ||
        !Number.isInteger(studentData.year) ||
        studentData.year < 1 ||
        studentData.year > 5
    ) {
        showMessage("Please enter valid information in every field.", true);
        return;
    }

    const previousStudents = [...students];

    if (editId) {
        students = students.map(student =>
            String(student.id) === editId
                ? { ...student, ...studentData }
                : student
        );
    } else {
        students.push({ id: nextId++, ...studentData });
    }

    if (!saveToStorage()) {
        students = previousStudents;
        return;
    }

    showMessage(editId ? "Student updated successfully!" :
        "Student added successfully!");
    resetForm();
    renderStudents(searchInput.value);
});

// Load a student into the form for editing
function editStudent(id) {
    const student = students.find(item => item.id === id);
    if (!student) return;

    document.getElementById("editId").value = student.id;

    fields.studentId.value = student.studentId;
    fields.name.value = student.name;
    fields.gender.value = student.gender;
    fields.age.value = student.age;
    fields.year.value = student.year;
    fields.department.value = student.department;

    document.getElementById("formTitle").textContent = "Edit Student";
    document.getElementById("saveButton").textContent = "Update Student";
    document.getElementById("cancelButton").hidden = false;

    showMessage("Edit the information and click Update Student.");
    form.scrollIntoView({ behavior: "smooth", block: "start" });
}

// DELETE
function deleteStudent(id) {
    const student = students.find(item => item.id === id);
    if (!student) return;

    if (!confirm(`Delete student ${student.name}?`)) return;

    const previousStudents = [...students];
    students = students.filter(item => item.id !== id);

    if (!saveToStorage()) {
        students = previousStudents;
        return;
    }

    if (document.getElementById("editId").value === String(id)) {
        resetForm();
    }

    showMessage("Student deleted successfully!");
    renderStudents(searchInput.value);
}

// SEARCH
searchInput.addEventListener("input", () => {
    renderStudents(searchInput.value);
});

document.getElementById("cancelButton").addEventListener("click", () => {
    resetForm();
    showMessage("Editing cancelled.");
});

renderStudents();
