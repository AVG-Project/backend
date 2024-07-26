import handleResize from "../shared/handleResize.js";
import initModals from "../shared/handleModals.js";
import initHomeScrollAndSlider1 from "../shared/handleHomeScrollAndSlider.js";
import initScrollToViewByClick from "../shared/scrollToViewByClick.js";

document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".container");

  if (container) {
    const resizeHandler = () => handleResize(container);
    const scrollHandler = () => initHomeScrollAndSlider1(container);
    resizeHandler();
    window.addEventListener("resize", resizeHandler);
    scrollHandler();
  } else console.debug("No container found");

  initModals();

  const controls = document.querySelectorAll(".bottom-progress-bar__btn");
  initScrollToViewByClick(controls);

  const sections = document.querySelectorAll(".main-content__section");
  const root = document.querySelector(".main-content");
  const options = {
    root: root,
    rootMargin: "0px",
    threshold: 0.5,
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
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

// slider 3 - materials

document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".page4__slider-btn");
  const images = document.querySelectorAll(".page4__image");
  const textBlocks = document.querySelectorAll(".page4__slide-txt-block-list");

  // Set the default active elements

  const defaultCategory = "frames";
  document
    .querySelector(`.page4__slider-btn[data-category="${defaultCategory}"]`)
    .classList.add("active");
  document
    .querySelector(`.page4__image[data-related-category="${defaultCategory}"]`)
    .classList.add("active");
  document
    .querySelector(
      `.page4__slide-txt-block-list[data-related-category="${defaultCategory}"]`
    )
    .classList.add("active");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const category = button.getAttribute("data-category");

      buttons.forEach((btn) => btn.classList.remove("active"));
      images.forEach((image) => image.classList.remove("active"));
      textBlocks.forEach((block) => block.classList.remove("active"));

      button.classList.add("active");

      document
        .querySelector(`.page4__image[data-related-category="${category}"]`)
        .classList.add("active");
      document
        .querySelector(
          `.page4__slide-txt-block-list[data-related-category="${category}"]`
        )
        .classList.add("active");
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const slider3Container = document.querySelector(".slider__inner-container");
  const btnLeft = document.querySelector(".slider__btn_left");
  const btnRight = document.querySelector(".slider__btn_right");
  const totalSlides = slider3Container.children.length;
  let currentIndex = 0;

  function updateButtons() {
    btnLeft.disabled = currentIndex === 0;
    btnRight.disabled = currentIndex === totalSlides - 1;
  }

  const moveToSlide = (index) => {
    const slideWidth =
      document.documentElement.style.getPropertyValue("--_slide-width") ||
      "1075px";
    const slideWidthValue = parseInt(slideWidth.replace("px", ""));
    slider3Container.style.transform = `translateX(-${
      index * slideWidthValue
    }px)`;
    updateButtons();
  };

  const nextSlide = () => {
    if (currentIndex < totalSlides - 1) {
      currentIndex++;
      moveToSlide(currentIndex);
    }
  };

  const prevSlide = () => {
    if (currentIndex > 0) {
      currentIndex--;
      moveToSlide(currentIndex);
    }
  };

  moveToSlide(currentIndex);

  btnRight.addEventListener("click", nextSlide);
  btnLeft.addEventListener("click", prevSlide);
});
