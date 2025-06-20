ops = document.querySelectorAll(".operation")
for (op of ops) {
    if (op.innerHTML == 'sell') {
        op.style.color = 'red';
    }
    if (op.innerHTML == 'buy') {
        op.style.color = 'green';
    }
}
