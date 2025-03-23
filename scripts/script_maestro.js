document.addEventListener("DOMContentLoaded", function () {
    // Verificar si los elementos existen en el DOM
    const header = document.getElementById("header-placeholder");
    const footer = document.getElementById("footer-placeholder");
    const resenas = document.getElementById("footer-placeholder");
    const formcrearcuenta = document.getElementById("formulariocrearcuenta-placeholder");
    const loginform = document.getElementById("formulariologin");



    // Cargar scripts en función de los elementos encontrados
    if (header) {
        cargarScript("//localhost/puppyCare/PuppyCare/scripts/partials/header.js");
        cargarScript("//localhost/puppyCare/PuppyCare/scripts/cerrar_sesion.js");
        cargarScript("//localhost/puppyCare/PuppyCare/scripts/userprofile.js");
    }

    if (footer) {
        cargarScript("//localhost/puppyCare/PuppyCare/scripts/partials/footer.js");
    }

    if (resenas) {
        cargarScript("//localhost/puppyCare/PuppyCare/scripts/partials/resenas.js");
    }else{
        console.warn("El elemento #resenas no existe en esta página.");
    }        
    if (loginform) {
        cargarScript("//localhost/puppyCare/PuppyCare/scripts/partials/login_formulario.js");
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




