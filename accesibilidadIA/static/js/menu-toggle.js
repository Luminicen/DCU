document.addEventListener('DOMContentLoaded', function() {
  const menuButton = document.getElementById('menu-button');
  const menu = document.querySelector('nav');
  const mainContent = document.querySelector('.main-content');

  menuButton.addEventListener('click', function() {
    menu.classList.toggle('active');
    mainContent.classList.toggle('hidden'); 
  });

  menu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', function() {
      menu.classList.remove('active');
      mainContent.classList.remove('hidden'); 
    });
  });
});

