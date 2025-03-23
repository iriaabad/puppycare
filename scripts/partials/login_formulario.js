// script que trae el formulario login a la página
fetch('//localhost/puppyCare/PuppyCare/partials/formulariologin.html')
.then(response => {
  if (!response.ok) {
    throw new Error('Error al cargar el formulario');
  }
  return response.text();
})
.then(data => {
  // Carga el formulario en el div
  document.getElementById('formulariologin').innerHTML = data;
  
})
.catch(error => console.error('Error:', error));
