const btnToggle = document.getElementById('toggle-sidebar');
const contenedor = document.getElementById('app-container');
let letras = document.querySelector('.letras')
let contenedorCerrado = document.querySelector(".sidebar-cerrado");

btnToggle.addEventListener('click', () => {
    contenedor.classList.toggle('sidebar-cerrado');

    if(!contenedor.classList.contains('sidebar-cerrado')){
        letras.innerHTML = "BookingRoom"
    } else {
        letras.innerHTML = "BR"
    }

});

const detailsList = document.querySelectorAll('details');

detailsList.forEach(details => {
  const contenido = details.querySelector('.deslizar');
  
  details.addEventListener('toggle', function() {
    if (details.open) {
      
      contenido.style.animation = 'none';
      // Forzar reflow
      contenido.offsetHeight;
      contenido.style.animation = 'slideDown 0.7s ease-out';
    }
  });
});

// Mobile sidebar functionality
const btnMenuMobile = document.getElementById('btn-menu-mobile');
const sidebar = document.getElementById('sidebar');
const overlaySidebar = document.getElementById('overlay-sidebar');

function toggleMobileSidebar() {
  sidebar.classList.toggle('abierto');
  overlaySidebar.classList.toggle('abierto');
  contenedor.classList.toggle('sidebar-abierto');
}

if (btnMenuMobile) {
  btnMenuMobile.addEventListener('click', toggleMobileSidebar);
}

if (overlaySidebar) {
  overlaySidebar.addEventListener('click', toggleMobileSidebar);
}

// Close sidebar when clicking a link on mobile
const sidebarLinks = document.querySelectorAll('.sidebar a');
sidebarLinks.forEach(link => {
  link.addEventListener('click', () => {
    if (window.innerWidth <= 768) {
      toggleMobileSidebar();
    }
  });
});

// Mobile: Keep details always open
function setupMobileDetails() {
  const isMobile = window.innerWidth <= 768;
  const detailsList = document.querySelectorAll('.sidebar details');
  
  detailsList.forEach(details => {
    if (isMobile) {
      details.setAttribute('open', '');
    } else {
      details.removeAttribute('open');
    }
  });
}

// Run on load and resize
setupMobileDetails();
window.addEventListener('resize', setupMobileDetails);