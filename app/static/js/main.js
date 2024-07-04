const pathName = window.location.pathname;
const nav = document.querySelector("nav"); 
const body = document.querySelector("body"); 
const bigTitle = document.querySelector(".big-title"); 
const hideMenu = document.querySelector(".hideMenu"); 
const container = document.querySelector(".container"); 
const titles = document.querySelectorAll(".title"); 
const logo = document.querySelector(".logo"); 
const hide = document.querySelector(".hide"); 
const show = document.querySelector(".show"); 
const formContainers = document.querySelectorAll(".form-container"); 
const tableContainers = document.querySelectorAll(".table-container"); 
const textLink = document.querySelectorAll(".text-link"); 
const links = document.querySelectorAll(".links-content .link")?.forEach((link) => {
    if(link.href.includes(`${pathName}`)) link.classList.add("active")
});

window.addEventListener("load", () => {
    body.classList.remove("preload")
})

window.addEventListener("DOMContentLoaded", () => {
    if(localStorage !== undefined) {
        if(localStorage.getItem("alert-open")) {
            window.localStorage.setItem("alert-open", ("alert-open"))
            const btnCloseAlert = document.querySelector("#close-alert")
            btnCloseAlert.addEventListener("click", () => {
                const alert = btnCloseAlert.parentElement;
                if (localStorage.getItem("alert-open")) {
                    alert.classList.toggle(localStorage.getItem("alert-open"));
                    window.localStorage.removeItem("alert-open")
                }
            })
        }

    }
})

if(window.innerWidth >= 800) {
    if(localStorage.getItem("showBtn")) {
        show.classList.add(window.localStorage.getItem("showBtn"));
        bigTitle.classList.add(window.localStorage.getItem("showBtn"));
    }
    if(localStorage.getItem("hideBtn")) {
        hide.classList.toggle(window.localStorage.getItem("hideBtn"))
    }
    if(localStorage.getItem("hide")) {
        nav.classList.add(window.localStorage.getItem("hide"))
        logo.classList.add(window.localStorage.getItem("hide"))
        container.classList.add(window.localStorage.getItem("hide"))
        textLink.forEach(text => {
            text.classList.add(localStorage.getItem("hide"))
        })
        textLink.forEach(text => {
            text.classList.add(localStorage.getItem("hide"))
        })
        formContainers.forEach(form => {
            form.classList.add(localStorage.getItem("hide"))
        })
        tableContainers.forEach(table => {
            table.classList.add(localStorage.getItem("hide"))
        })
        titles.forEach(title => {
            title.classList.add(localStorage.getItem("hide"))
        })
    }
    
    hide?.addEventListener("click", () => {
        window.localStorage.setItem("showBtn", "active")
        window.localStorage.setItem("hideBtn", "deactivate")
        window.localStorage.setItem("hide", "hidden")
        
        bigTitle.classList.toggle(window.localStorage.getItem("showBtn"));
        show.classList.toggle(window.localStorage.getItem("showBtn"))
        hide.classList.toggle(window.localStorage.getItem("hideBtn"))
        nav.classList.toggle(window.localStorage.getItem("hide"))
        logo.classList.toggle(window.localStorage.getItem("hide"))
        titles.forEach(title => {
            title.classList.toggle(localStorage.getItem("hide"))
        })
        container.classList.toggle(window.localStorage.getItem("hide"))
        textLink.forEach(text => {
            text.classList.toggle(localStorage.getItem("hide"))
        })
        tableContainers.forEach(table => {
            table.classList.toggle(localStorage.getItem("hide"))
        })
    })
    show?.addEventListener("click", () => {
        window.localStorage.removeItem("showBtn")
        window.localStorage.removeItem("hideBtn")
        window.localStorage.removeItem("hide")

        bigTitle.classList.toggle(window.localStorage.getItem("showBtn") ?? "active");
        nav.classList.toggle(localStorage.getItem("hide") ?? "hidden")
        hide.classList.toggle(localStorage.getItem("hideBtn") ?? "deactivate")
        show.classList.toggle(localStorage.getItem("showBtn") ?? "active")
        logo.classList.toggle(localStorage.getItem("hide") ?? "hidden")
        container.classList.toggle(localStorage.getItem("hide") ?? "hidden")
        titles.forEach(title => {
            title.classList.toggle(localStorage.getItem("hide") ?? "hidden")
        })
        textLink.forEach(text => {
            text.classList.toggle(localStorage.getItem("hide") ?? "hidden")
        })
        tableContainers.forEach(table => {
            table.classList.toggle(localStorage.getItem("hide") ?? "hidden")
        })
    })
} else {
    hideMenu.style.display = "none"
}