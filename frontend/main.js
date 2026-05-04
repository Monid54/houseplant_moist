/////// pasword toggle ////


function togglePassword(el) {
  const input = el.parentElement.querySelector("input");
  const icon = el.querySelector("img");

  if (input.type === "password") {
    input.type = "text";
    icon.src = "https://img.icons8.com/?size=100&id=7877&format=png&color=737373";
  } else {
    input.type = "password";
    icon.src = "https://img.icons8.com/?size=100&id=34226&format=png&color=737373";
  }
}