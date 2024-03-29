const urlAddItem = document.querySelector(".url-add-item")?.textContent;

formItem?.addEventListener("submit", async(e) => {
    e.preventDefault();
    formContainer[0]?.classList.toggle("opened");
    try {
        const response = await fetch(urlAddItem, {
            method: 'POST',
            headers: {
                'X-CSRFToken': formItem["csrfmiddlewaretoken"].value,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sl_opcion: formItem["sl_opcion"].value,
                articulo: formItem["articulo"].value,
                codigo: formItem["codigo"].value,
                cantidad: formItem["cantidad"].value,
                area: formItem["area"].value,
                marca: formItem["marca"].value,
                modelo: formItem["modelo"].value,
                proyecto: formItem["proyecto"].value,
                resguardo: formItem["resguardo"].value,
                noseriei: formItem["noseriei"].value,
                cantidad: formItem["cantidad"].value,
                proveedor: formItem["proveedor"].value,
                oc: formItem["oc"].value,
                sl_opcion_oc: formItem["sl_opcion_oc"].value,
                status: formItem["status"].value,
                fsalida: formItem["fsalida"]?.value ?? "",
                fregreso: formItem["fregreso"]?.value ?? "",
            })
        });
        if(response.status != 201) throw new Error(response.statusText);
        const data = await response.json();
        console.log(data.message)
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
