

document.addEventListener("DOMContentLoaded", () => {

  const parameters = document.querySelectorAll(".parameter");
  const details = document.querySelectorAll(".parameter__details");

  parameters.forEach((parameter) => {
    // disable the typeOfFurniture parameter and set it as selected because user has already selected it in pop up
    if (parameter.getAttribute('data-parameter') === 'typeOfFurniture') {
      parameter.classList.add('selected');
      parameter.style.pointerEvents = 'none';
    }

    parameter.addEventListener("click", (e) => {
      e.preventDefault();

      parameters.forEach((param) => param.classList.remove("current"));
      details.forEach((detail) => detail.classList.remove("current"));

      parameter.classList.add("current");
      const parameterData = parameter.getAttribute("data-parameter");
      document
        .querySelector(`.parameter__details[data-parameter="${parameterData}"]`)
        .classList.add("current");

// check if any parameter details have been selected and add the selected class to the parameter

      parameters.forEach((param) => {
        const paramData = param.getAttribute("data-parameter");
        const associatedDetail = document.querySelector(
          `.parameter__details[data-parameter="${paramData}"]`
        );
        const hasCheckedInput =
          associatedDetail.querySelector('input[type="radio"]:checked[data-parameter]') !==
          null;

        if (param.classList.contains("current")) {
          param.classList.remove("selected");
        } else if (hasCheckedInput) {
          param.classList.add("selected");
        } else {
          param.classList.remove("selected");
        }
      });
    });
  });
  // allow user to deselect radio buttons
  document.querySelectorAll('input[type="radio"]').forEach((radio) => {
    if (!radio.getAttribute("data-personal")) {
      radio.addEventListener("click", function () {
        if (this.checked) {
          if (this.getAttribute("data-waschecked") === "true") {
            this.checked = false;
            this.removeAttribute("data-waschecked");
          } else {
            document
              .querySelectorAll('input[type="radio"]')
              .forEach((rb) => rb.removeAttribute("data-waschecked"));
            this.setAttribute("data-waschecked", "true");
          }
        }
      });
    }
  });

  // script to customize the imported date flatpickr

  flatpickr("#datePicker", {
    inline: false,
    weekNumbers: true,
    defaultDate: null,
    showMonths: 1,
    disableMobile: "true",
    minDate: "today",
    startDate: "today",
    altInput: true,
    altFormat: "F j, Y",
    dateFormat: "Y-m-d",
    onReady: function (selectedDates, dateStr, instance) {
      const monthContainer =
        instance.calendarContainer.querySelector(".flatpickr-months");
      const month = instance.currentMonth;
      const year = instance.currentYear;
      const monthName = instance.l10n.months.longhand[month];
      const monthElement = document.createElement("div");
      monthElement.className = "flatpickr-month";
      monthElement.textContent = `${monthName} ${year}`;
      monthContainer.innerHTML = "";
      monthContainer.appendChild(monthElement);
    },
    onDayCreate: function (dObj, dStr, fp, dayElem) {
      if (
        dayElem.dateObj.getDay() === 0 ||
        dayElem.dateObj.getDay() === 6
      ) {
        dayElem.classList.add("weekend");
      } else {
        dayElem.classList.add("weekday");
      }
    },
    onChange: function (selectedDates, dateStr, instance) {
      const datepicker = document.getElementById("datePicker");
      if (selectedDates.length === 0) {
        datepicker.placeholder = "Дата";
      } else {
        datepicker.placeholder = "";
      }
    },
    locale: {
      firstDayOfWeek: 1,
    },
  });

  flatpickr("#timePicker", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
    defaultDate: null,
    disableMobile: "true",
    minTime: "08:00",
    maxTime: "22:00",
    onReady: function (selectedDates, dateStr, instance) {
      const timePicker = document.getElementById("timePicker");
      if (selectedDates.length === 0) {
        timePicker.placeholder = "Время";
      } else {
        timePicker.placeholder = "";
      }
    },
    onChange: function (selectedDates, dateStr, instance) {
      const timePicker = document.getElementById("timePicker");
      if (selectedDates.length === 0) {
        timePicker.placeholder = "Время";
      } else {
        timePicker.placeholder = "";
      }
    },
  });
});
