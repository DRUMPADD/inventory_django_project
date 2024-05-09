const selectFilterOption = document.querySelector("[name='sl_filter_option']");
const tableBody = document.querySelector("table tbody");
const tableRows = tableBody.querySelectorAll("tr");

selectFilterOption.addEventListener('change', function () {
    const value = this.value;
    
    tableRows.forEach((txt) => {
        const txtRowValue = txt.getAttribute("data-code");
        if(txtRowValue.toUpperCase().indexOf(value) > -1) {
            txt.style.display = "table-row";
        } else {
            txt.style.display = "none";
        }
    })
})

const searchInput = document.querySelector("[name='searchProduct']")
const tableInfo = document.querySelectorAll("#data-list tr")

searchInput?.addEventListener('keyup', (e) => {
    const value = String(e.target.value);

    if(value.trim() != "") {
        console.log(value)
        tableInfo.forEach(text => {
            if(text.innerHTML.toLocaleLowerCase().indexOf(value.toLocaleLowerCase()) != -1) {
                text.style.display = "table-row";
            } else {
                text.style.display = "none";
            }
        })
    }

})