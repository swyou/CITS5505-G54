document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const showRegister = document.getElementById('showRegister');
  const showLogin = document.getElementById('showLogin');

  showRegister.addEventListener('click', function (e) {
    e.preventDefault();
    loginForm.classList.add('d-none');
    registerForm.classList.remove('d-none');
  });

  showLogin.addEventListener('click', function (e) {
    e.preventDefault();
    registerForm.classList.add('d-none');
    loginForm.classList.remove('d-none');
  });
});
