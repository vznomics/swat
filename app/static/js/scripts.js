document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const tgt = document.getElementById(btn.getAttribute('data-target'));
      tgt.classList.toggle('hidden');
    });
  });
});
