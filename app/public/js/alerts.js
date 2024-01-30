const user = document.querySelector(".input-text");

user.addEventListener("keyup", (e) => {
    let string = e.target.value;

    if(!string.length) {
        user.classList.add("error")
    } else {
        user.classList.remove("error")
    }
})