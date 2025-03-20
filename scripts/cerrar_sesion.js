
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(() => {
        const logoutBtn = document.getElementById("logout-btn");
        console.log("logoutBtn", logoutBtn);
        if (logoutBtn) {
            logoutBtn.addEventListener("click", logout);
        } else {
            console.error("No se encontró el botón de cerrar sesión");
        }
    }, 1000);

    async function logout() {
        try {
            const response = await fetch("http://127.0.0.1:8000/auth/logout", {
                method: "POST",
                credentials: "include"  // Para incluir la cookie de sesión
            });
            if (response.ok) {
                // Limpia los datos de sesión en el cliente, si es necesario
                localStorage.removeItem("access_token");
                window.location.href = "//localhost/puppyCare/PuppyCare/index.html";
            } else {
                console.error("Error al cerrar la sesión.");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }
    
    // Asocia la función al botón de "Cerrar Sesión"
    document.getElementById("logout-btn").addEventListener("click", logout);
});