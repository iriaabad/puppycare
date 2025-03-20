    // Al cargar la página, se verifica si el usuario está autenticado.
    fetch("http://127.0.0.1:8000/auth/users/me", {
        method: "GET",
        credentials: "include" // Envía la cookie de sesión
    })
    .then(response => {
        if (response.status === 200) {
            // Usuario autenticado: redirige a la página de área de cliente.
            window.location.href = "/puppyCare/PuppyCare/cliente/areacliente.html";
        }
        // Si la respuesta es 401 o cualquier otro código, no se realiza ninguna acción
    })
    .catch(error => {
        // En caso de error, no se realiza ninguna acción
    });

