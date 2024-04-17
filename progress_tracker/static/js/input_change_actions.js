document.addEventListener('DOMContentLoaded', ()=> {
    const emailField = document.querySelector('#inputEmail');
    const passwordField = document.querySelector('#inputPassword');
    const submitButton = document.querySelector('#submit');
    const confirmPasswordField = document.querySelector('#inputConfirmPassword');
    const usernameField = document.querySelector('#username');

    emailField.addEventListener('keyup', (e) =>
        {
            emailVal = e.target.value;
            emailField.style.borderColor = 'green';
            fetch('/auth/validateEmail',{
                body:JSON.stringify({
                    email: emailVal
                }), 
                method:'POST',
            })
        .then(res=>res.json())
        .then(data=>{const emailField = document.querySelector('#inputEmail');
                if (data['emailError']){
                    submitButton.setAttribute('disabled','disabled');
                    emailField.style.borderColor = 'red';
                } else {
                    submitButton.removeAttribute('disabled','disabled');
                    emailField.style.borderColor = 'green';
                }
        })
    })


    passwordField.addEventListener('keyup', (e) =>
        {
            passwordVal = e.target.value;
            passwordField.style.borderColor = 'green';
            fetch('/auth/validatePassword',{
                body:JSON.stringify({
                    password: passwordVal
                }), 
                method:'POST',
            })
        .then(res=>res.json())
        .then(data=>{
                if (data['passwordError']){
                    submitButton.setAttribute('disabled','disabled');
                    passwordField.style.borderColor = 'red';
                } else {
                    submitButton.removeAttribute('disabled','disabled');
                    passwordField.style.borderColor = 'green';
                }
        })
    })

    if (confirmPasswordField){
        confirmPasswordField.addEventListener('keyup', (e) =>
        {
            passwordVal = e.target.value;
            confirmPasswordField.style.borderColor = 'green';
            fetch('/auth/validatePassword',{
                body:JSON.stringify({
                    password: passwordVal
                }), 
                method:'POST',
            })
        .then(res=>res.json())
        .then(data=>{
                if (data['passwordError'] || passwordVal != passwordField.value){
                    submitButton.setAttribute('disabled','disabled');
                    confirmPasswordField.style.borderColor = 'red';
                } else {
                    submitButton.removeAttribute('disabled','disabled');
                    confirmPasswordField.style.borderColor = 'green';
                    
                }
        })
    })
    }

    if (usernameField){
        usernameField.addEventListener('keyup', (e) =>
        {
            usernameVal = e.target.value;
            usernameField.style.borderColor = 'green';
            fetch('/auth/validateUsername',{
                body:JSON.stringify({
                    password: passwordVal
                }), 
                method:'POST',
            })
        .then(res=>res.json())
        .then(data=>{
                if (data['usernameError']){
                    submitButton.setAttribute('disabled','disabled');
                    usernameField.style.borderColor = 'red';
                } else {
                    submitButton.removeAttribute('disabled','disabled');
                    usernameField.style.borderColor = 'green';
                }
        })
    })
    }


})