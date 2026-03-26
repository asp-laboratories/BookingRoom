document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      locale: 'es',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      eventColor: '#9c5c31',
      events: '/api/calendario-eventos/',
      eventBackgroundColor: '#9c5c31',
      eventBorderColor: '#9c5c31',
      eventTextColor: '#ffffff',
    });
    calendar.render();
    calendar.updateSize();
  });