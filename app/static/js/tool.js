const urlUpdateTool = document.querySelector(".url-update-tool")?.textContent;
const urlUpdateItemUse = document.querySelector(".url-update-item-use")?.textContent;
const inputsFechas = document.querySelectorAll(".inp-fechas");
const inpFRegreso = document.querySelectorAll(".inp-fregreso");
const inpFSalida = document.querySelectorAll(".inp-fsalida");

const formProduct = document.querySelector(".form-product");
const url = document.querySelector(".url-update-state-product")
const quantityText = document.querySelector("#quantity_available")

const formUseProduct = document.querySelector(".form-use-product");

formTools[0]?.addEventListener("submit", async(e) => {
    e.preventDefault();
    try {
        const response = await fetch(urlUpdateTool, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': formTools[0]["csrfmiddlewaretoken"].value,
                'Content-Type': 'application/json',
                'mode': 'same-origin',
            },
            body: JSON.stringify({
                producto: formTools[0]["herramienta"].value,
                codigo: formTools[0]["codigo"].value,
                tamanio: formTools[0]["tamanio"].value,
                cantidad: formTools[0]["cantidad"].value,
                libraje: formTools[0]["libraje"].value,
                conexion: formTools[0]["conexion"].value,
                medida: formTools[0]["medida"].value,
                noserie: formTools[0]["noserie"].value,
                noseriei: formTools[0]["noseriei"].value,
                proveedor: formTools[0]["proveedor"].value,
                oc: formTools[0]["oc"].value,
                sl_opcion_oc: formTools[0]["sl_opcion_oc"].value,
                status: formTools[0]["status"].value,
                pozo: formTools[0]["pozo"].value,
                observaciones: formTools[0]["observaciones"].value
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
        if(response.status == 201) {
            formContainer[0]?.classList.toggle("opened");
            window.location.reload();
        }
    } catch (error) {
        Swal.fire({
            icon: 'error',
            text: 'Ha ocurrido un error',
            position: 'top-end'
        })
    }
})

function toggleInputActive(element) {
    if(!element.classList.contains("active")) {
        element.classList.add("active")
    } else {
        element.classList.remove("active")
    }
}

document.querySelectorAll("select[name='sl_tipo_mov']").forEach((selector, key) => {
    selector.addEventListener("change", (e) => {
        // console.log(key)
        // console.log(e.target.value)
        const seleccion = e.target.value;
        console.log(seleccion == 'RENTA')
        if(seleccion == 'RENTA') {
            inputsFechas[key].classList.add("active");
            inpFRegreso[key].classList.add("active");
            inpFSalida[key].classList.add("active");
        }
        if(seleccion == 'VENTA') {
            inputsFechas[key].classList.add("active");
            inpFRegreso[key].classList.remove("active");
            inpFSalida[key].classList.add("active");
        }
        if(seleccion == 'USO') {
            inputsFechas[key].classList.remove("active");
            inpFRegreso[key].classList.remove("active");
            inpFSalida[key].classList.remove("active");
        }
    })
})
// document.querySelector("select[name='sl_tipo_mov']").addEventListener("change", (e) => {
//     console.log(e.target.value)
//     const seleccion = e.target.value;
//     if(seleccion == 'RENTA') {
//         inputsFechas.classList.add("active");
//         inpFRegreso.classList.add("active");
//         inpFSalida.classList.add("active");
//     }
//     if(seleccion == 'VENTA') {
//         inputsFechas.classList.add("active");
//         inpFRegreso.classList.remove("active");
//         inpFSalida.classList.add("active");
//     }
//     if(seleccion == 'USO') {
//         inputsFechas.classList.remove("active");
//         inpFRegreso.classList.remove("active");
//         inpFSalida.classList.remove("active");
//     }
// })

// formTools[1]?.addEventListener("submit", async(e) => {
//     e.preventDefault();
//     if(Number(formTools[1]["cantidad_uso"].value) > 0) {
//         await fetch(urlUpdateItemUse, {
//             method: 'POST',
//             mode: 'same-origin',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': formTools[1]["csrfmiddlewaretoken"].value
//             },
//             body: JSON.stringify({
//                 cantidad: formTools[1]["cantidad_uso"].value,
//                 sl_status: formTools[1]["sl_status"].value,
//                 tipo_mov: formTools[1]["sl_tipo_mov"].value,
//                 fsalida: formTools[1]["fsalida"]?.value,
//                 fregreso: formTools[1]["fregreso"]?.value,
//                 condicion: formTools[1]["condicion"].value
//             })
//         }).then(response => response.json())
//         .then(data => {
//             Swal.fire({
//                 title: data.status == 201 ? "Éxito" : "Oh, no!",
//                 icon: data.status == 201 ? 'success' : "warning",
//                 text: data.status == 201 ? data.message : data.message,
//                 position: "center",
//             })
//             if(data.status == 201) {
//                 formContainer[1]?.classList.toggle("opened");
//                 window.location.reload();
//             }
//         }).catch(error => {
//             console.log(error)
//             Swal.fire({
//                 icon: 'error',
//                 text: 'No se ha podido registrar el equipo',
//                 position: 'top-end'
//             })
//             formContainer[1]?.classList.toggle("opened");
//         })
//     }
// })

formTools[1]?.addEventListener("submit", (e) => {
    e.preventDefault();
    if(e.target.quantity.value > quantityText.textContent) {
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
            title: response.status == 201 ? 'Éxito!' : null,
            icon: response.status == 201 ? 'success' : "warning",
            text: data.message,
            position: 'center'
        })
        if(response.status == 201) {
            formContainer[2]?.classList.toggle("opened");
            window.location.reload();
        }
    })
    .catch(error => {
        console.log(error)
        Swal.fire({
            icon: 'error',
            text: 'Ha ocurrido un error',
            position: 'top-end'
        })
    })
})

const btnUpdate = document.querySelector(".btnUpdate");
btnUpdate.addEventListener('click', (e) => {;
    formContainer[2]?.classList.toggle("opened");
})



formProduct?.addEventListener("submit", (e) => {
    e.preventDefault();
    const quantity_current = Number(quantityText.textContent);
    if(e.target.cantidad_uso.value > quantity_current) {
        return Swal.fire({
            title: "La cantidad elegida es mayor a la disponible.",
            icon: "warning",
            position: 'center'
        })
    }
    if(e.target.cantidad_uso.value == 0) {
        return Swal.fire({
            title: "La cantidad debe ser mayor a cero.",
            icon: "warning",
            position: 'center'
        })
    }
    fetch(url.textContent, {
        method: 'PUT',
        mode: "same-origin",
        headers: {
            'X-CSRFToken': e.target.csrfmiddlewaretoken.value,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cantidad: e.target.cantidad_uso?.value,
            condiciones: e.target.condicion?.value,
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


document.querySelectorAll(".btnUseProduct")?.forEach(btn => {
    btn.addEventListener("click", () => {
        const parent = btn.parentElement.parentElement;
        const cantidad = Number(parent.getElementsByTagName("td")[2].textContent);
        formUseProduct["cantidad_uso"].max = cantidad;
        formUseProduct["cantidad_uso"].value = cantidad;
        // console.log(formUseProduct["cantidad_uso"].max)
        formContainer[3].classList.toggle("opened");
        // console.log(cantidad)
    })
})

formUseProduct.addEventListener("submit", (e) => {
    e.preventDefault();
    if(e.target.cantidad_uso.value > 0) {
        fetch(urlUpdateItemUse, {
            method: 'POST',
            headers: {
                'X-CSRFToken': e.target.csrfmiddlewaretoken.value,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                cantidad: e.target.cantidad_uso.value,
                mov_type: e.target.sl_tipo_mov.value,
                fsalida: e.target.fsalida.value,
                fregreso: e.target.fregreso.value,
            })
        })
        .then(res => res.json())
        .then(async(data) => {
            await Swal.fire({
                title: data.status == 201 ? "Éxito" : "Oh, no!",
                icon: data.status == 201 ? 'success' : "warning",
                text: data.status == 201 ? data.message : data.message,
                position: "center",
            })
            if(data.status == 201) {
                formContainer[3]?.classList.toggle("opened");
                window.location.reload();
            }
        }).catch(error => {
            console.log(error)
            Swal.fire({
                icon: 'error',
                text: 'No se ha podido registrar el equipo',
                position: 'center'
            })
            formContainer[3]?.classList.toggle("opened");
        })
    }
})