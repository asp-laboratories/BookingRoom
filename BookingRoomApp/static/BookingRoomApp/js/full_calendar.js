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
        { title: 'Evento de prueba', start: '2026-03-01' },
        { title: 'Mi evento', start: '2026-03-10' },
        { title: 'Presentacion Web :)', start: '2026-03-13' },
        { title: 'Funeral de ricardo', start: '2026-03-24' },
      ]
    });
    calendar.render();
    calendar.updateSize();
  });