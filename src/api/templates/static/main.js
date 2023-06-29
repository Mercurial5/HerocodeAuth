function register() {
    const username = document.getElementById('register-username').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value.trim();

    const data = {};

    if (username) {
        data.username = username;
    }

    if (email) {
        data.email = email;
    }

    if (password) {
        data.password = password;
    }

    fetch('/api/v1/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    console.log(data.message);
                });
            } else {
                response.json().then(data => {
                    console.log(data.message);
                });
                console.log('Registration failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}



function login() {
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value.trim();

    const data = {};

    if (email) {
        data.email = email;
    }

    if (password) {
        data.password = password;
    }

    fetch('/api/v1/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    localStorage.setItem('access_token', data.access_token);
                    if (!data.message) {
                        console.log("You are logged in");
                    } else {
                        console.log(data.message);
                    }
                });
                // redirect to a new page
            } else {
                console.log('Verification failed');
                response.json().then(data => {
                    console.log(data.message);
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function reset_password() {
    const email = document.getElementById('reset-password-email').value.trim();
    const new_password = document.getElementById('reset-new-password').value.trim();

    const data = {};

    if (email) {
        data.email = email;
    }

    if (new_password) {
        data.new_password = new_password;
    }

    fetch('/api/v1/reset-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    console.log(data.message);
                });
            } else {
                console.log('Reset password failed');
                response.json().then(data => {
                    console.log(data.message);
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function change_password() {
    const old_password = document.getElementById('change-password-email').value.trim();
    const new_password = document.getElementById('change-new-password').value.trim();

    const data = {};

    if (old_password) {
        data.old_password = old_password;
    }

    if (new_password) {
        data.new_password = new_password;
    }

    fetch('/api/v1/change-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    console.log(data.message);
                });
            } else {
                console.log('Reset password failed');
                response.json().then(data => {
                    console.log(data.message);
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


const registerButton = document.getElementById('register-button');
registerButton.addEventListener('click', register);

const loginButton = document.getElementById('login-button');
loginButton.addEventListener('click', login);

const ResetPasswordButton = document.getElementById('reset-password-button');
ResetPasswordButton.addEventListener('click', reset_password);

const ChangePasswordButton = document.getElementById('change-password-button');
ChangePasswordButton.addEventListener('click', change_password);
