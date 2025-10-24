/* jshint esversion: 8 */

console.log("Test script file loaded");

// Funtions from Bootstrap
const initBootstrapComponents = () => {
  // Popovers
  const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
  [...popoverTriggerList].map(el => new bootstrap.Popover(el));

  // Calls Toast when modal triggered
  document.querySelectorAll('.toast').forEach(toastEl => {
    const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
    toast.show();
  });

  // Back to top function
  document.querySelectorAll('.btt-link').forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });
};

// Search bar toggle functionality
const initSearchToggle = () => {
  const searchButton = document.getElementById("searchButton");
  const searchInput = document.getElementById("searchInput");
  const searchForm = document.getElementById("searchForm");

  if (!searchButton || !searchInput) return;

  // Hides and shows search bar in main nav
  searchButton.addEventListener("click", (e) => {
    e.stopPropagation();
    if (!searchInput.classList.contains("search-visible")) {
      searchInput.classList.remove("search-hidden");
      searchInput.classList.add("search-visible");
      searchInput.focus();
    } else if (searchInput.value.trim() !== "") {
      searchForm.submit();
    }
  });

  // Close search when clicking outside
  document.addEventListener("click", (e) => {
    if (!searchForm.contains(e.target) && searchInput.classList.contains("search-visible")) {
      searchInput.classList.remove("search-visible");
      searchInput.classList.add("search-hidden");
      searchInput.value = "";
    }
  });
};

// Search setup with keyboard navigation
const setupSearch = (inputId, resultsId) => {
  const searchInput = document.getElementById(inputId);
  const resultsBox = document.getElementById(resultsId);
  
  if (!searchInput || !resultsBox) return;

  let activeIndex = -1;

  // Update active item styling
  const updateActive = (items) => {
    items.forEach((item, index) => {
      if (index === activeIndex) {
        item.classList.add('active');
        item.scrollIntoView({ block: 'nearest' });
      } else {
        item.classList.remove('active');
      }
    });
  };

  // Handle input changes
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
          item.href = `/book-details/${book.slug}/`;
          item.classList.add('list-group-item', 'list-group-item-action');
          item.innerHTML = `
            <div class="d-flex align-items-center">
              ${book.cover ? `<img src="${book.cover}" alt="${book.title}" class="me-2 search-result">` : ''}
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

  // Keyboard navigation
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

  // Hide dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!resultsBox.contains(e.target) && e.target !== searchInput) {
      resultsBox.style.display = 'none';
    }
  });
};

//Changes active tab once selected
const initTabManagement = () => {
  const tabs = document.querySelectorAll("#bookTabs .nav-link");
  
  tabs.forEach(tab => {
    tab.addEventListener("click", function () {
      // Remove 'active' from all tabs
      tabs.forEach(t => { t.classList.remove("active"); });
      // Add 'active' to the clicked one
      this.classList.add("active");
    });
  });
};

// Review show more/less toggle
const initReviewToggle = () => {
  const toggleReview = (link, showFull) => {
    const reviewId = link.getAttribute("data-review-id");
    const shortReview = document.getElementById(`review-${reviewId}`);
    const fullReview = document.getElementById(`full-review-${reviewId}`);
    
    if (showFull) {
      shortReview.style.display = "none";
      fullReview.style.display = "block";
    } else {
      fullReview.style.display = "none";
      shortReview.style.display = "block";
    }
  };

  // Show more
  document.querySelectorAll(".show-more-link").forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      toggleReview(link, true);
    });
  });

  // Show less
  document.querySelectorAll(".show-less-link").forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      toggleReview(link, false);
    });
  });
};

// Initialize everything when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  initBootstrapComponents();
  initSearchToggle();
  setupSearch('searchInput', 'searchResults');
  setupSearch('mobileSearchInput', 'mobileSearchResults');
  initTabManagement();
  initReviewToggle();
});