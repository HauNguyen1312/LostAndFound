document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const query = document.getElementById('search-input').value;
    const resultsContainer = document.getElementById('list-of-items');
    const itemType = document.getElementById('search-button').value;
    resultsContainer.innerHTML = '<p>Searching...</p>';

    // Construct the URL with the query parameter. Replace with your actual API URL.
    const apiUrl = `http://127.0.0.1:8000/api/${itemType}_items/?q=${encodeURIComponent(query)}`;
    
    // Fetch API call to your Django backend
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        
        .then(data => {
            if (data.length === 0) {
                resultsContainer.innerHTML = '<p>No matching items found.</p>';
                return;
            }

            // Loop through the data and create a card for each item
            data.forEach(item => {
                const itemCard = document.createElement('div');
                itemCard.className = 'item-card'; // Add a class for styling
                itemCard.innerHTML = `
                    <h3>${item.description}</h3>
                    <p><strong>Status:</strong> ${item.status}</p>
                    <p><strong>Location:</strong> ${item.location}</p>
                    <p><strong>Category:</strong> ${item.category}</p>
                    <p><strong>Date:</strong> ${item.date}</p>
                `;
                resultsContainer.appendChild(itemCard);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            resultsContainer.innerHTML = '<p>Error fetching data. Please try again.</p>';
        });
});


document.getElementById('email').addEventListener('DOMContentLoaded', function(event) {
    event.preventDefault();
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('email-error');
    
    // Add an event listener that triggers when the user leaves the input field
    emailInput.addEventListener('blur', function() {
        const email = emailInput.value;
        const validDomain = /@live\.vu\.edu\.au$/.test(email);

        if (email.trim() === '') {
            emailError.style.display = 'none'; // Hide error if field is empty
        } else if (!validDomain) {
            emailError.style.display = 'block'; // Show the error message
        } else {
            emailError.style.display = 'none'; // Hide the error message
        }
    });
});