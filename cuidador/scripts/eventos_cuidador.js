// Declarar la variable global para la instancia del calendario
let calendar;

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
        if (!Array.isArray(cuidadorData) || cuidadorData.length === 0) {
            throw new Error("No se encontró un cuidador asociado a este usuario");
        }
        const id_cuidador = cuidadorData[0].id_cuidador;
    
        // Cargar eventos del cuidador en el calendario
        const events = await cargarEventosCuidador(id_cuidador);
        inicializarCalendario(events);
    
        // Actualizar la lista de eventos de forma global
        actualizarListaEventos();
    } catch (error) {
        console.error("Error:", error.message);
    }
    
    // Poblar el select de tipo de evento al cargar la página
    const tipoSelect = document.getElementById("event-tipo_evento");
    fetchSelectOptions("http://127.0.0.1:8000/tipo_evento/", tipoSelect, "id_tipo_evento", "descripcion");
});

/**
 * Función para obtener los eventos del calendario del cuidador
 */
async function cargarEventosCuidador(id_cuidador) {
    try {
        const eventosResponse = await fetch(`http://127.0.0.1:8000/eventos-calendario/eventos_por_cuidador/${id_cuidador}`);
        if (!eventosResponse.ok) throw new Error("Error al obtener el calendario del cuidador");
        const eventosData = await eventosResponse.json();
        // Convertir datos al formato que usa FullCalendar
        return eventosData.map(evento => ({
            title: evento.title || "Evento sin título",
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
    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: events,
        dateClick: function(info) {
            document.getElementById('event-form').style.display = 'block';
            document.getElementById('event-start').value = info.dateStr;
        }
    });
    calendar.render();
}

/**
 * Función para actualizar la lista de eventos (mostrados en un contenedor global)
 */
function actualizarListaEventos() {
    const eventList = document.getElementById("event-list");
    eventList.innerHTML = "";
    // Obtener los eventos del calendario
    const events = calendar.getEvents();
    events.forEach(event => {
        // Formatear las fechas si es necesario
        const start = event.start ? event.start.toLocaleString() : "";
        const end = event.end ? event.end.toLocaleString() : "";
        const eventItem = document.createElement("div");
        eventItem.classList.add("event-item");
        eventItem.innerHTML = `<strong>${event.title}</strong> (${start} - ${end})`;
        eventList.appendChild(eventItem);
    });
}

// Manejar el botón de "Añadir Evento/Bloqueo"
document.getElementById('add-event-btn').addEventListener('click', function() {
    document.getElementById('event-form').style.display = 'block';
});

// Manejar el envío del formulario de eventos
document.getElementById('event-form-content').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const start = document.getElementById('event-start').value;
    const end = document.getElementById('event-end').value;
    const tipoSelect = document.getElementById('event-tipo_evento');
    // Obtener tanto el id como el texto (descripción) del tipo seleccionado
    const tipoEventoText = tipoSelect.options[tipoSelect.selectedIndex].text;
    // Construir el título concatenando la descripción del tipo y las fechas
    const title = `${tipoEventoText} (${start} - ${end})`;
    
    // Agregar el evento al calendario usando la instancia global
    calendar.addEvent({
        title: title,
        start: start,
        end: end
    });
    
    // Actualizar la lista de eventos tras agregar uno nuevo
    actualizarListaEventos();
    
    // Ocultar y resetear el formulario
    document.getElementById('event-form').style.display = 'none';
    document.getElementById('event-form-content').reset();
});

/**
 * Función para poblar un select con datos obtenidos de un endpoint
 */
async function fetchSelectOptions(url, selectElement, idField, nameField) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item[idField];
            option.textContent = item[nameField];
            selectElement.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching options:", error);
    }
}
