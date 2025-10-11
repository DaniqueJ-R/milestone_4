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


document.addEventListener('DOMContentLoaded', function() {
  // Show more
  document.querySelectorAll('.show-more-link').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const reviewId = this.getAttribute('data-review-id');
      document.getElementById('review-' + reviewId).style.display = 'none';
      document.getElementById('full-review-' + reviewId).style.display = 'block';
    });
  });

  // Show less
  document.querySelectorAll('.show-less-link').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const reviewId = this.getAttribute('data-review-id');
      document.getElementById('full-review-' + reviewId).style.display = 'none';
      document.getElementById('review-' + reviewId).style.display = 'block';
    });
  });
});

  // Toggle custom amount input visibility
  document.addEventListener('DOMContentLoaded', function() {
    const customRadio = document.getElementById('customAmount');
    const customInput = document.getElementById('customAmountInput');
    const radios = document.querySelectorAll('input[name="amount"]');

    radios.forEach(radio => {
      radio.addEventListener('change', function() {
        if (customRadio.checked) {
          customInput.style.display = 'block';
        } else {
          customInput.style.display = 'none';
          customInput.querySelector('input').value = '';
        }
      });
    });
  });