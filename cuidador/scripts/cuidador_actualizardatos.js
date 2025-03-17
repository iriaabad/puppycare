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
        cargarDatosCuidador(id_cuidador);


        // Manejo del botón de edición
        document.getElementById("editar-btn").addEventListener("click", function () {
            document.querySelectorAll("#cuidador-form input").forEach(input => input.removeAttribute("disabled"));
            document.getElementById("guardar-btn").style.display = "inline-block";
            document.getElementById("editar-btn").style.display = "none";
        });

        // Manejo del envío del formulario
        document.getElementById("cuidador-form").addEventListener("submit", async function (event) {
            event.preventDefault();
            const datosActualizados = {};
            
            const campos = ["tarifa_dia", "capacidad_mascotas", "descripcion", "disponibilidad_activa"];
            campos.forEach(campo => {
                const input = document.getElementById(campo);
                if (input) {
                    if (input.type === "checkbox") {
                        datosActualizados[campo] = input.checked;
                    } else {
                        datosActualizados[campo] = input.value.trim();
                    }
                }
            });
            if (datosActualizados["descripcion_cuidador"] !== undefined) {
                datosActualizados["descripcion"] = datosActualizados["descripcion_cuidador"];
                delete datosActualizados["descripcion_cuidador"];
            }

            if (Object.keys(datosActualizados).length > 0) {
                await actualizarCuidador(id_cuidador, datosActualizados);
            }
        });

    } catch (error) {
        console.error("Error de autenticación o carga de datos del cuidador:", error);
    }
});

// Cargar datos del cuidador en el formulario
async function cargarDatosCuidador(id_cuidador) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/cuidadores/recibir/${id_cuidador}`);
        if (!response.ok) throw new Error(`Error al obtener datos del cuidador: ${response.status}`);
        
        const data = await response.json();
        document.getElementById("tarifa_dia").value = data.tarifa_dia ?? "";
        document.getElementById("capacidad_mascotas").value = data.capacidad_mascota ?? "";
        document.getElementById("descripcion").value = data.descripcion ?? "";
        document.getElementById("disponibilidad_activa").checked = data.disponibilidad_activa ?? false;
    } catch (error) {
        console.error("Error al cargar datos del cuidador:", error);
    }
}

// Actualizar datos del cuidador
async function actualizarCuidador(id_cuidador, datos) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/cuidadores/modificar/${id_cuidador}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos)
        });

        if (!response.ok) throw new Error(`Error al actualizar cuidador: ${response.status}`);
        console.log("Datos del cuidador actualizados correctamente");
        alert("Datos actualizados con éxito");
        location.reload();
    } catch (error) {
        console.error("Error al actualizar datos del cuidador:", error);
    }
}
