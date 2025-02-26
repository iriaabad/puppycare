document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("formulariocrearcuenta");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();  // Evitar el envío normal del formulario

        const formData = new FormData(form);
        const data = {
            email: formData.get('email'),
            nombre: formData.get('nombre'),
            apellido1: formData.get('apellido1'),
            apellido2: formData.get('apellido2'),
            password: formData.get('password')
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/users/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: data.email,
                    nombre: data.nombre,
                    apellido1: data.apellido1,
                    apellido2: data.apellido2,
                    password: data.password
                }),
            });

            if (response.ok) {
                alert("Usuario creado con éxito");
                console.log(await response.json());
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            alert("Hubo un problema con la solicitud. Por favor, contacta con atención al cliente");
            console.error(error);
        }
    });
});
