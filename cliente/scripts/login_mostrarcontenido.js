fetch("http://127.0.0.1:8000/auth/users/me", {
    method: "GET",
    credentials: "include"
})
.then(response => {
    if (response.status === 200) {
        document.getElementById('formulariologin').style.display = 'none';
        document.getElementById('areacliente').style.display = 'block';
    } else {
        document.getElementById('formulariologin').style.display = 'block';
        document.getElementById('areacliente').style.display = 'none';
    }
})
.catch(error => {
    console.error('Error al verificar la autenticación:', error);
    document.getElementById('formulariologin').style.display = 'block';
    document.getElementById('areacliente').style.display = 'none';
})
.finally(() => {
    // Una vez verificado, se hace visible el contenido del body
    document.body.style.visibility = "visible";
});
