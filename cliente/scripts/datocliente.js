// Al cargar la página, se verifica si el usuario está autenticado, para configurar el saludo
fetch("http://127.0.0.1:8000/auth/users/me", {
    method: "GET",
    credentials: "include" // Envía la cookie de sesión
})
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al obtener los datos del usuario');
        }
        return response.json();
    })
    .then(data => {
        // Verificamos si el nombre está presente
        const nombreUsuario = data.nombre ? data.nombre : ''; // Si el nombre no existe, dejamos la variable vacía
        const saludo = nombreUsuario.trim() ? `Bienvenid@, ${nombreUsuario}` : 'Bienvenid@'; // Si el nombre está vacío, mostramos 'Bienvenid@'
        document.getElementById('saludo-cliente').textContent = saludo;
    })
    .catch(error => {
        console.error('Error:', error);
    });
