const urlUpdateItem = document.querySelector(".url-update-item")?.textContent;
formItem?.addEventListener("submit", async(e) => {
    e.preventDefault();
    try {
        const res = await fetch(urlUpdateItem, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': formItem["csrfmiddlewaretoken"].value,
                'Content-Type': 'application/json',
                'mode': 'same-origin',
            },
            body: JSON.stringify({
                sl_opcion: formItem["sl_opcion"].value,
                articulo: formItem["articulo"].value,
                tamanio: formItem["tamanio"].value,
                cantidad: formItem["cantidad"].value,
                area: formItem["area"].value,
                marca: formItem["marca"].value,
                modelo: formItem["modelo"].value,
                proyecto: formItem["proyecto"].value,
                resguardo: formItem["resguardo"].value,
                noserie: formItem["noserie"].value,
                noseriei: formItem["noseriei"].value,
                cantidad: formItem["cantidad"].value,
                proveedor: formItem["proveedor"].value,
                oc: formItem["oc"].value,
                sl_opcion_oc: formItem["sl_opcion_oc"].value,
                status: formItem["status"].value,
                fsalida: formItem["fsalida"]?.value ?? "",
                fregreso: formItem["fregreso"]?.value ?? "",
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
        if(response.status == 201) {
            formContainer[0]?.classList.toggle("opened");
            window.location.reload();
        }
    } catch(e) {
        Swal.fire({
            icon: 'error',
            text: 'No se ha podido registrar el equipo',
            position: 'top-end'
        })
        return
    }
})