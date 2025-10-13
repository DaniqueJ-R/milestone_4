console.log("Stripe JS loaded");

// Toggle custom amount input visibility
document.addEventListener("DOMContentLoaded", () => {
  const customRadio = document.getElementById("customAmount");
  const customInput = document.getElementById("customAmountInput");
  const radios = document.querySelectorAll('input[name="amount"]');

  radios.forEach((radio) => {
    radio.addEventListener("change", () => {
      if (customRadio.checked) {
        customInput.style.display = "block";
      } else {
        customInput.style.display = "none";
        customInput.querySelector("input").value = "";
      }
    });
  });
});

// Payment processing
const stripe_public_key = getElementById("id_stripe_public_key")
  .text()
  .slice(1, -1);
const client_secret = getElementById("id_client_secret").text().slice(1, -1);
const stripe = Stripe(stripe_public_key);