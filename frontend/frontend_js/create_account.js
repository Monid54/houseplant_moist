document
  .getElementById("createAccountForm")
  .addEventListener("submit", function (e) {

    e.preventDefault();

    // ===== FORM VALUES =====

    const email =
      document.querySelector(
        'input[name="email"]'
      ).value;

    const password =
      document.querySelector(
        'input[name="password"]'
      ).value;

    const confirmPassword =
      document.querySelector(
        'input[name="confirm-password"]'
      ).value;

    const termsAccepted =
      document.querySelector(
        'input[name="remember"]'
      ).checked;


    // ===== VALIDATION =====

    if (!termsAccepted) {

      alert(
        "Please accept the Terms of Use"
      );

      return;
    }

    if (password !== confirmPassword) {

      alert(
        "Passwords do not match"
      );

      return;
    }


    // ===== GET SIGNUP DATA =====

    const signupData =
      JSON.parse(
        localStorage.getItem("signupData")
      ) || {};


    // ===== CREATE USER OBJECT =====

    const user = {

      ...signupData,

      email,
      password

    };


    // ===== SAVE USER =====

    localStorage.setItem(
      "plantcareUser",
      JSON.stringify(user)
    );


    // ===== SAVE USERNAME =====

    localStorage.setItem(
      "userName",
      signupData.firstname
    );


    // ===== CLEAR TEMP DATA =====

    localStorage.removeItem(
      "signupData"
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