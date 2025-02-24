// Al cargar la página, se verifica si el usuario está autenticado
fetch("http://127.0.0.1:8000/auth/users/me", {
    method: "GET",
    credentials: "include" // Envia la cookie de sesión
})
    .then(response => {
        if (response.status === 200) {
            // Usuario autenticado: ocultar el formulario de login
            document.getElementById('formulariologin').style.display = 'none';
            // Mostrar contenido habitual
            document.getElementById('areacliente').style.display = 'block';
        } else {
            // Si no está autenticado, mostrar solo el formulario de login
            document.getElementById('formulariologin').style.display = 'block';
            // Ocultar contenido habitual
            document.getElementById('areacliente').style.display = 'none';
        }
    })
    .catch(error => {
        // En caso de error, muestra el formulario de login
        console.error('Error al verificar la autenticación:', error);
        document.getElementById('formulariologin').style.display = 'block';
        // Ocultar contenido habitual
        document.getElementById('areacliente').style.display = 'none';
    });


