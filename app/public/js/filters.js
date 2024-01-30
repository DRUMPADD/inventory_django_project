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