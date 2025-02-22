// script que trael el header a la página
fetch('header.html')
  .then(response => {
    if (!response.ok) {
      throw new Error('Error al cargar la cabecera');
    }
    return response.text();
  })
  .then(data => {
    document.getElementById('header-placeholder').innerHTML = data;
    const script = document.createElement('script');
    script.src = 'scripts/userdisplaymenu.js';
    document.body.appendChild(script);
  })
  
  .catch(error => console.error('Error:', error));


  // script que trael el footer a la página
fetch('footer.html')
.then(response => {
  if (!response.ok) {
    throw new Error('Error al cargar el footer');
  }
  return response.text();
})
.then(data => {
  document.getElementById('footer-placeholder').innerHTML = data;
})
.catch(error => console.error('Error:', error));

 