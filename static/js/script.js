document.getElementById("itemForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const formData = {
    status: document.getElementById("status").value,
    item: document.getElementById("item").value,
    location: document.getElementById("location").value,
    date: document.getElementById("date").value,
    contact: document.getElementById("contact").value,
    image: document.getElementById("image").value,
  };

  fetch("https://script.google.com/macros/s/AKfycbxNflV29SkHx1J10j26H5_LqRUH5FvrAcKed66Pf9kBe5-8VfsrwrS_vQAG8ymOzAxaww/exec", {
    method: "POST",
    mode: "no-cors",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then(() => {
      document.getElementById("confirmation").style.display = "block";
      document.getElementById("itemForm").reset();
    })
    .catch((error) => console.error("Error:", error));
});

// Load reported items
fetch("https://script.google.com/macros/s/AKfycbxNflV29SkHx1J10j26H5_LqRUH5FvrAcKed66Pf9kBe5-8VfsrwrS_vQAG8ymOzAxaww/exec")
  .then(response => response.json())
  .then(data => {
    const itemsContainer = document.getElementById("itemsContainer");
    itemsContainer.innerHTML = "";

    data.forEach((row, index) => {
      if (index === 0) return; // Skip headers

      const [timestamp, status, item, location, date, contact, image] = row;
      const div = document.createElement("div");
      div.style.border = "1px solid #ccc";
      div.style.padding = "10px";
      div.style.marginBottom = "10px";

      div.innerHTML = `
        <strong>Status:</strong> ${status}<br>
        <strong>Item:</strong> ${item}<br>
        <strong>Location:</strong> ${location}<br>
        <strong>Date:</strong> ${date}<br>
        <strong>Contact:</strong> ${contact}<br>
        ${image ? `<img src="${image}" alt="Item image" style="max-width: 200px; margin-top: 10px;">` : ""}
      `;

      itemsContainer.appendChild(div);
    });
  })
  .catch(error => {
    document.getElementById("itemsContainer").innerText = "Failed to load items.";
    console.error("Error loading items:", error);
});
