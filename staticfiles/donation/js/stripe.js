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
const stripePublicKey = JSON.parse(
	document.getElementById("id_stripe_public_key").textContent,
);
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

// Show/hide custom amount input
const customAmountRadio = document.getElementById("customAmount");
const customAmountInput = document.getElementById("customAmountInput");

document.querySelectorAll('input[name="amount"]').forEach((radio) => {
	radio.addEventListener("change", () => {
		if (customAmountRadio.checked) {
			customAmountInput.style.display = "block";
		} else {
			customAmountInput.style.display = "none";
		}
	});
});

// Handle form submit
const form = document.getElementById("donation-form");
const submitButton = form.querySelector('button[type="submit"]');

form.addEventListener("submit", async (ev) => {
	ev.preventDefault();

	// Disable card and button
	card.update({ disabled: true });
	submitButton.setAttribute("disabled", true);

	// Show loading overlay
	document.getElementById("loading-overlay").style.display = "block";

	// Get form data
	const formData = new FormData(form);
	const fullName = formData.get("full_name");
	const email = formData.get("email");
	const phoneNumber = formData.get("phone_number");

	// Get the correct amount value
	let amount = formData.get("amount");
	if (amount === "custom") {
		amount = formData.get("custom_amount");
		if (!amount || amount <= 0) {
			document.getElementById("card-errors").textContent =
				"Please enter a valid donation amount";
			document.getElementById("loading-overlay").style.display = "none";
			card.update({ disabled: false });
			submitButton.removeAttribute("disabled");
			return;
		}
	}

	const csrfToken = formData.get("csrfmiddlewaretoken");

	try {
		// Create payment intent on the server
		const intentResponse = await fetch("/payment/donations/", {
			method: "POST",
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
				"X-CSRFToken": csrfToken,
			},
			body: new URLSearchParams({
				amount: amount,
				full_name: fullName,
				email: email,
				phone_number: phoneNumber,
			}),
		});

		const intentData = await intentResponse.json();

		if (!intentData.client_secret) {
			throw new Error(intentData.error || "Failed to create payment intent");
		}

		// Confirm payment with Stripe
		const result = await stripe.confirmCardPayment(intentData.client_secret, {
			payment_method: {
				card: card,
				billing_details: {
					name: fullName,
					email: email,
					phone: phoneNumber,
				},
			},
		});

		if (result.error) {
			// Show error
			document.getElementById("card-errors").textContent = result.error.message;
			document.getElementById("loading-overlay").style.display = "none";
			card.update({ disabled: false });
			submitButton.removeAttribute("disabled");
		} else {
			if (result.paymentIntent.status === "succeeded") {
				// Redirect to success page
				window.location.href = `/payment/success/${intentData.payment_number}/`;
			}
		}
	} catch (error) {
		document.getElementById("card-errors").textContent = error.message;
		document.getElementById("loading-overlay").style.display = "none";
		card.update({ disabled: false });
		submitButton.removeAttribute("disabled");
	}
});
