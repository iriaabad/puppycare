// script que trael el formulario de crear cuenta a la página
fetch('//localhost/puppyCare/PuppyCare/partials/formulariocrearcuenta.html')
.then(response => {
  if (!response.ok) {
    throw new Error('Error al cargar el formulario');
  }
  return response.text();
})
.then(data => {
  document.getElementById('formulariocrearcuenta-placeholder').innerHTML = data;
})
.catch(error => console.error('Error:', error));