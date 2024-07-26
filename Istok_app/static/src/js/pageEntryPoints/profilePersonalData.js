import initModals from "../shared/handleModals.js";

window.addEventListener("DOMContentLoaded", () => {
  initModals();

  function maskPasswordById(id) {
    const passwordText = document.querySelector(id);
    const passwordTextValue = passwordText.textContent;
    const passwordTextLength = passwordTextValue.length;
    const passwordTextMask = "\u25CF".repeat(passwordTextLength);
    passwordText.textContent = passwordTextMask;
  }

  const today = new Date();
  const nineYearsAgo = new Date(
    today.getFullYear() - 9,
    today.getMonth(),
    today.getDate()
  );
  const formattedDate = nineYearsAgo.toISOString().split("T")[0];
  maskPasswordById(".profile__password-mask");

  // script to customize the imported date flatpickr

  flatpickr("#id_birth_date", {
    altInput: true,
    altFormat: "F j, Y",
    dateFormat: "Y-m-d",
    maxDate: formattedDate,
  });

  document
    .getElementById("id_copy_code")
    .addEventListener("click", function () {
      const referralCode =
        document.getElementById("id_referral_code").textContent;
      navigator.clipboard
        .writeText(referralCode)
        .then(function () {})
        .catch(function (err) {
          console.error("Ошибка при копировании текста: ", err);
        });
    });
});
