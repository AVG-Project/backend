export default function handleScroll(container) {
  function handleScroll(e) {
    if (window.innerWidth > 768) {
      e.preventDefault();
      container.scrollLeft += e.deltaY;
    }
  }

  container.addEventListener("wheel", handleScroll);
}
