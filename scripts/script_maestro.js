document.addEventListener("DOMContentLoaded", function () {
    // Verificar si los elementos existen en el DOM
    const header = document.getElementById("header-placeholder");
    const footer = document.getElementById("footer-placeholder");
    const resenas = document.getElementById("footer-placeholder");
    const formcrearcuenta = document.getElementById("formulariocrearcuenta-placeholder");


    // Cargar scripts en función de los elementos encontrados
    if (header) {
        cargarScript("/puppyCare/PuppyCare/scripts/partials/header.js");
        cargarScript("/puppyCare/PuppyCare/scripts/cerrar_sesion.js");
        cargarScript("/puppyCare/PuppyCare/scripts/userprofile.js");
    }

    if (footer) {
        cargarScript("/puppyCare/PuppyCare/scripts/partials/footer.js");
    }

    if (resenas) {
        cargarScript("/puppyCare/PuppyCare/scripts/partials/resenas.js");
    }

    if (formcrearcuenta) {
        cargarScript("/puppyCare/PuppyCare/scripts/partials/crearcuentaform.js");
        document.addEventListener("submit", async function (event) {
            event.preventDefault();  // Prevent the default form submission

            async function manejoCrearCuenta(form) {
                event.preventDefault();  // Prevent the default form submission

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
                        body: JSON.stringify(data),
                    });

                    if (response.ok) {
                        alert("Usuario creado con éxito");
                        console.log(await response.json());
                        window.location.reload();
                    } else {
                        const errorData = await response.json();
                        alert(`Error: ${errorData.detail}`);
                    }
                } catch (error) {
                    alert("Hubo un problema con la solicitud. Por favor, contacta con atención al cliente");
                    console.error(error);
                }
            }

            const form = event.target; // Get the form element
            manejoCrearCuenta(form); // Call the function with the form
        });
    }             

                // Función para esperar hasta que el elemento esté en el DOM
                function esperarElemento(selector) {
                    return new Promise((resolve) => {
                        if (document.querySelector(selector)) {
                            return resolve(document.querySelector(selector));
                        }

                        const observer = new MutationObserver((mutations, obs) => {
                            if (document.querySelector(selector)) {
                                obs.disconnect();
                                resolve(document.querySelector(selector));
                            }
                        });

                        observer.observe(document.body, {
                            childList: true,
                            subtree: true
                        });
                    });
                }

             

                // Función para cargar un script dinámicamente
                function cargarScript(src) {
                    return new Promise((resolve, reject) => {
                        const script = document.createElement("script");
                        script.src = src;
                        script.onload = () => {
                            console.log(`Script cargado: ${src}`);
                            resolve();
                        };
                        script.onerror = () => {
                            console.error(`Error cargando el script: ${src}`);
                            reject();
                        };
                        document.body.appendChild(script);
                    });
                }

            });




