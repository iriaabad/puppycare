// script que trael el header a la página
fetch('//localhost/puppyCare/PuppyCare/partials/header.html')
  .then(response => {
    if (!response.ok) {
      throw new Error('Error al cargar la cabecera');
    }
    return response.text();
  })
  .then(data => {
    document.getElementById('header-placeholder').innerHTML = data;
    const script = document.createElement('script');
    script.src = '//localhost/puppyCare/PuppyCare/scripts/userdisplaymenu.js';
    document.body.appendChild(script);
  })
  
  .catch(error => console.error('Error:', error));




 
 