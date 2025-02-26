document.addEventListener("DOMContentLoaded", function() {
    const formContainer = document.getElementById("formulariologin"); // Donde se inyecta el formulario

    formContainer.addEventListener('submit', async (event) => {
        event.preventDefault();  // Evitar el envío normal del formulario

        const form = event.target;  // Usar el formulario que se ha enviado

        const formData = new FormData(form);

        // Convertir los datos del FormData a un string codificado en URL
        const data = new URLSearchParams();
        data.append("username", formData.get('email'));  
        data.append("password", formData.get('password'));

        try {
            const response = await fetch('http://127.0.0.1:8000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'  // Especificamos el tipo adecuado
                },
                body: data.toString(),  // Los datos en formato URL codificado
                credentials: "include"// Incluye las cookies en la solicitud
            });

            if (response.ok) {
                alert("Usuario autenticado");
                window.location.href = "//localhost/puppyCare/PuppyCare/cliente/areacliente.html";
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            alert("No se ha podido autenticar al usuario");
            console.error(error);
        }
    });
});
