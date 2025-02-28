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

        document.getElementById("editar-btn").addEventListener("click", function() {
        console.log("Modo edición activado.");
        document.querySelectorAll("#user-form input").forEach(input => input.disabled = false);
        document.getElementById("editar-btn").style.display = "none";
        document.getElementById("guardar-btn").style.display = "inline";
      });
  
      document.getElementById("user-form").addEventListener("submit", function(event) {
          event.preventDefault();
          
          // Solo enviar los campos que tienen valores
          const datosActualizados = {};
          
          // Verificar si el campo tiene valor antes de incluirlo en los datos
          if (document.getElementById("nombre").value.trim()) {
              datosActualizados.nombre = document.getElementById("nombre").value.trim();
          }
          if (document.getElementById("apellido1").value.trim()) {
              datosActualizados.apellido1 = document.getElementById("apellido1").value.trim();
          }
          if (document.getElementById("apellido2").value.trim()) {
              datosActualizados.apellido2 = document.getElementById("apellido2").value.trim();
          }
          if (document.getElementById("emailuser").value.trim()) {
              datosActualizados.email = document.getElementById("emailuser").value.trim();
          }
          if (document.getElementById("calle").value.trim()) {
              datosActualizados.calle = document.getElementById("calle").value.trim();
          }
          if (document.getElementById("numero").value.trim()) {
              datosActualizados.numero = document.getElementById("numero").value.trim();
          }
          if (document.getElementById("piso").value.trim()) {
              datosActualizados.piso = document.getElementById("piso").value.trim();
          }
          if (document.getElementById("codigopostal").value.trim()) {
              datosActualizados.codigopostal = document.getElementById("codigopostal").value.trim();
          }
          if (document.getElementById("ciudad").value.trim()) {
              datosActualizados.ciudad = document.getElementById("ciudad").value.trim();
          }
  
          // Si no se ha modificado nada, no enviar nada
          if (Object.keys(datosActualizados).length === 0) {
              return;
          }
  
          console.log("Enviando datos actualizados:", datosActualizados);
  
          fetch(`http://127.0.0.1:8000/users/user/${id_usuario}`, {
              method: "PUT",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify(datosActualizados)
          })
          .then(response => {
              console.log("Respuesta de actualización recibida:", response);
              
              if (!response.ok) {
                  throw new Error(`Error al actualizar usuario: ${response.status} ${response.statusText}`);
              }
  
              return response.json();
          })
          .then(data => {
              console.log("Usuario actualizado correctamente:", data);
              document.querySelectorAll("#user-form input").forEach(input => input.disabled = true);
              document.getElementById("editar-btn").style.display = "inline";
              document.getElementById("guardar-btn").style.display = "none";
          })
          .catch(error => console.error("Error al actualizar usuario:", error));
      });
  
      cargarUsuario(id_usuario);  // Llamamos para cargar los datos del usuario
  
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