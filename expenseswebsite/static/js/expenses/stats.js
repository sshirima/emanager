const renderChart = (data, labels)=>{
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: labels,
        datasets: [{
            label: 'Expense per category last 6 months',
            data: data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        title :{
            display: true,
            text: 'Expenses per category'
        }
    }
});
}

const getChartdata = ()=>{
    fetch('/expense-category-summary').then(res=>res.json()).then((expenseData)=>{
        console.log('data found', expenseData)
        const category_data = expenseData.expense_category_data
        
        const [labels, data] = [Object.keys(category_data), Object.values(category_data)]
        renderChart(data, labels)
    })
}

document.onload = getChartdata()