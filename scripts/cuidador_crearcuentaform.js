document.addEventListener("DOMContentLoaded", async function () {
    // Función para obtener datos del usuario autenticado.
    async function getAuthenticatedUser() {
        try {
            const response = await fetch("http://127.0.0.1:8000/auth/users/me", {
                method: "GET",
                credentials: "include"
            });

            if (!response.ok) return null; // Si no está autenticado, devuelve null

            const userData = await response.json();
            return userData; // Devuelve los datos completos del usuario
        } catch (error) {
            console.error("Error de autenticación:", error);
            return null;
        }
    }
    // Función para verificar si el usuario ya existe en la tabla de cuidadores, se salta a la página de areacuidador
  async function checkIfCuidadorExists(userId) {
    try {
      const response = await fetch(`http://127.0.0.1:8000/cuidadores/select/?usuario_id_usuario=${userId}`, {
        method: "GET",
        credentials: "include"
      });
      if (!response.ok) return false;
      const data = await response.json();
      // Se asume que el endpoint retorna un array; si existe al menos un registro, el usuario ya es cuidador.
      return Array.isArray(data) && data.length > 0;
    } catch (error) {
      console.error("Error al verificar cuidador:", error);
      return false;
    }
  }

    // Esperamos el resultado de la autenticación.
    const user = await getAuthenticatedUser();
    const isLoggedIn = user !== null;
    const id_usuario = isLoggedIn ? user.id_usuario : null;

  // Si el usuario está logado, verificamos si ya es cuidador y redirigimos si es así.
  if (isLoggedIn) {
    const isCuidador = await checkIfCuidadorExists(id_usuario);
    if (isCuidador) {
      window.location.href = "//localhost/puppyCare/PuppyCare/cuidador/areacuidador.html";
      return; // Salir del flujo para que no se ejecute el resto del código
    }
  }

    // Seleccionar secciones del formulario de registro
    const parte1 = document.getElementById("formulariocrearcuenta-placeholder");
    const parte2 = document.getElementById("formulariocrearcuentacuidador2");
    const parte3 = document.getElementById("formulariocrearcuentacuidador3");
  
    // Mostrar u ocultar las partes del formulario según si el usuario está logado
    if (isLoggedIn) {
      parte1.style.display = "none";
      parte2.style.display = "block";
      parte3.style.display = "none";
    } else {
      parte1.style.display = "block";
      parte2.style.display = "none";
      parte3.style.display = "none";
    }
  
    // Transición de la Parte 1 a la Parte 2 (Crear cuenta)
    parte1.addEventListener("submit", async function(e) {
      e.preventDefault();
      // Usar e.target para referirse al formulario actual
      const formData = new FormData(e.target);
      const data = {
        email: formData.get('email'),
        nombre: formData.get('nombre'),
        apellido1: formData.get('apellido1'),
        apellido2: formData.get('apellido2'),
        password: formData.get('password')
      };
  
      try {
        const response = await fetch('http://127.0.0.1:8000/users/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });
  
        if (response.ok) {
          console.log(await response.json());
        } else {
          const errorData = await response.json();
          alert(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        alert("Hubo un problema con la solicitud. Por favor, contacta con atención al cliente");
        console.error(error);
      }
      // Mostrar una vez creada la cuenta muestra el formulario de login
      parte1.style.display = "none";
      parte2.style.display = "none";
      document.getElementById("formulariologin").style.display = "block";
    });
  
    // Transición de la Parte 2 a la Parte 3 (Datos de dirección)
    parte2.addEventListener("submit", function(e) {
      e.preventDefault();
      parte2.style.display = "none";
      parte3.style.display = "block";
    });

    // Envío final del formulario (Parte 3: Datos adicionales)
    parte3.addEventListener("submit", async function(e) {
      e.preventDefault();
      // Usar e.target para referirse al formulario actual
      const formData = new FormData(e.target);
      const data = {
        tarifa_dia: formData.get('tarifa_dia'),
        capacidad_mascota: formData.get('capacidad_mascota'),
        descripcion: formData.get('descripcion'),
        usuario_id_usuario: id_usuario, // Pasar el ID del usuario al cuidador
        disponibilidad_activa: formData.get('disponibilidad_activa')
      };
  
      try {
        const response = await fetch('http://127.0.0.1:8000/cuidadores/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });
  
        if (response.ok) {
          console.log(await response.json());
        } else {
          const errorData = await response.json();
          alert(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        alert("Hubo un problema con la solicitud. Por favor, contacta con atención al cliente");
        console.error(error);
      }
      window.location.reload()
    });
  
    // Mostrar formulario de login cuando el usuario haga clic en "¿Ya tienes cuenta? Inicia sesión para continuar el registro"
    const enlaceLogin = document.getElementById("ofertalogin");
    if (enlaceLogin) {
      enlaceLogin.addEventListener("click", function(e) {
        e.preventDefault();
        document.getElementById("formulariologin").style.display = "block";
        // Ocultar las secciones de registro
        parte1.style.display = "none";
        parte2.style.display = "none";
        parte3.style.display = "none";

      });
    }
  });
  