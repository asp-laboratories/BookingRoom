document.addEventListener('DOMContentLoaded', function() {
  // Tab 1: Tipo de Eventos
  const ctx1 = document.getElementById('chart-tipo-evento');
  if (ctx1) {
    new Chart(ctx1, {
      type: 'bar',
      data: {
        labels: ['Boda', 'Reunion', 'Ceremonia', 'Aniversario', 'Conferencia', 'Debate'],
        datasets: [{
          label: 'Cantidad de reservaciones',
          data: [12, 19, 3, 5, 2, 3],
          backgroundColor: 'rgba(209, 138, 91, 0.7)',
          borderWidth: 1
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
    });
  }

  const ctx1b = document.getElementById('chart-tipo-frecuente');
  if (ctx1b) {
    new Chart(ctx1b, {
      type: 'bar',
      data: {
        labels: ['Boda', 'Reunion', 'Conferencia'],
        datasets: [{
          label: 'Reservaciones',
          data: [45, 30, 20],
          backgroundColor: 'rgba(54, 162, 235, 0.7)',
          borderWidth: 1
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
    });
  }

  // Tab 2: Reservaciones
  const ctx2 = document.getElementById('chart-reservaciones-mes');
  if (ctx2) {
    new Chart(ctx2, {
      type: 'bar',
      data: {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        datasets: [{
          label: 'Reservaciones',
          data: [15, 22, 18, 25, 30, 28],
          backgroundColor: 'rgba(75, 192, 192, 0.7)',
          borderWidth: 1
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
    });
  }

  const ctx2b = document.getElementById('chart-reservaciones-dia');
  if (ctx2b) {
    new Chart(ctx2b, {
      type: 'bar',
      data: {
        labels: ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'],
        datasets: [{
          label: 'Reservaciones',
          data: [5, 8, 12, 15, 25, 30, 10],
          backgroundColor: 'rgba(255, 206, 86, 0.7)',
          borderWidth: 1
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
    });
  }

  // Tab 3: Ingresos
  const ctx3 = document.getElementById('chart-ingresos-servicios');
  if (ctx3) {
    new Chart(ctx3, {
      type: 'bar',
      data: {
        labels: ['Catering', 'Audio', 'Decoracion', 'Fotografia', 'Transporte'],
        datasets: [{
          label: 'Ingresos ($)',
          data: [15000, 8000, 12000, 5000, 3500],
          backgroundColor: 'rgba(153, 102, 255, 0.7)',
          borderWidth: 1
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
    });
  }

  const ctx3b = document.getElementById('chart-ingresos-totales');
  if (ctx3b) {
    new Chart(ctx3b, {
      type: 'bar',
      data: {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        datasets: [{
          label: 'Ingresos ($)',
          data: [45000, 52000, 48000, 61000, 55000, 60000],
          backgroundColor: 'rgba(75, 192, 192, 0.7)',
          borderWidth: 1
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
    });
  }

  // Tab 4: Estado
  const ctx4 = document.getElementById('chart-estado-reservaciones');
  if (ctx4) {
    new Chart(ctx4, {
      type: 'bar',
      data: {
        labels: ['Confirmada', 'Pendiente', 'Cancelada', 'Completada'],
        datasets: [{
          label: 'Reservaciones',
          data: [45, 20, 8, 60],
          backgroundColor: 'rgba(255, 99, 132, 0.7)',
          borderWidth: 1
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
    });
  }

  const ctx4b = document.getElementById('chart-salones-utilizados');
  if (ctx4b) {
    new Chart(ctx4b, {
      type: 'bar',
      data: {
        labels: ['Salón A', 'Salón B', 'Salón C', 'Salón D'],
        datasets: [{
          label: 'Veces utilizado',
          data: [35, 28, 22, 15],
          backgroundColor: 'rgba(54, 162, 235, 0.7)',
          borderWidth: 1
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
    });
  }
});