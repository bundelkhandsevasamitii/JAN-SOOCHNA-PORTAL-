// =====================================
// STATES PAGE JAVASCRIPT (SEARCH & MODAL)
// =====================================

// Live Search Functionality
const searchInput = document.getElementById("stateSearchInput");
if (searchInput) {
    searchInput.addEventListener("input", function() {
        const query = this.value.toLowerCase().trim();
        const cards = document.querySelectorAll(".state-card");
        
        cards.forEach(card => {
            const text = card.getAttribute("data-name").toLowerCase();
            if (text.includes(query)) {
                card.style.display = "flex";
            } else {
                card.style.display = "none";
            }
        });
    });
}

// Modal Functions
window.openModal = function(name, capital, districts, heritage, centers) {
    document.getElementById("modalTitle").innerText = `${name} - विस्तृत परिचय`;
    document.getElementById("modalBody").innerHTML = `
        <table class="modal-info-table">
            <tr><td>राजधानी:</td><td>${capital}</td></tr>
            <tr><td>कुल जिले:</td><td>${districts}</td></tr>
            <tr><td>प्रमुख केंद्र:</td><td>${centers}</td></tr>
            <tr><td>ऐतिहासिक धरोहरें:</td><td>${heritage}</td></tr>
        </table>
    `;
    document.getElementById("stateModal").style.display = "flex";
}

window.closeModal = function() {
    document.getElementById("stateModal").style.display = "none";
}

// Close modal when clicking outside the box
window.addEventListener("click", function(e) {
    const modal = document.getElementById("stateModal");
    if (e.target === modal) {
        modal.style.display = "none";
    }
});
