document.addEventListener('DOMContentLoaded', function() {
  const menuButton = document.getElementById('menu-button');
  const menu = document.querySelector('nav');

  menuButton.addEventListener('click', function() {
    menu.classList.toggle('active');
    document.querySelector('.main-content').classList.toggle('shifted'); 
  });
});