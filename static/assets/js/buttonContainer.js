



// Event delegation using vanilla JavaScript
document.getElementById('buttonContainer').addEventListener('click', function(event) {
    if (event.target && event.target.className === 'button next scrolly') {
        payWithMonnify();
    }
});

