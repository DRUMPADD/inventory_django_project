const pathName = window.location.pathname;
const links = document.querySelectorAll(".links-content .link")?.forEach((link) => {
    if(link.href.includes(`${pathName}`)) link.classList.add("active")
});

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