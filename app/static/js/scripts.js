document.addEventListener('DOMContentLoaded', () => {
  const toggles = document.querySelectorAll('.btn-toggle');

  toggles.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const targetElem = document.getElementById(targetId);

      if (targetElem) {
        targetElem.classList.toggle('hidden');
      }
    });
  });
});
