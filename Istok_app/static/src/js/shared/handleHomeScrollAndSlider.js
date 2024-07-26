export default function initHomeScrollAndSlider1(container) {
  const projects = document.getElementById("products");
  const sliderInnerContainer = document.querySelector(
    ".page3__slider-inner-container"
  );

  const projectSectionStopScrollPosition = 490;
  let sliderActive = false;
  // TransformX values of the slider to set the range of motion
  const initialTransformX = 493;
  const minTransform = -567;
  const maxTransform = initialTransformX;
  
  function handleScroll(e) {
    if (window.innerWidth > 768) {
      const projectsRect = projects.getBoundingClientRect();
  
      // Check if the slider section is in view
      const isSliderInView = projectsRect.left <= projectSectionStopScrollPosition && projectsRect.right >= 0;
  
      if (sliderActive || isSliderInView) {
        if (!sliderActive && isSliderInView) {
          sliderActive = true;
          e.preventDefault();
        }
  
        if (sliderActive) {
          e.preventDefault();
          const delta = e.deltaY;
          const currentTransform = getCurrentTransformX(sliderInnerContainer);
          let newTransform = currentTransform - delta;
  
          if (newTransform < minTransform) {
            newTransform = minTransform;
          } else if (newTransform > maxTransform) {
            newTransform = maxTransform;
          }
  
          sliderInnerContainer.style.transform = `translateX(${newTransform}px)`;
          if (newTransform === minTransform || newTransform === maxTransform) {
            sliderActive = false;
            container.style.overflowX = "scroll";
            container.scrollLeft += e.deltaY;
          }
        } else {
          container.scrollLeft += e.deltaY;
        }
      } else {

        sliderInnerContainer.style.transform = `translateX(${initialTransformX}px)`;
        container.scrollLeft += e.deltaY;
      }
    }
  }
  
  const getCurrentTransformX = (element) => {
    const style = window.getComputedStyle(element);
    const matrix = new WebKitCSSMatrix(style.transform);
    return matrix.m41;
  };
  
  container.addEventListener('wheel', handleScroll, { passive: false });
}
