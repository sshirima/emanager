const usernameField = document.querySelector('#usernameField');
const emailField = document.querySelector('#emailField');
const passwordField = document.querySelector('#passwordField');
const submitBtn = document.querySelector('.submit-btn');
const invalidUsernameFeedbackArea = document.querySelector('.invalid_username_feedback');
const invalidEmailFeedbackArea = document.querySelector('.invalid_email_feedback');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');
const emailSuccessOutput = document.querySelector('.emailSuccessOutput');

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


emailField.addEventListener('keyup', (e)=>{
    
    const emailVal = e.target.value
    emailSuccessOutput.textContent = `Checking ${emailVal}`
    emailField.classList.remove("is-invalid")
    invalidEmailFeedbackArea.style.display = 'none'

    if (emailVal.length > 0){
        fetch('/authentication/validate-email', {
            body:JSON.stringify({email : emailVal}),
            method:"POST"
        })
        .then(res =>res.json())
        .then(data=>{
            emailSuccessOutput.style.display= 'none'
            if (data.email_error){
                submitBtn.disabled = true
                emailField.classList.add("is-invalid")
                invalidEmailFeedbackArea.style.display = 'block'
                invalidEmailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`
            } else {
                submitBtn.removeAttribute('disabled')
            }
        })
    }
});
          
usernameField.addEventListener('keyup', (e)=>{
    
    const usernameVal = e.target.value
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`

    usernameField.classList.remove("is-invalid")
    invalidUsernameFeedbackArea.style.display = 'none'

    if (usernameVal.length > 0){
        fetch('/authentication/validate-username', {
            body:JSON.stringify({username : usernameVal}),
            method:"POST"
        })
        .then(res =>res.json())
        .then(data=>{
            usernameSuccessOutput.style.display = 'none'
            if (data.username_error){
                usernameField.classList.add("is-invalid")
                invalidUsernameFeedbackArea.style.display = 'block'
                invalidUsernameFeedbackArea.innerHTML = `<p>${data.username_error}</p>`
            }
        })
    }
});