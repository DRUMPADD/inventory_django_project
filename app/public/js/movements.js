const urlMovement = document.querySelector(".url-update-movement")?.textContent;
const formMovement = document.querySelector(".form-movement");


formMovement.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const response = await fetch(urlMovement, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': formMovement["csrfmiddlewaretoken"].value,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_product: formMovement["sl_product"].value,
                fsalida: formMovement["fsalida"]?.value ?? "",
                fregreso: formMovement["fregreso"]?.value ?? ""
            })
        })

        if(response.status != 201) throw Error(response.statusText);
        const data = await response.json();
        await Swal.fire({
            title: response.status == 201 ? 'Éxito!' : null,
            icon: response.status == 201 ? 'success' : "warning",
            text: data.message,
            position: response.status == 201 ? 'center' : 'top-end'
        })

        window.location.reload();
    } catch (error) {
        Swal.fire({
            icon: 'error',
            text: 'Ha ocurrido un error',
            position: 'top-end'
        })
    }
})