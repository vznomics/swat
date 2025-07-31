document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.dropdown-btn').forEach((btn, index) => {
    btn.addEventListener('click', () => {
      const shareBox = btn.closest('.share-box');
      shareBox.classList.toggle('open');
    });
  });

  window.confirmDelete = function (formId) {
    if (confirm("Are you sure you want to delete this share?")) {
      document.getElementById(formId).submit();
    }
  };
});
