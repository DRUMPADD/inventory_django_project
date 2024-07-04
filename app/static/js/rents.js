document.querySelectorAll(".form-rent-product").forEach(form => {
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const url = e.target.returnRent.getAttribute("id");
        const middleware = e.target.csrfmiddlewaretoken.value;
        Swal.fire({
            title: "Está seguro de continuar?",
            text: "Una vez devuelto el producto no se podrá editar este registro.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#35d630",
            cancelButtonColor: "#b72525",
            confirmButtonText: "Regresar producto.",
            cancelButtonText: "Cancelar",
        }).then(async(result) => {
            if(result.isConfirmed) {
                console.log(url)
                console.log(middleware)
                await fetch(url, {
                    method: 'PUT',
                    mode: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': middleware
                    },
                    body: JSON.stringify({
                        id: url.split("/")[1]
                    })
                }).then(response => response.json())
                .then(async (data) => {
                    await Swal.fire({
                        title: data.status == 200 ? "Éxito" : "Oh, no!",
                        icon: data.status == 200 ? 'success' : "warning",
                        text: data.status == 200 ? data.message : "Oh, no!",
                        position: "center",
                    })
                    if(data.status == 200) {
                        window.location.reload();
                    }
                }).catch(error => {
                    console.log(error)
                    Swal.fire({
                        icon: 'error',
                        text: 'No se puede actualizar el status del producto',
                        position: 'center'
                    })
                })
            }
        })
    })
})
document.querySelectorAll(".form-cancel-product").forEach(form => {
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const url = e.target.cancelRent.getAttribute("id");
        const middleware = e.target.csrfmiddlewaretoken.value;
        Swal.fire({
            title: "Está seguro de continuar?",
            text: "Una vez cancelado el producto no se podrá editar este registro.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#35d630",
            cancelButtonColor: "#b72525",
            confirmButtonText: "Cancelar producto.",
            cancelButtonText: "Descartar",
        }).then(async(result) => {
            if(result.isConfirmed) {
                await fetch(url, {
                    method: 'PUT',
                    mode: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': middleware
                    },
                    body: JSON.stringify({
                        id: url.split("/")[1]
                    })
                }).then(response => response.json())
                .then(async (data) => {
                    await Swal.fire({
                        title: data.status == 200 ? "Éxito" : "Oh, no!",
                        icon: data.status == 200 ? 'success' : "warning",
                        text: data.status == 200 ? data.message : "Oh, no!",
                        position: "center",
                    })
                    if(data.status == 200) {
                        window.location.reload();
                    }
                }).catch(error => {
                    console.log(error)
                    Swal.fire({
                        icon: 'error',
                        text: 'No se puede actualizar el status del producto',
                        position: 'center'
                    })
                })
            }
        })
    })
})