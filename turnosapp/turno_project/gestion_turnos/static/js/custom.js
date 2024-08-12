document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      locale: 'es',
      dayCellDidMount: function(info) {
        if (info.date.getDate() === new Date().getDate() && 
            info.date.getMonth() === new Date().getMonth() && 
            info.date.getFullYear() === new Date().getFullYear()) {
          info.el.classList.add('fc-day-today');
        }
      },
      events: [
        {% for turno in turnos %}
        {
          title: '{{ turno.title }}',
          start: '{{ turno.start }}',
        },
        {% endfor %}
      ],
      dateClick: function(info) {
        var dateStr = info.dateStr;
        var event = calendar.getEvents().find(e => e.startStr.startsWith(dateStr));
        var content = event ? 
          `<p><strong>Paciente:</strong> ${event.title}</p><p><strong>Horario:</strong> ${event.start.toLocaleTimeString()}</p>` : 
          `<p>No hay turnos asignados</p>`;
        var modal = document.createElement('div');
        modal.innerHTML = `<div class="modal">
                              <div class="modal-content">
                                <span class="close">&times;</span>
                                ${content}
                              </div>
                            </div>`;
        document.body.appendChild(modal);
        document.querySelector('.close').onclick = function() {
          document.body.removeChild(modal);
        };
      }
    });
    calendar.render();
  });
  