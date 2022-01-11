const showPasswordToggle = document.querySelector('.showPasswordToggle');

showPasswordToggle.addEventListener('click', (e)=>{
    if (showPasswordToggle.textContent === 'SHOW'){
        showPasswordToggle.textContent = 'HIDE'
        passwordField.setAttribute('type', 'text')
    } else {
        showPasswordToggle.textContent = 'SHOW'
        passwordField.setAttribute('type', 'password')
    }
});