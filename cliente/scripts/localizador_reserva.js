// Se ejecuta cuando el DOM está completamente cargado
document.addEventListener("DOMContentLoaded", async function () {

    // Verificar si la geolocalización está disponible y obtener la posición
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(initMap, function (error) {
        console.error("Error al obtener geolocalización:", error);
      });
    } else {
      alert("Geolocalización no soportada");
    }
  
    // Declarar la variable global para el mapa
    let map;
  
    // Función para inicializar el mapa; se llama cuando se obtiene la posición
    function initMap(position) {
      const userLat = position.coords.latitude;
      const userLng = position.coords.longitude;
  
      // Inicializar el mapa centrado en la posición del usuario y asignarlo a la variable global
      map = L.map("map").setView([userLat, userLng], 13);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
      }).addTo(map);
  
      //Se agrega un setTimeout para forzar el reajuste del tamaño del mapa tras su renderizado
      setTimeout(function () {
        if (map) {
          map.invalidateSize();
        }
      }, 100);
  
      // Se agrega un listener al evento "resize" para actualizar el tamaño del mapa al cambiar la ventana
      window.addEventListener("resize", function () {
        if (map) {
          map.invalidateSize();
        }
      });

      let markers = []; // Array para almacenar los marcadores y limpiarlos después
     

         // Función para obtener y mostrar los cuidadores en el mapa
        function cargarCuidadores(params = "") {
            fetch(`http://127.0.0.1:8000/cuidadores/obtener/disponibles?${params}`)
                .then(response => response.json())
                .then(cuidadores => {
                    // Limpiar los marcadores anteriores
                    markers.forEach(marker => map.removeLayer(marker));
                    markers = []; // Vaciar el array después de eliminarlos
        
                    // Agregar nuevos marcadores en el mapa para cada cuidador
                    cuidadores.forEach(cuidador => {
                        if (cuidador.usuario && cuidador.usuario.latitud && cuidador.usuario.longitud) {
                            const lat = cuidador.usuario.latitud;
                            const lon = cuidador.usuario.longitud;
                            const marker = L.marker([lat, lon]).addTo(map);
                            marker.bindPopup(`
                                <b>${cuidador.usuario.nombre} ${cuidador.usuario.apellido1}</b><br>
                                <b>${cuidador.descripcion}</b><br>
                                <button onclick="seleccionarCuidador(${cuidador.id})">Seleccionar</button>
                            `);
                            markers.push(marker); // Guardamos el marcador para luego eliminarlo
                        } else {
                            console.error(`No se pudo obtener coordenadas para ${cuidador.usuario ? cuidador.usuario.nombre : "cuidador desconocido"}. Datos:`, cuidador);
                        }
                    });
                })
                .catch(err => console.error("Error al cargar cuidadores:", err));
        }

        // Evento al presionar "Buscar"
        document.getElementById("buscar-btn").addEventListener("click", function() {
            const form = document.getElementById("reserva-form");
            const fecha_inicio = form.elements["fecha_inicio"].value;
            const fecha_fin = form.elements["fecha_fin"].value;
            const cantidad_mascotas = form.elements["cantidad_mascotas"].value;

            const params = new URLSearchParams();
            params.append("lat", userLat);
            params.append("lng", userLng);
            params.append("radius", 10);
            if (fecha_inicio) params.append("fecha_inicio", fecha_inicio);
            if (fecha_fin) params.append("fecha_fin", fecha_fin);
            if (cantidad_mascotas) params.append("cantidad_mascotas", cantidad_mascotas);

            // Cargar cuidadores con filtros
            cargarCuidadores(params.toString());
        });
     
         // Función para asignar el cuidador seleccionado (llamada desde el popup de cada marcador)
        function seleccionarCuidador(id) {
        document.getElementById("cuidador_id_cuidador").value = id;
        alert("Cuidador seleccionado: " + id);
      }
  
      // Manejo del envío del formulario ("Crear Reserva")
      document.getElementById("reserva-form").addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = {
          cuidador_id_cuidador: formData.get("cuidador_id_cuidador"),
          fecha_inicio: formData.get("fecha_inicio"),
          fecha_fin: formData.get("fecha_fin"),
          cantidad_mascotas: formData.get("cantidad_mascotas")
          // Agregar otros campos si es necesario
        };
  
        fetch("http://127.0.0.1:8000/reservas/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        })
          .then(response => {
            if (response.ok) {
              alert("Reserva creada correctamente");
              event.target.reset();
            } else {
              alert("Error al crear la reserva");
            }
          })
          .catch(err => console.error("Error en el envío:", err));
      });
    } // Fin de initMap
  
 
  
  });
  