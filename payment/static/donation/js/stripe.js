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
  const stripePublicKey = JSON.parse(document.getElementById("id_stripe_public_key").textContent);
  const clientSecret = JSON.parse(document.getElementById("id_client_secret").textContent);

  const stripe = Stripe(stripePublicKey);
  const elements = stripe.elements();

  const style = {
    base: {
      color: "#000",
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": { color: "#aab7c4" },
    },
    invalid: { color: "#dc3545", iconColor: "#dc3545" },
  };

  const card = elements.create("card", { style: style });
  card.mount("#card-element");

  card.on("change", (event) => {
    const displayError = document.getElementById("card-errors");
    displayError.textContent = event.error ? event.error.message : "";
  });

// Handle form submit
const form = document.getElementById('payment-form');

form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then((result) => {
        let errorDiv, html;
        if (result.error) {
            errorDiv = document.getElementById('card-errors');
            html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});