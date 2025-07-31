document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn-toggle').forEach(btn =>
    btn.addEventListener('click', () => {
      const target = document.getElementById(btn.getAttribute('data-target'));
      target.classList.toggle('hidden');
    })
  );
});
