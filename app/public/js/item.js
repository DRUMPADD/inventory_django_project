const urlUpdateItem = document.querySelector(".url-update-item")?.textContent;
formItem?.addEventListener("submit", async(e) => {
    e.preventDefault();
    formContainer[0]?.classList.toggle("opened")
    try {
        const res = await fetch(urlUpdateItem, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': formItem["csrfmiddlewaretoken"].value,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                articulo: formItem["articulo"].value,
                codigo: formItem["codigo"].value,
                area: formItem["area"].value,
                cantidad: formItem["cantidad"].value,
                marca: formItem["marca"].value,
                modelo: formItem["modelo"].value,
                proyecto: formItem["proyecto"].value,
                proveedor: formItem["proveedor"].value,
                oc: formItem["oc"].value,
                noseriei: formItem["noseriei"].value,
                noserie: formItem["noserie"].value,
                resguardo: formItem["resguardo"].value,
                sl_opcion_oc: formItem["sl_opcion_oc"].value,
                status: formItem["status"].value,
            })
        })

        if(res.status != 201) {
            throw Error(res.statusText)
        }
        const data = await res.json();
        await Swal.fire({
            title: res.status == 201 ? 'Éxito!' : "Oh, no!",
            icon: res.status == 201 ? 'success' : "warning",
            text: data.message,
            position: res.status == 201 ? 'center' : 'top-end'
        })
        window.location.reload()
    } catch(e) {
        Swal.fire({
            icon: 'error',
            text: 'No se ha podido registrar el equipo',
            position: 'top-end'
        })
        return
    }
})