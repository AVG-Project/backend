export default function handleResize(container) {
    if (window.innerWidth <= 768) {
      container.style.flexDirection = "column";
      container.style.overflowY = "scroll";
      container.style.overflowX = "hidden";
    } else {
      container.style.flexDirection = "row";
      container.style.overflowY = "hidden";
      container.style.overflowX = "scroll";
    }
  };