function validateForm() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Send a request to your server-side script for validation
    fetch("../../csharp/login.aspx?username=" + username + "&password=" + password)
        .then(response => response.json())
        .then(data => {
            if (data.isValid) {
                // If the user is valid, redirect to the condominio.html page
                window.location.href = "../html/condominio.html";
            } else {
                // If the user is not valid, display an error message
                alert("Invalid email or password.");
            }
        });

    return false;
}