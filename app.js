// Event listener for form submission
document.getElementById('transaction-form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Get input values
    const amount = parseFloat(document.getElementById('amount').value);
    const description = document.getElementById('description').value;
    const date = document.getElementById('date').value;
    const category = document.getElementById('category').value;

    // Create a transaction object
    const transaction = {
        amount: amount,
        description: description,
        date: date,
        category: category
    };

    // Save the transaction to LocalStorage
    let transactions = JSON.parse(localStorage.getItem('transactions')) || [];
    transactions.push(transaction);
    localStorage.setItem('transactions', JSON.stringify(transactions));

    // Reset form fields
    document.getElementById('transaction-form').reset();

    // Update the transaction list and summary
    updateTransactionsList();
    updateSummary();
    renderChart();
});

// Function to update the transactions list
function updateTransactionsList() {
    const transactions = JSON.parse(localStorage.getItem('transactions')) || [];
    const transactionList = document.getElementById('transaction-list');
    transactionList.innerHTML = '';

    transactions.forEach((transaction, index) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${transaction.description}</span>
            <span>${transaction.amount}</span>
            <span>${transaction.category}</span>
            <span>${transaction.date}</span>
            <button onclick="deleteTransaction(${index})">Delete</button>
        `;
        transactionList.appendChild(li);
    });
}

// Function to update the summary (Total Income, Expense, and Balance)
function updateSummary() {
    const transactions = JSON.parse(localStorage.getItem('transactions')) || [];

    let totalIncome = 0;
    let totalExpense = 0;

    transactions.forEach(transaction => {
        if (transaction.category === 'Income') {
            totalIncome += transaction.amount;
        } else {
            totalExpense += transaction.amount;
        }
    });

    const balance = totalIncome - totalExpense;

    // Update summary fields
    document.getElementById('total-income').innerText = totalIncome.toFixed(2);
    document.getElementById('total-expense').innerText = totalExpense.toFixed(2);
    document.getElementById('balance').innerText = balance.toFixed(2);
}

// Function to delete a transaction
function deleteTransaction(index) {
    let transactions = JSON.parse(localStorage.getItem('transactions')) || [];
    transactions.splice(index, 1);
    localStorage.setItem('transactions', JSON.stringify(transactions));

    // Update the transaction list and summary after deletion
    updateTransactionsList();
    updateSummary();
    renderChart();
}

// Function to render the spending chart using Chart.js
function renderChart() {
    const transactions = JSON.parse(localStorage.getItem('transactions')) || [];
    const categories = ['Food', 'Transport', 'Rent', 'Entertainment', 'Income'];
    const spending = categories.map(category => {
        return transactions.filter(transaction => transaction.category === category)
                           .reduce((sum, transaction) => sum + transaction.amount, 0);
    });

    const ctx = document.getElementById('chart').getContext('2d');
    
    // Create or update the chart
    if (window.chart) {
        window.chart.destroy(); // Destroy the previous chart if exists
    }

    window.chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [{
                label: 'Spending by Category',
                data: spending,
                backgroundColor: ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#FF914D'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Call functions to initially update the transactions list, summary, and chart
updateTransactionsList();
updateSummary();
renderChart();
