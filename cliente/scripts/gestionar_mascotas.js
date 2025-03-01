// Mostrar/ocultar el formulario al pulsar el botón
document.getElementById("toggle-form").addEventListener("click", () => {
    const form = document.getElementById("mascota-form");
    form.style.display = (form.style.display === "none" || form.style.display === "") ? "block" : "none";
  });

  // Función para poblar un select con datos obtenidos de un endpoint
  async function fetchSelectOptions(url, selectElement, idField, nameField) {
    try {
      const response = await fetch(url);
      const data = await response.json();
      data.forEach(item => {
        const option = document.createElement('option');
        option.value = item[idField];
        option.textContent = item[nameField];
        selectElement.appendChild(option);
      });
    } catch (error) {
      console.error("Error fetching options:", error);
    }
  }

  // Función para cargar la lista de mascotas y mostrarlas en tarjetas
  async function loadMascotas() {
    try {
      const response = await fetch("http://127.0.0.1:8000/mascotas/");
      const mascotas = await response.json();
      const container = document.getElementById('mascotas-container');
      container.innerHTML = "";
      mascotas.forEach(mascota => {
        const card = document.createElement('div');
        card.className = "card";
        card.innerHTML = `
        <h3>${mascota.nombre}</h3>
        <p><strong>Tipo:</strong> ${mascota.tipo_mascota ? mascota.tipo_mascota.tipo : mascota.tipo_mascota_id_tipo_mascota}</p>
        <p><strong>Edad:</strong> ${mascota.edad || ''}</p>
        <p><strong>Tamaño:</strong> ${mascota.tamano ? mascota.tamano.descripcion : mascota.tamano_id_tamano}</p>
        <p><strong>Necesidades:</strong> ${mascota.necesidades_especiales || ''}</p>
      `;
        container.appendChild(card);
        
      });
      
    } catch (error) {
      console.error("Error loading mascotas:", error);
    }
  }

  // Manejo del envío del formulario
  document.getElementById('mascota-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
      nombre: formData.get('nombre'),
      edad: formData.get('edad') ? parseInt(formData.get('edad')) : null,
      tipo_mascota_id_tipo_mascota: parseInt(formData.get('tipo_mascota_id_tipo_mascota') || formData.get('tipo')),
      tamano_id_tamano: formData.get('tamano_id_tamano') ? parseInt(formData.get('tamano_id_tamano')) : null,
      necesidades_especiales: formData.get('necesidades_especiales'),
      cliente_id_cliente: formData.get('cliente_id_cliente') ? parseInt(formData.get('cliente_id_cliente')) : null,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/mascotas/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      if (!response.ok) throw new Error("Error al crear mascota");
      alert("Mascota creada correctamente");
      event.target.reset();
      loadMascotas();
    } catch (error) {
      console.error("Error:", error);
      alert("Error al crear mascota");
    }
  });

  // Al cargar la página, poblar los selects y cargar la lista de mascotas
  window.addEventListener('load', () => {
    const tipoSelect = document.getElementById("tipo");
    fetchSelectOptions("http://127.0.0.1:8000/tipos-mascota/", tipoSelect, "id_tipo_mascota", "tipo");

    const tamanoSelect = document.getElementById("tamano");
    fetchSelectOptions("http://127.0.0.1:8000/tamanos/", tamanoSelect, "id_tamano", "descripcion");

    loadMascotas();
  });