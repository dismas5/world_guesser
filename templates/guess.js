document.addEventListener('DOMContentLoaded', function () {
    const counter = document.getElementById('counter');
    const guessInput = document.getElementById('guessInput');
    const submitGuess = document.getElementById('submitGuess');
    const resultMessage = document.getElementById('resultMessage');
    
    let count = 0;
    const total = {{ country_count }};
    
    function updateCounter() {
        counter.textContent = `${count}/${total}`;
    }
    
    submitGuess.addEventListener('click', function () {
        const guess = guessInput.value;
        count++;
        updateCounter();
        
        resultMessage.textContent = `Your guess: ${guess}`;
        resultMessage.style.display = 'block';
        guessInput.value = ''; // Clear the input field for the next guess
    });
    
    updateCounter();
});
