const selectFilterOption = document.querySelector("[name='sl_filter_option']");
const tableBody = document.querySelector("table tbody");
const tableRows = tableBody.querySelectorAll("tr");

selectFilterOption?.addEventListener('change', function () {
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

const inputSearch = document.querySelector('[name="searchData"]');
const iconSearch = document.querySelector('[name="search-outline"]');
const tableInfo = document.querySelectorAll('table tbody tr');

function showTableInfo(value) {
    if(value) {
        tableInfo.forEach(element => {
            if(element.textContent.toLowerCase().indexOf(value.toLowerCase()) > -1) {
                element.style.display = 'table-row';
            } else {
                element.style.display = 'none';
            }
        })
    } else {
        tableInfo.forEach(element => {
            element.style.display = 'table-row';
        })
    }
}

function toggleIcon(icon, option) {
    if(option == 'add') {
        icon.classList.add("show")
    } else {
        icon.classList.remove("show")
    }
}

inputSearch.addEventListener('keyup', function(e) {
    const value = String(e.target.value);
    if(value.trim() != "") {
        showTableInfo(value)
    } else {
        showTableInfo('')
    }
})
