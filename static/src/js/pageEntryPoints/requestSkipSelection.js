

document.addEventListener("DOMContentLoaded", () => {
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
  