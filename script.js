function validateForm() {
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();

    if (email === "" || password === "") {
        alert("Please fill in all fields.");
    } 
    else{
        window.location.href="homepage.html"
    }
}

function validateSignUp() {
    let email = document.getElementById("emailSign").value.trim();
    let password = document.getElementById("passSign").value.trim();
    let name = document.getElementById("nameSign").value.trim();
    let age = document.getElementById("ageSign").value.trim();
    if (email === "" || password === "" || name==="" || age==="") {
        alert("Please fill in all fields.");
    } 
    else{
        window.location.href="homepage.html"
    }
}

document.getElementById("recommendationForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevents the form from submitting and reloading the page

    const interests = getSelectedInterests(); 
    const budget = getSelectedBudget(); 
    const duration = getSelectedDuration(); 
    const type = getSelectedType(); 

    // Prepare the data to be sent to the backend
    const data = {
        interests: interests,
        budget: budget,
        duration: duration,
        type: type
    };

    fetch('http://127.0.0.1:5000/predict', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Recommendations:', data.recommended_trips);

        const recommendationsHTML = data.recommended_trips.map(city => `
            <div class="destination">
                <img src="../images/plane.jpg" alt="Plane" class="plane-icon">
                <span class="city-name">${city}</span>
            </div>
        `).join('');

        document.getElementById("results").innerHTML = recommendationsHTML;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function getSelectedInterests() {
    const checkboxes = document.querySelectorAll("input[name='interest']:checked");
    return Array.from(checkboxes).map(checkbox => checkbox.value);
}

function getSelectedBudget() {
    return document.getElementById("budgetInput").value;
}

function getSelectedDuration() {
    return document.getElementById("durationInput").value;
}

function getSelectedType() {
    return document.getElementById("travelTypeSelect").value;
}



function validateForm(event) {
    event.preventDefault();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.message === "Login successful") {
            window.location.href = "homepage.html";
        }
    });
}

function validateSignUp(event) {
    event.preventDefault();
    let name = document.getElementById("nameSign").value.trim();
    let email = document.getElementById("emailSign").value.trim();
    let age = document.getElementById("ageSign").value.trim();
    let password = document.getElementById("passSign").value.trim();

    fetch('http://127.0.0.1:5000/signup', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name, email, age, password })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.message === "User created successfully") {
            window.location.href = "homepage.html";
        }
    });
}

