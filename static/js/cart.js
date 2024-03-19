const quantity_divs = document.getElementsByClassName("quantity");

for (let i = 0; i < quantity_divs.length; i++) {
	let quantity = quantity_divs[i];
	const quantityInput = quantity.querySelector("#quantity");
	const plusBtn = quantity.querySelector(".plus");
	const minusBtn = quantity.querySelector(".minus");

	if (parseInt(quantityInput.textContent) != 1)
		quantity.querySelector(".minus-img").src = "../static/assets/minus.svg";
	else
		quantity.querySelector(".minus-img").src =
			"../static/assets/delete.svg";

	const itemID = quantity.getAttribute("itemID");
	const cantID = quantity.getAttribute("cantID");

	plusBtn.addEventListener("display", () => {
		let currentValue = parseInt(quantityInput.textContent);
		updateCart(itemID, cantID, currentValue);
	});

	plusBtn.addEventListener("click", () => {
		let currentValue = parseInt(quantityInput.textContent);
		let newValue = currentValue + 1;
		if (newValue < quantityInput.getAttribute("max"))
			quantityInput.textContent = newValue;
		else {
			quantityInput.textContent = quantityInput.getAttribute("max");
			plusBtn.style.display = "none";
		}
		if (newValue > 1)
			quantity.querySelector(".minus-img").src =
				"../static/assets/minus.svg";
		updateCart(itemID, cantID, newValue);
	});

	minusBtn.addEventListener("click", () => {
		let currentValue = parseInt(quantityInput.textContent);
		let newValue = currentValue - 1;
		if (newValue <= quantityInput.getAttribute("max"))
			plusBtn.style.display = "block";

		quantityInput.textContent = newValue;

		if (newValue == 1) {
			// minusBtn.style.backgroundColor = 'red';
			quantity.querySelector(".minus-img").src =
				"../static/assets/delete.svg";
		} else {
			quantity.querySelector(".minus-img").src =
				"../static/assets/minus.svg";
		}

		updateCart(itemID, cantID, newValue);
	});
}

function updateCart(itemID, cantID, quantity) {
	fetch(
		"../checkout?item_id=" +
			itemID +
			"&canteen_id=" +
			cantID +
			"&quantity=" +
			quantity,
		{
			method: "POST",
		}
	).then(setTimeout(() => window.location.reload(true), 50));
}

function placeOrder() {
	let items = document.getElementsByClassName("list-of-products")[0];
	items = items.getAttribute("items");
	console.log(items);

	// var user;
	// fetch("user", {
	// 	method: "GET",
	// }).then((response) => {
	// 	if (response.status == 200) {
	// 		response.json().then((data) => {
	// 			// console.log(data);
	// 			user = data;
	// 			// console.log(user);
	const addr = document.getElementById("address-input").value;

	if (addr == "") {
		alert("Please enter an address");
		return;
	}

	fetch("placeOrder?address=" + addr , {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
	}).then((response) => {
		if (response.status == 200) {
			window.location.href = "/viewOrders";
		} else {
			alert("Error placing order");
		}
	});
	// 		});
	// 	} else {
	// 		alert("Error placing order");
	// 	}
	// });

	// console.log(user);

	// fetch("placeOrder?", {
	// 	method: "POST",
	// }).then((response) => {
	// 	if (response.status == 200) {
	// 		window.location.href = "/checkout";
	// 	} else {
	// 		alert("Error placing order");
	// 	}
	// });
}
