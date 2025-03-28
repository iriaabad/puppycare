// Función para obtener coordenadas a partir de una dirección usando Nominatim
console.log("Script cargado correctamente");

function obtenerCoordenadas(direccion) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(direccion)}`;
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al obtener coordenadas");
            }
            return response.json();
        })
        .then(data => {
            if (data.length > 0) {
                const lat = parseFloat(data[0].lat);
                const lon = parseFloat(data[0].lon);
                return { lat, lon };
            } else {
                throw new Error("No se encontraron coordenadas para la dirección");
            }
        })
        .catch(error => {
            console.error("Error al obtener coordenadas:", error);
            return null;
        });
}

// Obtener datos del usuario autenticado

function processSessionInfo() {
    return fetch("akdsjhsak")
        .then(checkForError)
        .then(mapUserFromSessionInfo)
        .then(udpateForm)
}

fetch("http://127.0.0.1:8000/auth/users/me", {
    method: "GET",
    credentials: "include"
})
.then(response => {
    console.log("Respuesta de /auth/users/me recibida:", response);
    if (!response.ok) {
        throw new Error(`Error de autenticación: ${response.status} ${response.statusText}`);
    }
    return response.json();
})
.then(datoUsuario => {
    console.log("Datos del usuario autenticado:", datoUsuario);
    if (!datoUsuario.id_usuario) {
        throw new Error("Error: id_usuario no encontrado en la respuesta del servidor.");
    }
    const id_usuario = datoUsuario.id_usuario;

    document.addEventListener("DOMContentLoaded", function () {
        cargarUsuario(id_usuario);
    });

    function cargarUsuario(id_usuario) {
        console.log("Cargando usuario con ID:", id_usuario);
        fetch(`http://127.0.0.1:8000/users/user/${id_usuario}`)
            .then(response => {
                console.log("Respuesta de /users/user/{id_usuario} recibida:", response);
                if (!response.ok) {
                    throw new Error(`Error al obtener usuario: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Datos del usuario cargado:", data);
                // Asignar valores a los inputs y guardar el valor original en atributos data-original
                setTimeout(() => {
                    // Mapeo: clave = id del input en el formulario, valor = propiedad en data
                    const mapping = {
                        calle: "calle",
                        numero: "numero",
                        piso: "piso",
                        codigopostal: "codigopostal",
                        ciudad: "ciudad"
                    };
                
                    const campos = Object.keys(mapping);
                    campos.forEach(campo => {
                        const input = document.getElementById(campo);
                        // Obtener el valor usando el mapeo
                        let valor = data[mapping[campo]] ?? '';
                        input.value = valor;
                        // Para los campos de dirección se guardan atributos data-original
                        if (["calle", "numero", "codigopostal", "ciudad"].includes(campo)) {
                            input.setAttribute(`data-original-${campo}`, valor);
                        }
                    });
                }, 100);
                
            })
            .catch(error => console.error("Error al cargar usuario:", error));
    }

    // Manejo del envío del formulario desde cliente
    document.getElementById("formulariocrearcuentacuidador2").addEventListener("submit", function(event) {
        event.preventDefault();
        const datosActualizados = {};

        // Recopilar los valores actuales
        const nombre = document.getElementById("nombre").value.trim();
        const apellido1 = document.getElementById("apellido1").value.trim();
        const apellido2 = document.getElementById("apellido2").value.trim();
        const email = document.getElementById("emailuser").value.trim();
        const calle = document.getElementById("calle").value.trim();
        const numero = document.getElementById("numero").value.trim();
        const piso = document.getElementById("piso").value.trim();
        const codigopostal = document.getElementById("codigopostal").value.trim();
        const ciudad = document.getElementById("ciudad").value.trim();

        // Recopilar datos actualizados de todos los campos
        if (nombre) datosActualizados.nombre = nombre;
        if (apellido1) datosActualizados.apellido1 = apellido1;
        if (apellido2) datosActualizados.apellido2 = apellido2;
        if (email) datosActualizados.email = email;
        if (calle) datosActualizados.calle = calle;
        if (numero) datosActualizados.numero = numero;
        if (piso) datosActualizados.piso = piso;
        if (codigopostal) datosActualizados.codigopostal = codigopostal;
        if (ciudad) datosActualizados.ciudad = ciudad;

        // Comprobar si alguno de los campos de dirección ha cambiado respecto a su valor original
        const originalCalle = document.getElementById("calle").getAttribute("data-original-calle") || '';
        const originalNumero = document.getElementById("numero").getAttribute("data-original-numero") || '';
        const originalCP = document.getElementById("codigopostal").getAttribute("data-original-codigopostal") || '';
        const originalCiudad = document.getElementById("ciudad").getAttribute("data-original-ciudad") || '';

        const direccionModificada = (
            calle !== originalCalle ||
            numero !== originalNumero ||
            codigopostal !== originalCP ||
            ciudad !== originalCiudad
        );

        // Función para enviar la actualización (envío PUT)
        function enviarActualizacion() {
            if (Object.keys(datosActualizados).length === 0) {
                return;
            }
            console.log("Enviando datos actualizados:", datosActualizados);
            fetch(`http://127.0.0.1:8000/users/user/${id_usuario}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(datosActualizados)
            })
            .then(response => {
                console.log("Respuesta de actualización recibida:", response);
                if (!response.ok) {
                    throw new Error(`Error al actualizar usuario: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
    
            .catch(error => console.error("Error al actualizar usuario:", error));
        }

        if (direccionModificada) {
            // Concatenar la dirección completa
            const direccionCompleta = `${calle} ${numero} ${codigopostal} ${ciudad}`;
            obtenerCoordenadas(direccionCompleta).then(coordenadas => {
                if (coordenadas) {
                    datosActualizados.latitud = coordenadas.lat;
                    datosActualizados.longitud = coordenadas.lon;
                    console.log("Coordenadas obtenidas:", coordenadas);
                    enviarActualizacion();
                } else {
                    console.error("No se pudieron obtener las coordenadas");
                }
            });
        } else {
            enviarActualizacion();
        }
    });

    cargarUsuario(id_usuario);  // Cargar los datos del usuario
})
.catch(error => {
    console.error("Error de autenticación o carga de usuario:", error);
});
