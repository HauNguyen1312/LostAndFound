document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const query = document.getElementById('search-input').value;
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = ''; // Clear previous results

    // Construct the URL with the search query
    // This example searches for 'lost' items
    const apiUrl = `http://127.0.0.1:8000/api/lost_items/?q=${encodeURIComponent(query)}`;

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.length === 0) {
                resultsContainer.innerHTML = '<p>No results found.</p>';
                return;
            }
            data.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'item-card';
                itemDiv.innerHTML = `
                    <h3>${item.description}</h3>
                    <p><strong>Status:</strong> ${item.status}</p>
                    <p><strong>Location:</strong> ${item.location}</p>
                    <p><strong>Category:</strong> ${item.category}</p>
                    <p><strong>Date:</strong> ${item.date}</p>
                `;
                resultsContainer.appendChild(itemDiv);
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            resultsContainer.innerHTML = '<p>Error fetching data. Please try again.</p>';
        });
});