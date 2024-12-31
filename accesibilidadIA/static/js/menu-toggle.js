/* document.addEventListener('DOMContentLoaded', function() {
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
}); */
document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.querySelector("nav.sidebar");
  const mainContent = document.querySelector(".main-content");

  // Alternar el estado del menú lateral
  sidebar.addEventListener("mouseenter", () => {
    sidebar.classList.add("active"); // Mostrar el menú al pasar el mouse
  });

  sidebar.addEventListener("mouseleave", () => {
    sidebar.classList.remove("active"); // Ocultar el menú al salir
  });

  // Cierra el menú si se hace clic en un enlace
  sidebar.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      sidebar.classList.remove("active");
    });
  });
});

