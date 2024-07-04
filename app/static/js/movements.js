const urlMovement = document.querySelector(".url-update-movement")?.textContent;
const formMovement = document.querySelector(".form-movement");


formMovement.addEventListener("submit", async (e) => {
    e.preventDefault();
    Swal.fire({
        title: "Está seguro de continuar?",
        text: "El producto será actualizado.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Actualizar",
        cancelButtonText: "Cancelar",
    }).then(async(result) => {
        if(result.isConfirmed) {
            try {
                const response = await fetch(urlMovement, {
                    method: 'PUT',
                    headers: {
                        'X-CSRFToken': formMovement["csrfmiddlewaretoken"].value,
                        'Content-Type': 'application/json',
                        'mode': 'same-origin',
                    },
                    body: JSON.stringify({
                        cantidad: formMovement["cantidad"].value,
                        id_product: formMovement["id_product"].value,
                        fsalida: formMovement["fsalida"]?.value ?? "",
                        fregreso: formMovement["fregreso"]?.value ?? ""
                    })
                })
                const data = await response.json();
                await Swal.fire({
                    title: data.status == 201 ? 'Éxito!' : null,
                    icon: data.status == 201 ? 'success' : "warning",
                    text: data.message,
                    position: 'center'
                })
        
                if(response.status == 201) {
                    window.location.reload();
                }
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    text: 'Ha ocurrido un error',
                    position: 'center'
                })
            }
        }
    })
})