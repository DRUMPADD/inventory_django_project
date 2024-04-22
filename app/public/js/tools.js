const urlAddTool = document.querySelector(".url-add-tool")?.textContent;
form?.addEventListener("submit", async(e) => {
    e.preventDefault();
    formContainer[0]?.classList.toggle("opened");
    try {
        const response = await fetch(urlAddTool, {
            method: 'POST',
            headers: {
                'X-CSRFToken': form["csrfmiddlewaretoken"].value,
                'Content-Type': 'application/json',
                'mode': 'same-origin',
            },
            body: JSON.stringify({
                sl_opcion: form["sl_opcion"].value,
                herramienta: form["herramienta"].value,
                codigo: form["codigo"].value,
                tamanio: form["tamanio"].value,
                cantidad: form["cantidad"].value,
                libraje: form["libraje"].value,
                conexion: form["conexion"].value,
                medida: form["medida"].value,
                noserie: form["noserie"].value,
                noseriei: form["noseriei"].value,
                proveedor: form["proveedor"].value,
                oc: form["oc"].value,
                sl_opcion_oc: form["sl_opcion_oc"].value,
                status: form["status"].value,
                fsalida: form["fsalida"].value,
                fregreso: form["fregreso"].value,
                pozo: form["pozo"].value,
                observaciones: form["observaciones"].value
            })
        });
        if(response.status != 201) throw new Error(response.statusText);
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