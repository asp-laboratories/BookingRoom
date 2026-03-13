  const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Boda', 'Reunion', 'Ceremonia', 'Aniversario', 'Conferencia', 'Debate'],
      datasets: [{
        label: '# cantidad de reservaciones',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1,
        backgroundColor: [
        'rgba(209, 138, 91, 0.6)',
        'rgba(209, 138, 91, 0.6)',
        'rgba(209, 138, 91, 0.6)',
        'rgba(209, 138, 91, 0.6)',
        'rgba(209, 138, 91, 0.6)',
        'rgba(209, 138, 91, 0.6)',

    ],
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });