// script que trael el footer a la página
fetch('//localhost/puppyCare/PuppyCare/partials/footer.html')
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