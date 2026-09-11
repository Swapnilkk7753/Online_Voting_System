/*******************************
  TOGGLE LOGIN & SIGNUP
********************************/
function showSignup() {
  document.getElementById("loginBox").classList.add("d-none");
  document.getElementById("signupBox").classList.remove("d-none");
}

function showLogin() {
  document.getElementById("signupBox").classList.add("d-none");
  document.getElementById("loginBox").classList.remove("d-none");
}

/*******************************
  IMAGE PREVIEW
********************************/
document.getElementById("photo").addEventListener("change", function () {
  const file = this.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function (e) {
    const preview = document.getElementById("preview");
    preview.src = e.target.result;
    preview.classList.remove("d-none");
  };
  reader.readAsDataURL(file);
});

/*******************************
  SIGNUP FUNCTION
********************************/
function signup() {
  const type = document.getElementById("userType").value;
  const name = document.getElementById("name").value.trim();
  const id = document.getElementById("userId").value.trim();
  const email = document.getElementById("email").value.trim();
  const pass = document.getElementById("pass").value;
  const cpass = document.getElementById("cpass").value;
  const photoInput = document.getElementById("photo");

  if (!type || !name || !id || !email || !pass || !cpass) {
    alert("Please fill all fields");
    return;
  }

  if (pass !== cpass) {
    alert("Passwords do not match");
    return;
  }

  let users = JSON.parse(localStorage.getItem("users")) || [];

  // Check duplicate ID
  if (users.some(u => u.id === id)) {
    alert("User ID already exists");
    return;
  }

  let photoData = "";
  if (photoInput.files.length > 0) {
    const reader = new FileReader();
    reader.onload = function (e) {
      photoData = e.target.result;
      saveUser();
    };
    reader.readAsDataURL(photoInput.files[0]);
  } else {
    saveUser();
  }

  function saveUser() {
    users.push({
      type,
      name,
      id,
      email,
      password: pass,
      photo: photoData
    });

    localStorage.setItem("users", JSON.stringify(users));
    alert("Registration successful!");
    showLogin();
  }
}

/*******************************
  LOGIN FUNCTION
********************************/
function login() {
  const id = document.getElementById("loginId").value.trim();
  const pass = document.getElementById("loginPass").value;
  const type = document.getElementById("loginType").value;

  if (!id || !pass || !type) {
    alert("Please fill all fields");
    return;
  }

  const users = JSON.parse(localStorage.getItem("users")) || [];

  const user = users.find(
    u => u.id === id && u.password === pass && u.type === type
  );

  if (!user) {
    alert("Invalid login credentials");
    return;
  }

  // Save logged-in user
  localStorage.setItem("loggedInUser", JSON.stringify(user));

  // Redirect based on role
  if (type === "student") {
    window.location.href = "student/student.html";
  } else {
    window.location.href = "employee/employee.html";
  }
}
