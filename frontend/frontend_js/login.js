// ===== LOGIN FORM =====

document
  .getElementById("loginForm")
  .addEventListener("submit", function (e) {

    e.preventDefault();


    // ===== INPUT VALUES =====

    const email =
      document.querySelector(
        'input[name="email"]'
      ).value;

    const password =
      document.querySelector(
        'input[name="password"]'
      ).value;


    // ===== GET SAVED USER =====

    const savedUser =
      JSON.parse(
        localStorage.getItem("plantcareUser")
      );


    // ===== VALIDATE USER =====

    if (!savedUser) {

      alert(
        "No account found. Please sign up first."
      );

      return;
    }


    // ===== CHECK EMAIL =====

    if (email !== savedUser.email) {

      alert(
        "Incorrect email"
      );

      return;
    }


    // ===== CHECK PASSWORD =====

    if (password !== savedUser.password) {

      alert(
        "Incorrect password"
      );

      return;
    }


    // ===== SAVE USERNAME =====

    localStorage.setItem(
      "userName",
      savedUser.firstname
    );


    // ===== SUCCESS =====

    alert(
      "Login successful!"
    );


    // ===== REDIRECT =====

    window.location.href =
      "dashboard.html";

});



// ===== PASSWORD TOGGLE =====

function togglePassword(element) {

  const input =
    element.parentElement.querySelector("input");

  const icon =
    element.querySelector("img");


  // SHOW PASSWORD
  if (input.type === "password") {

    input.type = "text";

    icon.src =
      "https://img.icons8.com/?size=100&id=7877&format=png&color=737373";

  }

  // HIDE PASSWORD
  else {

    input.type = "password";

    icon.src =
      "https://img.icons8.com/?size=100&id=34226&format=png&color=737373";

  }

}