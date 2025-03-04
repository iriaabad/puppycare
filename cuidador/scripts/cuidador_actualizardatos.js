document.addEventListener("DOMContentLoaded", async function () {
    try {
        // Obtener datos del usuario autenticado
        const userResponse = await fetch("http://127.0.0.1:8000/auth/users/me", { method: "GET", credentials: "include" });
        if (!userResponse.ok) throw new Error(`Error de autenticación: ${userResponse.status}`);
        
        const userData = await userResponse.json();
        if (!userData.id_usuario) throw new Error("Error: id_usuario no encontrado.");

        const id_usuario = userData.id_usuario;
        cargarUsuario(id_usuario);

        // Manejo del envío del formulario
        document.getElementById("formularioparte2").addEventListener("submit", async function (event) {
            event.preventDefault();
            const datosActualizados = {};

            // Mapeo de campos
            const campos = ["nombre", "apellido1", "apellido2", "emailuser", "calle", "numero", "piso", "codigopostal", "ciudad"];
            campos.forEach(campo => {
                const input = document.getElementById(campo);
                if (input && input.value.trim()) datosActualizados[campo] = input.value.trim();
            });

            // Verificar si la dirección ha cambiado
            const direccionModificada = ["calle", "numero", "codigopostal", "ciudad"].some(campo => {
                return document.getElementById(campo).value.trim() !== document.getElementById(campo).getAttribute(`data-original-${campo}`);
            });

            if (direccionModificada) {
                const direccionCompleta = `${datosActualizados.calle} ${datosActualizados.numero} ${datosActualizados.codigopostal} ${datosActualizados.ciudad}`;
                const coordenadas = await obtenerCoordenadas(direccionCompleta);
                if (coordenadas) {
                    datosActualizados.latitud = coordenadas.lat;
                    datosActualizados.longitud = coordenadas.lon;
                } else {
                    console.error("No se pudieron obtener las coordenadas");
                }
            }

            if (Object.keys(datosActualizados).length > 0) {
                await actualizarUsuario(id_usuario, datosActualizados);
            }
        });

    } catch (error) {
        console.error("Error de autenticación o carga de usuario:", error);
    }
});

// Obtener coordenadas a partir de una dirección usando Nominatim
async function obtenerCoordenadas(direccion) {
    try {
        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(direccion)}`);
        if (!response.ok) throw new Error("Error al obtener coordenadas");

        const data = await response.json();
        return data.length > 0 ? { lat: parseFloat(data[0].lat), lon: parseFloat(data[0].lon) } : null;
    } catch (error) {
        console.error("Error al obtener coordenadas:", error);
        return null;
    }
}

// Cargar datos del usuario en el formulario
async function cargarUsuario(id_usuario) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/users/user/${id_usuario}`);
        if (!response.ok) throw new Error(`Error al obtener usuario: ${response.status}`);

        const data = await response.json();
        const mapping = { nombre: "nombre", apellido1: "apellido1", apellido2: "apellido2", emailuser: "email", calle: "calle", numero: "numero", piso: "piso", codigopostal: "codigopostal", ciudad: "ciudad" };

        Object.keys(mapping).forEach(campo => {
            const input = document.getElementById(campo);
            if (input) {
                input.value = data[mapping[campo]] ?? "";
                if (["calle", "numero", "codigopostal", "ciudad"].includes(campo)) {
                    input.setAttribute(`data-original-${campo}`, input.value);
                }
            }
        });

    } catch (error) {
        console.error("Error al cargar usuario:", error);
    }
}

// Actualizar datos del usuario
async function actualizarUsuario(id_usuario, datos) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/users/user/${id_usuario}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos)
        });

        if (!response.ok) throw new Error(`Error al actualizar usuario: ${response.status}`);

        console.log("Usuario actualizado correctamente");
        alert("Datos actualizados con éxito");

    } catch (error) {
        console.error("Error al actualizar usuario:", error);
    }
}
