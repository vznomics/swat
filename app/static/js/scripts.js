document.addEventListener('DOMContentLoaded', () => {
  // Abrir/Cerrar ajustes por tarjeta
  document.querySelectorAll('.settings-toggle').forEach(button => {
    button.addEventListener('click', () => {
      const box = button.closest('.share-box');
      box.classList.toggle('open');
    });
  });

  // Modal
  const openModalBtn = document.getElementById('openModalBtn');
  const modal = document.getElementById('createShareModal');
  const closeModalBtn = document.getElementById('closeModalBtn');

  if (openModalBtn && modal && closeModalBtn) {
    openModalBtn.addEventListener('click', () => {
      modal.style.display = 'flex';
    });

    closeModalBtn.addEventListener('click', () => {
      modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.style.display = 'none';
      }
    });
  }

  // Confirmación al eliminar
  window.confirmDelete = function (formId) {
    if (confirm("Are you sure you want to delete this share?")) {
      document.getElementById(formId).submit();
    }
  };
});
