console.log("Test script file loaded");

// popup from bootsraps docs
const popoverTriggerList = document.querySelectorAll(
	'[data-bs-toggle="popover"]',
);
const popoverList = [...popoverTriggerList].map(
	(popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl),
);

// Calls Toast when modal triggered
document.addEventListener("DOMContentLoaded", () => {
	const toastElements = document.querySelectorAll(".toast");
	toastElements.forEach((toastEl) => {
		const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
		toast.show();
	});
});

// Hides and shows search bar in main nav
document.addEventListener("DOMContentLoaded", () => {
	const searchButton = document.getElementById("searchButton");
	const searchInput = document.getElementById("searchInput");
	const searchForm = document.getElementById("searchForm");

	// Show or focus input on button click
	searchButton.addEventListener("click", (event) => {
		event.stopPropagation(); // prevent triggering the outside click listener
		if (!searchInput.classList.contains("search-visible")) {
			searchInput.classList.remove("search-hidden");
			searchInput.classList.add("search-visible");
			searchInput.focus();
		} else if (searchInput.value.trim() !== "") {
			// Optional: submit form if input already visible and filled
			searchForm.submit();
		}
	});

	// Close search input when clicking outside
	document.addEventListener("click", (event) => {
		if (
			!searchForm.contains(event.target) &&
			searchInput.classList.contains("search-visible")
		) {
			searchInput.classList.remove("search-visible");
			searchInput.classList.add("search-hidden");
			searchInput.value = ""; // optional: clear input when closed
		}
	});
});

//Changes active tab once selected
document.addEventListener("DOMContentLoaded", () => {
	const tabs = document.querySelectorAll("#bookTabs .nav-link");

	tabs.forEach((tab) => {
		tab.addEventListener("click", function () {
			// Remove 'active' from all tabs
			tabs.forEach((t) => t.classList.remove("active"));

			// Add 'active' to the clicked one
			this.classList.add("active");
		});
	});
});
