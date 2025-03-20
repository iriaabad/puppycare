document.addEventListener("DOMContentLoaded", function() {
    // Verificar si los elementos existen en el DOM
    const header = document.getElementById("header-placeholder");
    const footer = document.getElementById("footer-placeholder");
    const resenas = document.getElementById("footer-placeholder");


    // Cargar scripts en función de los elementos encontrados
    if (header) {
        cargarScript("/puppyCare/PuppyCare/scripts/headerdisplay.js");
        cargarScript("/puppyCare/PuppyCare/scripts/cerrar_sesion.js");
        cargarScript("/puppyCare/PuppyCare/scripts/userprofile.js");
    }

    if (footer) {
        cargarScript("/puppyCare/PuppyCare/scripts/footerdisplay.js");
    }

    if (resenas) {
        cargarScript("/puppyCare/PuppyCare/scripts/resenas.js");
    }
});

// Función para cargar scripts dinámicamente
function cargarScript(src) {
    const script = document.createElement('script');
    script.src = src;
    script.type = 'text/javascript';
    script.async = true;  // Opcional: para cargar de manera asincrónica
    document.head.appendChild(script);  // Puedes también usar document.body.appendChild(script);
}
