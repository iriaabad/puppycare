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
    
    // Verificar que id_usuario existe en la respuesta
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
              
                setTimeout(() => {
                    document.getElementById("nombre").value = data.nombre ?? '';   
                    document.getElementById("apellido1").value = data.apellido1 ?? '';  
                    document.getElementById("apellido2").value = data.apellido2 ?? '';  
                    document.getElementById("emailuser").value = data.email ?? ''; 
                    document.getElementById("calle").value = data.calle ?? ''; 
                    document.getElementById("numero").value = data.numero ?? ''; 
                    document.getElementById("piso").value = data.piso ?? ''; 
                    document.getElementById("codigopostal").value = data.codigopostal ?? ''; 
                    document.getElementById("ciudad").value = data.ciudad ?? ''; 
                }, 100); 
            })
            .catch(error => console.error("Error al cargar usuario:", error));
    }

    document.getElementById("editar-btn").addEventListener("click", function() {
        console.log("Modo edición activado.");
        document.querySelectorAll("#user-form input").forEach(input => input.disabled = false);
        document.getElementById("editar-btn").style.display = "none";
        document.getElementById("guardar-btn").style.display = "inline";
    });

    document.getElementById("user-form").addEventListener("submit", function(event) {
        event.preventDefault();
        
        const datosActualizados = {
            nombre: document.getElementById("nombre").value,
            apellido1: document.getElementById("apellido1").value,
            apellido2: document.getElementById("apellido2").value,
            email: document.getElementById("emailuser").value,
            calle: document.getElementById("calle").value,
            numero: document.getElementById("numero").value,
            piso: document.getElementById("piso").value,
            codigopostal: document.getElementById("codigopostal").value,
            ciudad: document.getElementById("ciudad").value,
        };

        console.log("Enviando datos actualizados:", datosActualizados);

        fetch(`http://127.0.0.1:8000/users/user/${id_usuario}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datosActualizados)
        })
        .then(response => {
            console.log("Respuesta de actualización recibida:", response);
            
            if (!response.ok) {
                throw new Error(`Error al actualizar usuario: ${response.status} ${response.statusText}`);
            }

            return response.json();
        })
        .then(data => {
            console.log("Usuario actualizado correctamente:", data);
            alert("Usuario actualizado correctamente");
            
            document.querySelectorAll("#user-form input").forEach(input => input.disabled = true);
            document.getElementById("editar-btn").style.display = "inline";
            document.getElementById("guardar-btn").style.display = "none";
        })
        .catch(error => console.error("Error al actualizar usuario:", error));
        alert("Error al actualizar, por favor revisa los datos introducidos");

    });

    cargarUsuario(id_usuario);  // Llamamos para cargar los datos del usuario

})
.catch(error => {
    console.error("Error de autenticación o carga de usuario:", error);
});
