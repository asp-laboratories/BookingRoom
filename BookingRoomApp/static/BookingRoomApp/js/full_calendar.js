document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      locale: 'es', // Para ponerlo en español
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      // Aquí es donde conectarás con Django después
      events: [
        { title: 'Evento de prueba', start: '2026-03-01' }
      ]
    });
    calendar.render();
    calendar.updateSize();
  });