  document.getElementById("showRegister").addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("loginForm").classList.add("d-none");
    document.getElementById("registerForm").classList.remove("d-none");
  });
  
  document.getElementById("showLogin").addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("registerForm").classList.add("d-none");
    document.getElementById("loginForm").classList.remove("d-none");
  });
  