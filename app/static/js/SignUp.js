// Password visibility toggle
function togglePassword(fieldId) {
  const field = document.getElementById(fieldId);
  const toggleIcon = field.parentElement.querySelector(".password-toggle");
  if (field.type === "password") {
    field.type = "text";
    toggleIcon.classList.replace("bi-eye-slash", "bi-eye");
  } else {
    field.type = "password";
    toggleIcon.classList.replace("bi-eye", "bi-eye-slash");
  }
}

// Password strength indicator
document.getElementById("password").addEventListener("input", function (e) {
  const strengthMeter = this.parentElement.querySelector(".strength-meter");
  const strength = Math.min(e.target.value.length / 2, 10);
  strengthMeter.style.width = strength * 10 + "%";
  strengthMeter.classList.remove("bg-danger", "bg-warning", "bg-success");
  if (strength < 3) strengthMeter.classList.add("bg-danger");
  else if (strength < 6) strengthMeter.classList.add("bg-warning");
  else strengthMeter.classList.add("bg-success");
});

// Form validation
(function () {
  "use strict";
  const form = document.getElementById("registrationForm");

  form.addEventListener(
    "submit",
    function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }

      // Check password match
      const password = document.getElementById("password");
      const confirmPassword = document.getElementById("confirmPassword");
      if (password.value !== confirmPassword.value) {
        confirmPassword.setCustomValidity("Passwords must match");
        confirmPassword.reportValidity();
        event.preventDefault();
        event.stopPropagation();
      } else {
        confirmPassword.setCustomValidity("");
      }

      form.classList.add("was-validated");
    },
    false
  );
})();
