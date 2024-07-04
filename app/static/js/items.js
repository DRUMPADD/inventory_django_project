const urlAddItem = document.querySelector(".url-add-item")?.textContent;

formItems[0]?.addEventListener("submit", async(e) => {
    e.preventDefault();
    try {
        const response = await fetch(urlAddItem, {
            method: 'POST',
            headers: {
                'X-CSRFToken': formItems[0]["csrfmiddlewaretoken"].value,
                'Content-Type': 'application/json',
                'mode': 'same-origin',
            },
            body: JSON.stringify({
                // sl_opcion: formItems[0]["sl_opcion"].value,
                producto: formItems[0]["articulo"].value,
                tamanio: formItems[0]["tamanio"].value,
                cantidad: formItems[0]["cantidad"].value,
                area: formItems[0]["area"].value,
                marca: formItems[0]["marca"].value,
                modelo: formItems[0]["modelo"].value,
                proyecto: formItems[0]["proyecto"].value,
                resguardo: formItems[0]["resguardo"].value,
                noserie: formItems[0]["noserie"].value,
                noseriei: formItems[0]["noseriei"].value,
                cantidad: formItems[0]["cantidad"].value,
                proveedor: formItems[0]["proveedor"].value,
                categoria: formItems[0]["categoria"].value,
                oc: formItems[0]["oc"].value,
                sl_opcion_oc: formItems[0]["sl_opcion_oc"].value,
                status: formItems[0]["status"].value,
                // fsalida: formItems[0]["fsalida"]?.value ?? "",
                // fregreso: formItems[0]["fregreso"]?.value ?? "",
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
        Swal.fire({
            icon: 'error',
            text: 'Ha ocurrido un error',
            position: 'center'
        })
    }
})
