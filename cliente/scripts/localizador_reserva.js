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

    // Declarar variables globales
    let map;
    let markers = []; // Array para almacenar los marcadores y limpiarlos después
    let cuidadorSeleccionado = null;
    let clienteId = null;




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
        }, 50);

        // Se agrega un listener al evento "resize" para actualizar el tamaño del mapa al cambiar la ventana
        window.addEventListener("resize", function () {
            if (map) {
                map.invalidateSize();
            }
        });

        function cargarCuidadores(params = "") {
            fetch(`http://127.0.0.1:8000/cuidadores/obtener/disponibles?${params}`)
                .then(response => response.json())
                .then(cuidadores => {
                    // Obtener ubicación del usuario
                    const userLat = map.getCenter().lat;
                    const userLng = map.getCenter().lng;

                    // Calcular la distancia de cada cuidador y ordenar
                    cuidadores.forEach(cuidador => {
                        if (cuidador.usuario && cuidador.usuario.latitud && cuidador.usuario.longitud) {
                            cuidador.distancia = calcularDistancia(userLat, userLng, cuidador.usuario.latitud, cuidador.usuario.longitud);
                        } else {
                            cuidador.distancia = Infinity; // Si no tiene coordenadas, ponerlo al final
                        }
                    });

                    // Ordenar de menor a mayor distancia
                    cuidadores.sort((a, b) => a.distancia - b.distancia);

                    // Limpiar lista y marcadores previos
                    document.getElementById("lista-cuidadores").innerHTML = "";
                    markers.forEach(marker => map.removeLayer(marker));
                    markers = [];

                    // Agregar cuidadores ordenados a la lista y al mapa
                    cuidadores.forEach((cuidador, index) => {
                        if (cuidador.usuario && cuidador.usuario.latitud && cuidador.usuario.longitud) {
                            const lat = cuidador.usuario.latitud;
                            const lon = cuidador.usuario.longitud;

                            // Agregar marcador con número
                            const marker = L.marker([lat, lon], {
                                icon: L.divIcon({
                                    className: "custom-marker",
                                    html: `<div class="marker-number">${index + 1}</div>`,
                                    iconSize: [25, 25]
                                })
                            }).addTo(map);

                            markers.push(marker);

                            // Agregar a la lista
                            const lista = document.getElementById("lista-cuidadores");
                            const item = document.createElement("div");
                            item.classList.add("cuidador-item");
                            item.innerHTML = `
                            <span class="numero">${index + 1}</span>
                            <h3>${cuidador.usuario.nombre} ${cuidador.usuario.apellido1}</h3>
                            <p>${cuidador.descripcion}</p>
                            <p><strong>Distancia:</strong> ${cuidador.distancia.toFixed(2)} km</p>
                            <button class="seleccionar-btn" data-id="${cuidador.id_cuidador}">Seleccionar</button>
                        `;
                            lista.appendChild(item);
                        }
                    });

                    // Asignar eventos a los botones
                    asignarEventosSeleccion(cuidadores);
                })
                .catch(err => console.error("Error al cargar cuidadores:", err));
        }

        //Función para calcular distancia entre dos puntos (Haversine)
        function calcularDistancia(lat1, lon1, lat2, lon2) {
            const R = 6371; // Radio de la Tierra en km
            const dLat = (lat2 - lat1) * (Math.PI / 180);
            const dLon = (lon2 - lon1) * (Math.PI / 180);
            const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            return R * c;
        }


        function asignarEventosSeleccion(cuidadores) {
            // Ordenar cuidadores por distancia al usuario
            cuidadores.sort((a, b) => a.distancia - b.distancia);

            const listaCuidadores = document.getElementById("lista-cuidadores");
            listaCuidadores.innerHTML = ""; // Limpiar la lista antes de agregar nuevos

            cuidadores.forEach((cuidador, index) => {
                console.log("Cuidador:", cuidador);
                // Crear elemento de la lista
                const item = document.createElement("div");
                item.classList.add("cuidador-item");
                item.innerHTML = `
                    <span class="cuidador-numero">${index + 1}</span>
                    <h3>${cuidador.usuario.nombre} ${cuidador.usuario.apellido1}</h3>
                    <p>${cuidador.descripcion}</p>
                    <button class="seleccionar-btn" data-id="${cuidador.id_cuidador}">Seleccionar</button>
                `;

                listaCuidadores.appendChild(item);

                // Agregar marcador numerado en el mapa
                const marker = L.marker([cuidador.usuario.latitud, cuidador.usuario.longitud], {
                    icon: L.divIcon({
                        className: 'custom-marker',
                        html: `<div class="marker-label">${index + 1}</div>`
                    })
                }).addTo(map);

                // Asignar evento de selección
                item.querySelector(".seleccionar-btn").addEventListener("click", () => {
                    seleccionarCuidador(cuidador.id_cuidador, cuidadores);
                });
            });
        }
        // Evento al presionar "Buscar"
        document.getElementById("buscar-btn").addEventListener("click", function () {
            const form = document.getElementById("reserva-form");
            if (form.checkValidity()) {
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
            } else {
                // Muestra los mensajes de validación nativos del navegador
                form.reportValidity();
            }

        });

        async function seleccionarCuidador(id, cuidadores) {
            const cuidador = cuidadores.find(c => c.id_cuidador == id);
            if (!cuidador) {
                alert("Error: No se encontró el cuidador.");
                return;
            }

            // Obtener los detalles completos del cuidador seleccionado
            const detallesCuidador = await obtenerCuidadorPorId(id);

            // Asignamos los detalles completos a la variable global
            cuidadorSeleccionado = detallesCuidador;

            // Actualizar los detalles en la interfaz
            document.getElementById("detalles-reserva").innerHTML = `
                <h3>${detallesCuidador.usuario.nombre} ${detallesCuidador.usuario.apellido1}</h3>
                <p>${detallesCuidador.descripcion}</p>
                <p>Tarifa/día: ${detallesCuidador.tarifa_dia}€</p>
        
                <button id="submit-form">Confirmar reserva</button>
            `;

            // Asignar el evento para confirmar la reserva
            document.getElementById("submit-form").addEventListener("click", function (event) {
                event.preventDefault();
                crearReserva(event, id);
            });
        }



        // Función para obtener el cliente actual
        async function obtenerCliente() {
            try {
                // Hacer la solicitud para obtener el usuario actual
                const userResponse = await fetch("http://127.0.0.1:8000/auth/users/me", {
                    method: "GET",
                    credentials: "include" // Para enviar automáticamente la cookie de sesión
                });
                const user = await userResponse.json(); // Asumiendo que la respuesta es un JSON
                console.log("Usuario actual:", user);  // Verifica la respuesta completa

                // Usamos el user_id para obtener el cliente
                const userId = user.id_usuario;

                // Hacer otra solicitud para obtener el cliente usando el userId
                const clienteResponse = await fetch(`http://127.0.0.1:8000/clientes/usuario/${userId}`, {
                    method: "GET",
                    credentials: "include"
                });
                const cliente = await clienteResponse.json();

                console.log("Cliente encontrado:", cliente);
                return cliente.id_cliente; // Retornamos el id del cliente directamente
            } catch (error) {
                console.error("Error al obtener el cliente:", error);
            }
        }


        // Manejo del envío del formulario ("Crear Reserva")
        async function crearReserva(event, id) {
            // Obtenemos el formulario y sus datos
            const form = document.getElementById("reserva-form");
            const clienteId = await obtenerCliente(); // Obtener el id del cliente de manera asincrónica

            // Verificar si se obtuvo el clienteId
            if (!clienteId) {
                alert("No se pudo obtener el ID del cliente.");
                return;
            }

            const formData = new FormData(form);
            const fechaInicio = formData.get("fecha_inicio");
            const fechaFin = formData.get("fecha_fin");
            const cantidadMascotas = formData.get("cantidad_mascotas");

            // Asegúrate de que los datos sean válidos
            if (!fechaInicio || !fechaFin || parseInt(cantidadMascotas) <= 0) {
                alert("Por favor, completa todos los campos correctamente.");
                return;
            }

            // Obtener el precio de la reserva
            const tarifaDia = cuidadorSeleccionado ? cuidadorSeleccionado.tarifa_dia : 0;
            console.log(cuidadorSeleccionado ? cuidadorSeleccionado.tarifa_dia : 0)
            const precioReserva = calcularPrecioReserva(fechaInicio, fechaFin, cantidadMascotas, tarifaDia);

            if (precioReserva <= 0) {
                alert("Hubo un error con el cálculo del precio.");
                return;
            }

            const data = {
                cuidador_id_cuidador: cuidadorSeleccionado.id_cuidador,
                fecha_inicio: fechaInicio,
                fecha_fin: fechaFin,
                cantidad_mascotas: cantidadMascotas,
                cliente_id_cliente: clienteId,
                precio_total: precioReserva,
                estado_reserva_id_estado: "2"
            };
            // Verificar que se haya seleccionado un cuidador
            if (!data.cuidador_id_cuidador) {
                alert("Debe seleccionar un cuidador.");
                return;
            }

            // Verificar que la cantidad de mascotas no sea cero
            if (parseInt(data.cantidad_mascotas) === 0) {
                alert("La cantidad de mascotas debe ser mayor a cero.");
                return;

            }

            // Realizar la petición para crear la reserva
            fetch("http://127.0.0.1:8000/reservas/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            })
                .then(response => {
                    if (response.ok) {
                        alert("Reserva creada correctamente");
                        form.reset();
                    } else {
                        alert("Error al crear la reserva");
                    }
                })
                .catch(err => console.error("Error en el envío:", err));
        }
    
}
    function calcularPrecioReserva(fecha_inicio, fecha_fin, cantidadMascotas, tarifaDia) {
        // Convertir las fechas a objetos Date
        const inicio = new Date(fecha_inicio);
        const fin = new Date(fecha_fin);

        // Calcular la diferencia en milisegundos entre las fechas
        const diferenciaMs = fin - inicio;

        // Verificar que la fecha de fin sea posterior a la fecha de inicio
        if (diferenciaMs < 0) {
            alert("La fecha de fin debe ser posterior a la fecha de inicio.");
            return 0;
        }

        // Calcular el número de días de la reserva
        const diasReserva = Math.ceil(diferenciaMs / (1000 * 3600 * 24)); // 1000 ms * 3600 s * 24 h

        // Calcular el precio total de la reserva
        const precioTotal = diasReserva * tarifaDia * cantidadMascotas;

        return precioTotal;
    }

    async function obtenerCuidadorPorId(idCuidador) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/cuidadores/recibir/${idCuidador}`, {
                method: "GET",
                credentials: "include" // Para enviar la cookie de sesión si es necesario
            });
            const cuidador = await response.json();
            console.log("Datos del cuidador:", cuidador);
            return cuidador; // Devuelve los detalles completos del cuidador
        } catch (error) {
            console.error("Error al obtener el cuidador:", error);
        }
    }
    

});