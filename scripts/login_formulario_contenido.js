document.addEventListener("DOMContentLoaded", function () {
// Primero, mostramos la pantalla de carga mientras se realiza la verificación
document.getElementById('loading-screen').style.display = 'block';

fetch('//localhost/puppyCare/PuppyCare/partials/formulariologin.html')
.then(response => {
  if (!response.ok) {
    throw new Error('Error al cargar el formulario');
  }
  return response.text();
})
.then(data => {
  // Cargamos el formulario en el div
  document.getElementById('formulariologin').innerHTML = data;

  // Luego, verificamos la autenticación
  return fetch("http://127.0.0.1:8000/auth/users/me", {
    method: "GET",
    credentials: "include"
  });
})
.then(response => {
  // Ocultamos la pantalla de carga
  document.getElementById('loading-screen').style.display = 'none';

  if (response.status === 200) {
    document.getElementById('formulariologin').style.display = 'none';
    document.getElementById('areaprivada').style.display = 'block';
  } else {
    document.getElementById('formulariologin').style.display = 'block';
    document.getElementById('areaprivada').style.display = 'none';
  }
})
.catch(error => {
  // Ocultamos la pantalla de carga en caso de error
  document.getElementById('loading-screen').style.display = 'none';

  console.error('Error:', error);
  document.getElementById('formulariologin').style.display = 'block';
  document.getElementById('areaprivada').style.display = 'none';
})
.finally(() => {
  // Una vez verificado, hacemos visible el contenido del body
  document.body.style.visibility = "visible";
});
});
