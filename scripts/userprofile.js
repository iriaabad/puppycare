document.addEventListener("DOMContentLoaded", function() {
    fetch("http://127.0.0.1:8000/auth/users/me", {
        method: "GET",
        credentials: "include"
    })
    .then(response => {
        if (response.status === 401) throw new Error("No autenticado");
        return response.json();
    })
    .then(user => {
        cargarPerfil(user);
    })
    .catch(error => {
        console.info(error);
        mostrarBotonLogin();
    });
});

function cargarPerfil(user) {
    fetch("//localhost/puppyCare/PuppyCare/partials/user_profile.html")
        .then(response => response.text())
        .then(html => {
            document.getElementById("user-container").innerHTML = html;
            document.getElementById("user-name").textContent = user.nombre;
        })
        .catch(error => console.error("Error cargando el perfil:", error));
}

function mostrarBotonLogin() {
    document.getElementById("user-container").innerHTML = `
        <button onclick="window.location.href='//localhost/puppyCare/PuppyCare/login.html'" class="login-button">Iniciar sesión</button>
    `;
}
