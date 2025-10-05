console.log("Test script file loaded")

// popup from bootsraps docs
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

//   document.addEventListener("DOMContentLoaded", function () {
//     const searchButton = document.getElementById("searchButton");
//     const searchInput = document.getElementById("searchInput");

//     searchButton.addEventListener("click", function () {
//       // Only show if hidden
//       if (searchInput.classList.contains("d-none")) {
//         searchInput.classList.remove("d-none");
//         searchInput.focus();
//       }
//       // else do nothing — don't toggle back
//     });
//   });

  document.addEventListener("DOMContentLoaded", function () {
    const searchButton = document.getElementById("searchButton");
    const searchInput = document.getElementById("searchInput");
    const searchForm = document.getElementById("searchForm");

    // Show or focus input on button click
    searchButton.addEventListener("click", function (event) {
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
    document.addEventListener("click", function (event) {
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