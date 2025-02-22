fetch("http://127.0.0.1:8000/auth/users/me", {
    method: "GET",
    credentials: "include" // Para enviar automáticamente la cookie de sesión
})
.then(response => {
    // Si la respuesta es 401 (no autenticado), lanzamos el error
    if (response.status === 401) {
        throw new Error("No autenticado");
    }
    return response.json();
})
.then(user => {
    console.log("Usuario autenticado:", user);
    mostrarPerfil(user);
})
.catch((error) => {
    // Muestra el botón de login si no se encuentra autenticado
    console.info(error);
    mostrarBotonLogin();
});

function mostrarPerfil(user) {
    document.getElementById("user-container").innerHTML = `
        <div class="user-profile">
            <a href="/perfil.html">
                <img src="${user.avatar || 'img/default-avatar.png'}" alt="Avatar">
                <span>${user.name}</span>
            </a>
            <a href="/logout" class="logout-button">Cerrar sesión</a>
        </div>
    `;
}

function mostrarBotonLogin() {
    document.getElementById("user-container").innerHTML = `
        <button href="/login.html" class="login-button">Iniciar sesión</button>
    `;
}
