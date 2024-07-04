const urlAddTool = document.querySelector(".url-add-tool")?.textContent;
formTools[0]?.addEventListener("submit", async(e) => {
    e.preventDefault();
    try {
        const response = await fetch(urlAddTool, {
            method: 'POST',
            headers: {
                'X-CSRFToken': formTools[0]["csrfmiddlewaretoken"].value,
                'Content-Type': 'application/json',
                'mode': 'same-origin',
            },
            body: JSON.stringify({
                // sl_opcion: form["sl_opcion"].value,
                producto: formTools[0]["herramienta"].value,
                codigo: formTools[0]["codigo"].value,
                tamanio: formTools[0]["tamanio"].value,
                cantidad: formTools[0]["cantidad"].value,
                libraje: formTools[0]["libraje"].value,
                conexion: formTools[0]["conexion"].value,
                medida: formTools[0]["medida"].value,
                noserie: formTools[0]["noserie"].value,
                noseriei: formTools[0]["noseriei"].value,
                categoria: formTools[0]["categoria"].value,
                proveedor: formTools[0]["proveedor"].value,
                oc: formTools[0]["oc"].value,
                sl_opcion_oc: formTools[0]["sl_opcion_oc"].value,
                status: formTools[0]["status"].value,
                // fsalida: formTools[0]["fsalida"].value,
                // fregreso: formTools[0]["fregreso"].value,
                pozo: formTools[0]["pozo"].value,
                observaciones: formTools[0]["observaciones"].value
            })
        });
        if(response.status != 201) throw new Error(response.statusText);
        const data = await response.json();
        await Swal.fire({
            title: data.status == 201 ? 'Éxito!' : null,
            icon: data.status == 201 ? 'success' : "warning",
            text: data.message,
            position: 'center'
        })
        if(data.status == 201) {
            formContainer[0]?.classList.toggle("opened");
            window.location.reload();
        }
    } catch (error) {
        console.log(error)
        Swal.fire({
            icon: 'error',
            text: 'Ha ocurrido un error',
            position: 'center'
        })
    }
})

document.querySelectorAll(".form-delete-tool").forEach(form => {
    form.addEventListener("submit", e => {
        e.preventDefault();
        const url = e.target?.deleteProduct?.getAttribute("id");
        const token = e.target?.csrfmiddlewaretoken?.value;
        Swal.fire({
            title: "Está seguro de continuar?",
            text: "El producto será eliminado y no podrá usarse.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Si, eliminar producto",
            cancelButtonText: "Descartar",
        }).then(async (result) => {
            if(result.isConfirmed) {
                await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': token,
                        'Content-Type': 'application/json',
                        'mode': 'same-origin',
                    }
                }).then(response => response.json())
                .then(async(data) => {
                    await Swal.fire({
                        title: data.status == 204 ? 'Éxito!' : null,
                        icon: data.status == 204 ? 'success' : "warning",
                        text: data.message,
                        position: 'center'
                    })
                    if(data.status == 204) {
                        window.location.reload();
                    }
                }).catch(error => {
                    console.log(error)
                    Swal.fire({
                        icon: 'error',
                        text: 'Ha ocurrido un error',
                        position: 'center'
                    })
                })
            }
        })
    })
})

const formProduct = document.querySelector(".form-product");
const quantityText = document.querySelector("#quantity")
const url = document.querySelector("#url")

document.querySelectorAll(".btnProduct").forEach(btn => {
    btn.addEventListener('click', (e) => {
        const quantity = e.target.parentElement?.getAttribute("quantity").split(" ");
        const urlText = e.target.parentElement?.getAttribute("url");
        document.querySelector("#productName").textContent = e.target.parentElement.parentElement.parentElement.parentElement.querySelectorAll("td")[1].textContent;
        formProduct["productid"].value = quantity[1];
        quantityText.textContent = Number(quantity[0]);
        url.textContent = urlText;
        formProduct["quantity"].value = Number(quantity[0]);
        formContainer[2].classList.toggle("opened")
    })
})

formProduct?.addEventListener("submit", (e) => {
    e.preventDefault();
    if(e.target.quantity.value > Number(quantityText.textContent)) {
        return Swal.fire({
            title: "La cantidad elegida es mayor a la disponible.",
            icon: "warning",
            position: 'center'
        })
    }
    if(e.target.quantity.value == 0) {
        return Swal.fire({
            title: "La cantidad debe ser mayor a cero.",
            icon: "warning",
            position: 'center'
        })
    }
    fetch(url.textContent, {
        method: 'POST',
        mode: "same-origin",
        headers: {
            'X-CSRFToken': e.target.csrfmiddlewaretoken.value,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cantidad: e.target.quantity?.value,
            condiciones: e.target.condition?.value,
            estado: e.target.sl_status?.value,
        })
    })
    .then(res => res.json())
    .then(async(data) => {
        await Swal.fire({
            title: data.status == 201 ? 'Éxito!' : null,
            icon: data.status == 201 ? 'success' : "warning",
            text: data.message,
            position: 'center'
        })
        if(data.status == 201) {
            formContainer[2]?.classList.toggle("opened");
            window.location.reload();
        }
    })
    .catch(error => {
        console.log(error)
        Swal.fire({
            icon: 'error',
            text: 'Ha ocurrido un error',
            position: 'center'
        })
    })
})