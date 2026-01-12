//gonna fetch and display all expenses
async function fetchExpenses() {
    const res = await fetch('/expenses');
    const data = await res.json();

    const tbody = document.querySelector("#expense-table tbody");
    tbody.innerHTML = "";

    let total = 0;

    data.forEach(expense => {
        total += expense.amount;

        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${expense.date}</td>
            <td>$${expense.amount.toFixed(2)}</td>
            <td>${expense.category}</td>
            <td>${expense.description}</td>
        `;
        tbody.appendChild(row);
    });

    document.getElementById("total").textContent = total.toFixed(2);
}

//add new expense
async function addExpense() {
    const amount = parseFloat(document.getElementById("amount").value);
    const category = document.getElementById("category").value;
    const description = document.getElementById("description").value;

    if (!amount || !category) {
        alert("Amount and category are required!");
        return;
    }

    await fetch('/expenses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount, category, description })
    });

    //clear form
    document.getElementById("amount").value = "";
    document.getElementById("category").value = "";
    document.getElementById("description").value = "";

    fetchExpenses();
}

//load expenses on page load
window.onload = fetchExpenses;
