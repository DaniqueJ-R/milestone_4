console.log("Test script file loaded");

// popup from bootsraps docs
const popoverTriggerList = document.querySelectorAll(
  '[data-bs-toggle="popover"]'
);
const popoverList = [...popoverTriggerList].map(
  (popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl)
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
      searchInput.value = ""; // Clear input when closed
    }
  });
});

function setupSearch(inputId, resultsId) {
  const searchInput = document.getElementById(inputId);
  const resultsBox = document.getElementById(resultsId);
  let activeIndex = -1;

  if (!searchInput) return;

  searchInput.addEventListener('input', async function () {
    const query = this.value.trim();
    activeIndex = -1;

    if (query.length < 2) {
      resultsBox.style.display = 'none';
      resultsBox.innerHTML = '';
      return;
    }

    try {
      const response = await fetch(`/ajax/search/?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      resultsBox.innerHTML = '';

      if (data.results.length > 0) {
        data.results.forEach(book => {
          const item = document.createElement('a');
          item.href = `/book-detail/${book.slug}/`;
          item.classList.add('list-group-item', 'list-group-item-action');
          item.innerHTML = `
            <div class="d-flex align-items-center">
              ${book.cover ? `<img src="${book.cover}" alt="${book.title}" class="me-2" style="width:40px;height:60px;object-fit:cover;">` : ''}
              <span class="search-item">${book.title}</span>
            </div>
          `;
          resultsBox.appendChild(item);
        });
        resultsBox.style.display = 'block';
      } else {
        resultsBox.innerHTML = '<div class="list-group-item text-muted">No results found</div>';
        resultsBox.style.display = 'block';
      }
    } catch (err) {
      console.error('Search error:', err);
    }
  });

  // Hide dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!resultsBox.contains(e.target) && e.target !== searchInput) {
      resultsBox.style.display = 'none';
    }
  });
}

// Initialize both desktop and mobile search
setupSearch('searchInput', 'searchResults');
setupSearch('mobileSearchInput', 'mobileSearchResults');


// Handle keyboard navigation
searchInput.addEventListener('keydown', (e) => {
  const items = Array.from(resultsBox.querySelectorAll('a.list-group-item'));
  if (items.length === 0) return;

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    activeIndex = (activeIndex + 1) % items.length;
    updateActive(items);
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    activeIndex = (activeIndex - 1 + items.length) % items.length;
    updateActive(items);
  } else if (e.key === 'Enter') {
    e.preventDefault();
    if (activeIndex >= 0 && items[activeIndex]) {
      window.location.href = items[activeIndex].href;
    }
  }
});

function updateActive(items) {
  items.forEach((item, index) => {
    if (index === activeIndex) {
      item.classList.add('active');
      item.scrollIntoView({ block: 'nearest' });
    } else {
      item.classList.remove('active');
    }
  });
}

// Hide dropdown when clicking outside
document.addEventListener('click', (e) => {
  if (!resultsBox.contains(e.target) && e.target !== searchInput) {
    resultsBox.style.display = 'none';
  }
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

document.addEventListener("DOMContentLoaded", function () {
  // Show more
  document.querySelectorAll(".show-more-link").forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const reviewId = this.getAttribute("data-review-id");
      document.getElementById("review-" + reviewId).style.display = "none";
      document.getElementById("full-review-" + reviewId).style.display =
        "block";
    });
  });

  // Show less
  document.querySelectorAll(".show-less-link").forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const reviewId = this.getAttribute("data-review-id");
      document.getElementById("full-review-" + reviewId).style.display = "none";
      document.getElementById("review-" + reviewId).style.display = "block";
    });
  });
});
