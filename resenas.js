
// trae el contenido de resenas
fetch('resenas.html')
  .then(response => {
    if (!response.ok) {
      throw new Error('Error al cargar las reseñas');
    }
    return response.text();
  })
  .then(data => {
    // Inserta el HTML de reseñas en el contenedor
    document.getElementById('resenas-placeholder').innerHTML = data;
    // Una vez insertado, inicializa el carrusel
     
    // Selecciona el carrusel y las tarjetas después de insertar el HTML
    const carousel = document.querySelector('.carousel-resena');
    const cards = document.querySelectorAll('.cardResena');
    const totalCards = cards.length;
    let index = 0;
    
    function moveCarousel() {
      index++;
      if (index >= totalCards) {
        index = 0; // Reinicia al inicio cuando llega al final
      }
      if (carousel) {
        carousel.style.transform = `translateX(-${index * 100}%)`;
      } else {
        console.error('El elemento carousel no se encontró en el DOM');
      }
    }
    
    // Verifica que el carrusel y las tarjetas existan antes de iniciar el intervalo
    if (carousel && totalCards > 0) {
      setInterval(moveCarousel, 6000); // Cambia cada 6 segundos
    } else {
      console.error('El carrusel o las tarjetas no se encontraron en el DOM');
    }
  })
  .catch(error => console.error('Error:', error));