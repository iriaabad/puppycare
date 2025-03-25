// Función para obtener el cliente actual
async function obtenerCliente() {
    try {
        // Hacer la solicitud para obtener el usuario actual
        const userResponse = await fetch("http://127.0.0.1:8000/auth/users/me", {
            method: "GET",
            credentials: "include"
        });

        if (!userResponse.ok) throw new Error("Error obteniendo el usuario");

        const user = await userResponse.json();
        console.log("Usuario actual:", user);

        // Usamos el user_id para obtener el cliente
        const userId = user.id_usuario;

        // Hacer otra solicitud para obtener el cliente usando el userId
        const clienteResponse = await fetch(`http://127.0.0.1:8000/clientes/usuario/${userId}`, {
            method: "GET",
            credentials: "include"
        });

        if (!clienteResponse.ok) throw new Error("Error obteniendo el cliente");

        const cliente = await clienteResponse.json();
        console.log("Cliente encontrado:", cliente);

        return cliente.id_cliente; // Retornamos el ID del cliente directamente
    } catch (error) {
        console.error("Error al obtener el cliente:", error);
        return null; // Devolver null si hay un error
    }
}

// Función para cargar la lista de reservas y mostrarlas en tarjetas
async function loadReservas(id_cliente) {
    if (!id_cliente) {
        console.error("ID de cliente no válido");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/reservas/cliente/${id_cliente}`);
        if (!response.ok) throw new Error("Error al cargar reservas");

        const reservas = await response.json();
        const container = document.getElementById('reservas-container');
        container.innerHTML = "";

        reservas.forEach(reserva => {
            const card = document.createElement('div');
            card.className = "card";
            card.innerHTML = `
        <h3>Código de reserva: ${reserva.id_reserva}</h3>
        <p><strong>Fecha Inicio:</strong> ${reserva.fecha_inicio}</p>
        <p><strong>Fecha Fin:</strong> ${reserva.fecha_fin}</p>
        <p><strong>Cantidad de Mascotas:</strong> ${reserva.cantidad_mascotas}</p>
        <p><strong>Precio Total:</strong> ${reserva.precio_total.toFixed(2)}€</p>
        <p><strong>Cuidador:</strong> ${reserva.nombre_cuidador}</p>
        <p><strong>Estado:</strong> ${reserva.estado_reserva}</p>
            `;
            container.appendChild(card);
        });

    } catch (error) {
        console.error("Error al cargar reservas:", error);
    }
}

// Ejecutar al cargar la página
document.addEventListener("DOMContentLoaded", async () => {
    const id_cliente = await obtenerCliente();
    if (id_cliente) {
        loadReservas(id_cliente);
    }
});

