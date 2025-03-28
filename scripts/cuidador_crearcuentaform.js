document.addEventListener("DOMContentLoaded", function () {

  function getAuthenticatedUser() {
      return fetch("http://127.0.0.1:8000/auth/users/me", {
          method: "GET",
          credentials: "include"
      })
      .then(response => response.ok ? response.json() : null)
      .catch(error => {
          console.error("Error de autenticación:", error);
          return null;
      });
  }

  function checkIfCuidadorExists(userId) {
      return fetch(`http://127.0.0.1:8000/cuidadores/select/?usuario_id_usuario=${userId}`, {
          method: "GET",
          credentials: "include"
      })
      .then(response => response.ok ? response.json() : [])
      .then(data => Array.isArray(data) && data.length > 0)
      .catch(error => {
          console.error("Error al verificar cuidador:", error);
          return false;
      });
  }

  getAuthenticatedUser().then(user => {
      const isLoggedIn = user !== null;
      const id_usuario = isLoggedIn ? user.id_usuario : null;

      if (isLoggedIn) {
          return checkIfCuidadorExists(id_usuario).then(isCuidador => {
              if (isCuidador) {
                  window.location.href = "//localhost/puppyCare/PuppyCare/cuidador/areacuidador.html";
                  return Promise.reject("Redirigiendo");
              }
              return { isLoggedIn, id_usuario };
          });
      }
      return { isLoggedIn, id_usuario };
  })
  .then(({ isLoggedIn, id_usuario }) => {
      const parte1 = document.getElementById("formulariocrearcuenta");
      const parte3 = document.getElementById("formulariocrearcuentacuidador3");

      // Mostrar u ocultar formularios según el estado de autenticación
      if (isLoggedIn) {
          parte1.style.display = "none";
          document.getElementById("formulariologin").style.display = "none";
          parte3.style.display = "block";
      } else {
          parte1.style.display = "block";
          parte3.style.display = "none";
      }

      // Evento para el formulario de creación de usuario (parte1)
      parte1.addEventListener("submit", function(e) {
          e.preventDefault();
          const formData = new FormData(e.target);
          const data = Object.fromEntries(formData.entries());
          fetch('http://127.0.0.1:8000/users/create', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(data)
          })
          .then(response => response.json())
          .then(result => {
              console.log(result);
              document.getElementById("formulariologin").style.display = "block";
              parte1.style.display = "none";
          })
          .catch(error => alert("Hubo un problema con la solicitud"));
      });

      // Evento para el formulario de creación de cuidador (parte3)
      parte3.addEventListener("submit", function(e) {
          e.preventDefault();
          const formData = new FormData(e.target);
          const data = Object.fromEntries(formData.entries());
          data.usuario_id_usuario = id_usuario;
          fetch('http://127.0.0.1:8000/cuidadores/', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(data)
          })
          .then(response => response.json())
          .then(result => {
              console.log(result);
              window.location.reload();
          })
          .catch(error => alert("Hubo un problema con la solicitud"));
      });

      // Enlace para mostrar el formulario de login
      const enlaceLogin = document.getElementById("ofertalogin");
      if (enlaceLogin) {
          enlaceLogin.addEventListener("click", function(e) {
              e.preventDefault();
              document.getElementById("formulariologin").style.display = "block";
              parte1.style.display = "none";
              parte3.style.display = "none";
          });
      }
  }).catch(err => console.log(err));
});

function cargarScript(src) {
  return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = src;
      script.onload = resolve;
      script.onerror = () => {
          console.error(`Error cargando el script: ${src}`);
          reject();
      };
      document.body.appendChild(script);
  });
}
