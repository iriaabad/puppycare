    document.addEventListener("DOMContentLoaded", async function () {
        try {
            // Obtener datos del usuario autenticado
            const userResponse = await fetch("http://127.0.0.1:8000/auth/users/me", { method: "GET", credentials: "include" });
            if (!userResponse.ok) throw new Error(`Error de autenticación: ${userResponse.status}`);
            
            const userData = await userResponse.json();
            if (!userData.id_usuario) throw new Error("Error: id_usuario no encontrado.");
    
            const id_usuario = userData.id_usuario;
            
            // Obtener el id_cuidador asociado al usuario
            const cuidadorResponse = await fetch(`http://127.0.0.1:8000/cuidadores/select/?usuario_id_usuario=${id_usuario}`);
            if (!cuidadorResponse.ok) throw new Error("Error al obtener datos del cuidador");
    
            const cuidadorData = await cuidadorResponse.json();
    
            // Verificar si el array tiene datos
            if (!Array.isArray(cuidadorData) || cuidadorData.length === 0) {
                throw new Error("No se encontró un cuidador asociado a este usuario");
            }
    
            const id_cuidador = cuidadorData[0].id_cuidador; // Acceder al primer elemento del array
    
            // Cargar eventos del cuidador en el calendario
            const events = await cargarEventosCuidador(id_cuidador);
            inicializarCalendario(events);
    
        } catch (error) {
            console.error("Error:", error.message);
        }
    });
    
    /**
     * Función para obtener los eventos del calendario del cuidador
     */
    async function cargarEventosCuidador(id_cuidador) {
        try {
            // Obtener el ID del calendario del cuidador
            const eventosResponse = await fetch(`http://127.0.0.1:8000/calendario/eventos_por_cuidador/${id_cuidador}`);
            if (!eventosResponse.ok) throw new Error("Error al obtener el calendario del cuidador");
    
            const eventosData = await eventosResponse.json();

            // Convertir datos al formato de FullCalendar
            return eventosData.map(evento => ({
                title: evento.titulo || "Evento sin título",
                start: evento.fecha_inicio,
                end: evento.fecha_fin,
                reserva_id_reserva: evento.reserva_id_reserva || ""
            }));
    
        } catch (error) {
            console.error("Error:", error.message);
            return [];
        }
    }
    /**
 * Función para inicializar el calendario con los eventos obtenidos
 */
function inicializarCalendario(events) {
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: events,
        dateClick: function(info) {
            document.getElementById('event-form').style.display = 'block';
            document.getElementById('event-start').value = info.dateStr;
        }
    });
    calendar.render();
}


    // Manejar el botón de "Añadir Evento/Bloqueo"
    document.getElementById('add-event-btn').addEventListener('click', function() {
        document.getElementById('event-form').style.display = 'block';
    });

    // Manejar el envío del formulario de eventos
    document.getElementById('event-form-content').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const title = document.getElementById('event-title').value;
        const start = document.getElementById('event-start').value;
        const end = document.getElementById('event-end').value;
        const description = document.getElementById('event-description').value;

        // Agregar el evento al calendario
        calendar.addEvent({
            title: title,
            start: start,
            end: end,
            description: description
        });

        // Mostrar el evento en la lista de próximos eventos
        const eventList = document.getElementById('event-list');
        const eventItem = document.createElement('div');
        eventItem.classList.add('event-item');
        eventItem.innerHTML = `
            <strong>${title}</strong> (${start} - ${end})
            <p>${description}</p>
        `;
        eventList.appendChild(eventItem);

        // Ocultar el formulario
        document.getElementById('event-form').style.display = 'none';
        document.getElementById('event-form-content').reset();
    });
