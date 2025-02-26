// script que trael el header a la página
fetch('partials/menucliente.html')
  .then(response => {
    if (!response.ok) {
      throw new Error('Error al cargar la cabecera');
    }
    return response.text();
  })
  .then(data => {
    document.getElementById('menucliente-placeholder').innerHTML = data;
    const script = document.createElement('script');
   // script.src = 'scripts/userdisplaymenu.js';
    document.body.appendChild(script); //sustituir
  })
  
  .catch(error => console.error('Error:', error));