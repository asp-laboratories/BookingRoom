const btnToggle = document.getElementById('toggle-sidebar');
const contenedor = document.getElementById('app-container');
let letras = document.querySelector('.letras')
let contenedorCerrado = document.querySelector(".sidebar-cerrado");

// Restaurar estado del sidebar desde localStorage
const sidebarState = localStorage.getItem('sidebar-cerrado');
if (sidebarState === 'true') {
    contenedor.classList.add('sidebar-cerrado');
    if (letras) letras.innerHTML = "BR";
}

btnToggle.addEventListener('click', () => {
    contenedor.classList.toggle('sidebar-cerrado');

    const isClosed = contenedor.classList.contains('sidebar-cerrado');
    localStorage.setItem('sidebar-cerrado', isClosed);

    if(!contenedor.classList.contains('sidebar-cerrado')){
        if (letras) letras.innerHTML = "BookingRoom"
    } else {
        if (letras) letras.innerHTML = "BR"
    }

});

const detailsList = document.querySelectorAll('.sidebar details');

console.log('Sidebar script loaded, found', detailsList.length, 'details');

// Restaurar estado de details desde localStorage
detailsList.forEach(details => {
  const summary = details.querySelector('summary .texto-menu');
  const sectionName = summary ? summary.textContent.trim() : 'unknown';
  const storedState = localStorage.getItem('sidebar-details-' + sectionName);
  console.log('Restoring', sectionName, 'state:', storedState);
  if (storedState === 'true') {
    details.open = true;
  }
});

detailsList.forEach(details => {
  const contenido = details.querySelector('.deslizar');
  const summary = details.querySelector('summary .texto-menu');
  const sectionName = summary ? summary.textContent.trim() : 'unknown';
  
  details.addEventListener('toggle', function() {
    localStorage.setItem('sidebar-details-' + sectionName, details.open);
    
    if (details.open) {
      contenido.style.animation = 'none';
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

// Mobile: Keep details always open (solo abrir en móvil, no cerrar en desktop)
function setupMobileDetails() {
  const isMobile = window.innerWidth <= 768;
  
  if (isMobile) {
    detailsList.forEach(details => {
      details.open = true;
    });
  }
}

// Run on load and resize
setupMobileDetails();
window.addEventListener('resize', setupMobileDetails);