export default function initModals() {
  // openButtons are buttons that open one modal and close the current one if it exists
    const openButtons = document.querySelectorAll('[data-modal]');
    const closeButtons = document.querySelectorAll('.modal__close');
  
    function openModal(modal) {
      modal.classList.add("active");
    }
  
    function closeModal(modal) {
      modal.classList.remove("active");
    }
  
    openButtons.forEach(button => {
      const targetOpenModalId = button.getAttribute('data-modal');
      const closeModalId = button.getAttribute('data-close-modal');
  
      button.addEventListener('click', (e) => {
        e.preventDefault();
        if (closeModalId) {
          const targetCloseModal = document.getElementById(closeModalId);
          closeModal(targetCloseModal);
        }
        const targetOpenModal = document.getElementById(targetOpenModalId);
        openModal(targetOpenModal);
      });
    });
  
    closeButtons.forEach(button => {
      const modalId = button.getAttribute('data-modal');
      const modal = document.getElementById(modalId);
  
      button.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        closeModal(modal)
      });
    });
  
    window.addEventListener('click', (event) => {
      if (event.target.classList.contains('modal')) {
        closeModal(event.target);
      }
    });
  
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
          closeModal(modal);
        });
      }
    });
  }
  