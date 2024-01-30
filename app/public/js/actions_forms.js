const btnOpenContainer = document.querySelectorAll(".open-form-container");
const formContainer = document.querySelectorAll(".form-container");
const btnCloseContainer = document.querySelectorAll(".close-form-container");
const form = document.querySelector("#form-tool");
const formItem = document.querySelector(".form-item");
const formSupplier = document.querySelector(".supplier-form");

btnOpenContainer?.forEach((element, id) => {
    element.addEventListener("click", () => {
        formContainer[id]?.classList.toggle("opened")
    })
})

btnCloseContainer?.forEach((element, id) => {
    element.addEventListener("click", () => {
        formContainer[id]?.classList.toggle("opened")
    })
})

// ?? Search all elements inside form that have required class added
form?.querySelectorAll(".required").forEach((element) => {
    // ?? Select each label that contains required class
    const label = element.parentElement;
    // ?? Select each input 
    const input = element?.parentElement.parentElement.querySelector(".input-required");
    // ?? Select each select
    const select = element?.parentElement.parentElement.querySelector(".select-required");
    // ?? Event listener to check if user is typing
    input?.addEventListener("keyup", (e) => {
        const value = e.target.value;
        // ?? Check if input is empty
        if(value.trim() != "") {
            label.style.borderColor = "#000"
        } else {
            label.style.borderColor = "#f00"
        }
    })
    // ?? Event listener to check if user selects an option
    select?.addEventListener("change", (e) => {
        // ?? Get the index from the select tag
        const value = e.target.selectedIndex;
        // ?? Get the text from the selected option
        const text = e.target.options[value].text;
        // ?? Check if option text is empty
        if(text != "") {
            label.style.borderColor = "#000"
        } else {
            label.style.borderColor = "#f00"
        }
    })
})

// ?? Search all elements inside form that have required class added
formItem?.querySelectorAll(".required").forEach((element) => {
    // ?? Select each label that contains required class
    const label = element.parentElement;
    // ?? Select each input 
    const input = element.parentElement.parentElement.querySelector(".input-required");
    // ?? Select each select
    const select = element?.parentElement.parentElement.querySelector(".select-required");
    // ?? Event listener to check if user is typing
    input?.addEventListener("keyup", (e) => {
        const value = e.target.value;
        // ?? Check if input is empty
        if(value.trim() != "") {
            label.style.borderColor = "#000"
        } else {
            label.style.borderColor = "#f00"
        }
    })
    // ?? Event listener to check if user selects an option
    select?.addEventListener("change", (e) => {
        // ?? Get the index from the select tag
        const value = e.target.selectedIndex;
        // ?? Get the text from the selected option
        const text = e.target.options[value].text;
        // ?? Check if option text is empty
        if(text != "") {
            label.style.borderColor = "#000"
        } else {
            label.style.borderColor = "#f00"
        }
    })
})

formSupplier?.querySelectorAll(".required").forEach((element) => {
    // ?? Select each label that contains required class
    const label = element.parentElement;
    // ?? Select each input 
    const input = element.parentElement.parentElement.querySelector(".input-required");
    // ?? Event listener to check if user is typing
    input?.addEventListener("keyup", (e) => {
        const value = e.target.value;
        // ?? Check if input is empty
        if(value.trim() != "") {
            label.style.borderColor = "#000"
        } else {
            label.style.borderColor = "#f00"
        }
    })
})