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