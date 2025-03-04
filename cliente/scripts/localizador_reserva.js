// Código para obtener la geolocalización y llamar a initMap
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(initMap, function(error) {
        console.error("Error al obtener geolocalización:", error);
    });
} else {
    alert("Geolocalización no soportada");
}
// Declarar la variable globalmente
let map;

// Función para inicializar el mapa (se llama en initMap)
function initMap(position) {
    const userLat = position.coords.latitude;
    const userLng = position.coords.longitude;

    // Inicializar el mapa centrado en la ubicación del usuario y asignarlo a la variable global
    map = L.map('map').setView([userLat, userLng], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
       maxZoom: 19,
    }).addTo(map);
    // Forzar actualización del tamaño justo después de cargar el mapa
setTimeout(function() {
    if (map) {
        map.invalidateSize();
    }
}, 100); 



    

window.addEventListener("resize", function() {
    if (map) {
        map.invalidateSize();
    }
});

    // Llamada a la API para obtener cuidadores disponibles cercanos
    fetch(`/api/cuidadores/disponibles?lat=${userLat}&lng=${userLng}&radius=10`)
        .then(response => response.json())
        .then(cuidadores => {
            cuidadores.forEach(cuidador => {
                // Obtener las coordenadas directamente desde el objeto 'cuidador'
                const lat = cuidador.usuario.latitud;
                const lon = cuidador.usuario.longitud;

                if (lat && lon) {
                    // Crear el marcador para el cuidador con las coordenadas obtenidas
                    const marker = L.marker([lat, lon]).addTo(map);
                    marker.bindPopup(`
                        <b>${cuidador.nombre}</b><br>
                        <button onclick="seleccionarCuidador(${cuidador.id})">Seleccionar</button>
                    `);
                } else {
                    console.error(`No se pudo obtener coordenadas para ${cuidador.nombre}`);
                }
            });
        })
        .catch(err => console.error("Error al cargar cuidadores:", err));
}

// Función para asignar el cuidador seleccionado al formulario
function seleccionarCuidador(id) {
    document.getElementById('cuidador_id_cuidador').value = id;
    alert("Cuidador seleccionado: " + id);
}

// Manejo del envío del formulario de reserva
document.getElementById('reserva-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    // Envía la reserva a través de una petición POST al endpoint de reservas
    fetch("/reservas/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => {
        if(response.ok){
            alert("Reserva creada correctamente");
            this.reset();
        } else {
            alert("Error al crear la reserva");
        }
    })
    .catch(err => console.error("Error en el envío:", err));
});
