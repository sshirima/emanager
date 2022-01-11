const searchField = document.querySelector('#searchField');
const tableSearch = document.querySelector('.table-search-output');
const tableContainer = document.querySelector('.table-container');
const paginationContainer = document.querySelector('.pagination-container');
const tableSearchBody = document.querySelector('.table-search-output-body');
tableSearch.style.display ='none'

searchField.addEventListener('keyup', (e)=>{
    
    const searchVal = e.target.value;
    

    if (searchVal.length > 0){
        tableSearchBody.innerHTML = ''
        fetch('/expenses/search', {
            body:JSON.stringify({searchText : searchVal}),
            method:"POST"
        })
        .then(res =>res.json())
        .then(data=>{
            console.log('data', data)
            tableSearch.style.display = "block";
            tableContainer.style.display = "none";
            paginationContainer.style.display = "none";
            if (data.length === 0){
                tableSearch.innerHTML = "No Result Found"
            } else {
                data.forEach((item) => {
                    tableSearchBody.innerHTML +=`
                        <tr>
                            <td>${item.amount}</td>
                            <td>${item.category}</td>
                            <td>${item.description}</td>
                            <td>${item.date}</td>
                        </tr>
                `
                });
                
            }
        })
    } else {
        tableContainer.style.display = "block";
        paginationContainer.style.display = "block";
        tableSearch.style.display = "none";
    }
});