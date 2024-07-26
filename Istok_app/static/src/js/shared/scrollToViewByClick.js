

export default function initScrollToViewByClick(controls) {
  function scrollToItem(itemId) {
    const element = document.getElementById(itemId);

  
    element.scrollIntoView({
      behavior: "smooth",
      alignToTop: false,
      block: "end",
    });
  }

  controls.forEach((control) => {
    control.addEventListener("click", () => {
      const sectionId = control.getAttribute("data-related-section-id");
      if (sectionId) {
        scrollToItem(sectionId);
      }
    });
  });
}