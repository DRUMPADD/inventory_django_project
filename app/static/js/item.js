const urlUpdateItem = document.querySelector(".url-update-item")?.textContent;
const urlUpdateItemUse = document.querySelector(".url-update-item-use")?.textContent;
const inputsFechas = document.querySelector(".inp-fechas");
const inpFRegreso = document.querySelector(".inp-fregreso");
const inpFSalida = document.querySelector(".inp-fsalida");

formItems[0]?.addEventListener("submit", async(e) => {
    e.preventDefault();
    try {
        const res = await fetch(urlUpdateItem, {
            method: 'PUT',
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
                oc: formItems[0]["oc"].value,
                sl_opcion_oc: formItems[0]["sl_opcion_oc"].value,
                status: formItems[0]["status"].value,
                // fsalida: formItems[0]["fsalida"]?.value ?? "",
                // fregreso: formItems[0]["fregreso"]?.value ?? "",
            })
        })

        if(res.status != 201) {
            throw Error(res.statusText)
        }
        const data = await res.json();
        console.log(data)
        await Swal.fire({
            title: data.status == 201 ? 'Éxito!' : "Oh, no!",
            icon: data.status == 201 ? 'success' : "warning",
            text: data.message,
            position: 'center'
        })
        if(data.status == 201) {
            formContainer[0]?.classList.toggle("opened");
            window.location.reload();
        }
    } catch(e) {
        console.log(e)
        Swal.fire({
            icon: 'error',
            text: 'No se ha podido modificar el equipo',
            position: 'center'
        })
        return
    }
})

// formContainer[1]?.classList.toggle("opened");

function toggleInputActive(element) {
    if(!element.classList.contains("active")) {
        element.classList.add("active")
    } else {
        element.classList.remove("active")
    }
}

document.querySelector("select[name='sl_tipo_mov']").addEventListener("change", (e) => {
    console.log(e.target.value)
    const seleccion = e.target.value;
    if(seleccion == 'RENTA') {
        inputsFechas.classList.add("active");
        inpFRegreso.classList.add("active");
        inpFSalida.classList.add("active");
    }
    if(seleccion == 'USO') {
        inputsFechas.classList.remove("active");
        inpFRegreso.classList.remove("active");
        inpFSalida.classList.remove("active");
    }
})

formItems[1]?.addEventListener("submit", async(e) => {
    e.preventDefault();
    if(Number(formItems[1]["cantidad_uso"].value) > 0) {
        await fetch(urlUpdateItemUse, {
            method: 'POST',
            mode: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formItems[1]["csrfmiddlewaretoken"].value
            },
            body: JSON.stringify({
                cantidad: formItems[1]["cantidad_uso"].value,
                sl_status: formItems[1]["sl_status"].value,
                tipo_mov: formItems[1]["sl_tipo_mov"].value,
                fsalida: formItems[1]["fsalida"]?.value,
                fregreso: formItems[1]["fregreso"]?.value,
                condicion: formItems[1]["condicion"].value
            })
        }).then(response => response.json())
        .then(data => {
            Swal.fire({
                title: data.status == 201 ? "Éxito" : "Oh, no!",
                icon: data.status == 201 ? 'success' : "warning",
                text: data.status == 201 ? data.message : data.message,
                position: "center",
            })
            if(data.status == 201) {
                formContainer[1]?.classList.toggle("opened");
                window.location.reload();
            }
        }).catch(error => {
            console.log(error)
            Swal.fire({
                icon: 'error',
                text: 'No se ha podido modificar el equipo',
                position: 'top-end'
            })
            formContainer[1]?.classList.toggle("opened");
        })
    }
})

document.querySelectorAll(".btnUpdate").forEach(btn => {
    btn.addEventListener('click', (e) => {
        const id = btn.parentElement;
        const tr = btn.parentElement.parentElement;
        console.log(id)
        formContainer[2]?.classList.toggle("opened");
        formItems[2]["url"].value = id.getAttribute('id');
        formItems[2]["cantidad_uso"].value = tr.querySelectorAll('td')[2].textContent;
        formItems[2]["sl_status"].value = tr.querySelectorAll('td')[3].getAttribute("id-status");
        formItems[2]["condicion"].value = tr.querySelectorAll('td')[4].textContent.trim();
    })
})

formItems[2]?.addEventListener("submit", async(e) => {
    e.preventDefault();
    if(formItems[2]["sl_status"].value == 'Listo') {
        Swal.fire({
            title: "Está seguro de continuar?",
            text: "Una vez devuelto el equipo no se podrá editar este registro.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Si, regresar equipo",
            cancelButtonText: "Descartar",
        }).then(async(result) => {
            if (result.isConfirmed) {
                if(Number(formItems[2]["cantidad_uso"].value) > 0) {
                    await fetch(formItems[2]["url"].value, {
                        method: 'PUT',
                        mode: 'same-origin',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': formItems[2]["csrfmiddlewaretoken"].value
                        },
                        body: JSON.stringify({
                            "cantidad_uso": formItems[2]["cantidad_uso"].value,
                            "condicion": formItems[2]["condicion"].value,
                            "sl_status": formItems[2]["sl_status"].value
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
                            formContainer[2]?.classList.toggle("opened");
                            window.location.reload();
                        }
                    }).catch(error => {
                        console.log(error)
                        formContainer[2]?.classList.toggle("opened");
                        Swal.fire({
                            icon: 'error',
                            text: 'No se puede actualizar el uso del equipo',
                            position: 'center'
                        })
                    })
                }
            }
        });
        return
    }
    if(Number(formItems[2]["cantidad_uso"].value) > 0) {
        await fetch(formItems[2]["url"].value, {
            method: 'PUT',
            mode: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formItems[2]["csrfmiddlewaretoken"].value
            },
            body: JSON.stringify({
                "cantidad_uso": formItems[2]["cantidad_uso"].value,
                "condicion": formItems[2]["condicion"].value,
                "sl_status": formItems[2]["sl_status"].value
            })
        }).then(response => response.json())
        .then(async (data) => {
            await Swal.fire({
                title: data.status == 200 ? "Éxito" : "Oh, no!",
                icon: data.status == 200 ? 'success' : "warning",
                text: data.status == 200 ? data.message : "Oh, no!",
                position: data.status == 200 ? "center" : "top-end",
            })
            if(data.status == 200) {
                formContainer[2]?.classList.toggle("opened");
                window.location.reload();
            }
        }).catch(error => {
            console.log(error)
            formContainer[2]?.classList.toggle("opened");
            Swal.fire({
                icon: 'error',
                text: 'No se puede actualizar el uso del equipo',
                position: 'top-end'
            })
        })
    }
})