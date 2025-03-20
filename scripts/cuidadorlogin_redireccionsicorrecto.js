    // Al cargar la página, se verifica si el usuario está autenticado.
    fetch("http://127.0.0.1:8000/auth/users/me", {
        method: "GET",
        credentials: "include" // Envía la cookie de sesión
    })
    .then(response => {
        if (response.status === 200) {
            // Usuario autenticado: redirige a la página de 
            window.location.href = "/puppyCare/PuppyCare/cuidador/areacuidador.html";
        }
        // Si la respuesta es 401 o cualquier otro código, no se realiza ninguna acción
    })
    .catch(error => {
        // En caso de error, no se realiza ninguna acción
    });


    //pendiente añadir validacion de que el cuidador esté dado de alta para ese usuario