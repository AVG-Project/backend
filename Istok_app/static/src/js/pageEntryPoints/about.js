import initScrollToViewByClick from "../shared/scrollToViewByClick.js";
import handleScroll from "../shared/handleScroll.js";
import handleResize from "../shared/handleResize.js";

window.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container");

  if (container) {
    const resizeHandler = () => handleResize(container);
    const scrollHandler = () => handleScroll(container);
    resizeHandler();
    window.addEventListener("resize", resizeHandler);
    scrollHandler();
  } else console.debug("No container found");

  
  const controls = document.querySelectorAll(".bottom-progress-bar__btn");
  initScrollToViewByClick(controls);
  
  const root = document.querySelector(".main-content");
  const textBlock = document.getElementById("fixedTextBlockOnAboutPage");
  const textContent = textBlock.querySelector(".text-block__content");
  const sections = document.querySelectorAll(".main-content__section");

  const options = {
    root: root,
    rootMargin: "0px",
    threshold: 0.4,
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const newContent = entry.target.querySelector(
          ".slide__content_hidden"
        ).innerHTML;

        if (textContent.innerHTML !== newContent) {
          textContent.style.opacity = 0;
          // textBlock.classList.add("fade");
          // setTimeout(() => {
            //   textBlock.classList.remove("fade");
            // }, 500);
            setTimeout(() => {
            textContent.innerHTML = newContent;
            textContent.style.opacity = 1;
          }, 700);
          // change width of text block for brand section
          if (entry.target.id === "brand") {
            textBlock.style.width = "auto";
          } else {
            textBlock.style.width = "487px";
          }
        }
        const sectionId = entry.target.id;
        controls.forEach((control) => {
          const controlCircle = control.querySelector(".slide-control__circle");
          if (
            control.getAttribute("data-related-section-id") === sectionId ||
            (sectionId === "values_2" &&
              control.getAttribute("data-related-section-id") === "values")
          ) {
            controlCircle.classList.add("slide-control__circle_active");
          } else {
            controlCircle.classList.remove("slide-control__circle_active");
          }
        });
      }
    });
  }, options);

  sections.forEach((section) => {
    observer.observe(section);
  });
});
