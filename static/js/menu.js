let items = document.getElementsByClassName("item");

for (let i = 0; i < items.length; i++) {
	var item = items[i];
	let add_to_cart_button = item.querySelector(".add-to-cart-button");
	add_to_cart_button.addEventListener("click", () => {
		add_to_cart_button.style.display = "none";
		let parent = add_to_cart_button.parentElement.parentElement;
		const itemID = parent.getAttribute("itemID");
		const cantID = parent.getAttribute("cantID");
		// let quantity_div = parent.querySelector(".quantity");
		// quantity_div.style.display = "block";
		// let quantityInput = quantity_div.querySelector("#quantity");
		// quantityInput.textContent = 1;
		// if (parseInt(quantityInput.textContent) == 1) {
		// 	quantity_div.querySelector(".minus-img").src =
		// 		"../static/assets/delete.svg";
		// }

		updateCart(itemID, cantID, 1);
	});
}

const quantity_divs = document.getElementsByClassName("quantity");

for (let i = 0; i < quantity_divs.length; i++) {
	let quantity = quantity_divs[i];
	const quantityInput = quantity.querySelector("#quantity");
	const plusBtn = quantity.querySelector(".plus");
	const minusBtn = quantity.querySelector(".minus");

	if (parseInt(quantityInput.value) == 1) {
		// minusBtn.style.backgroundColor = 'red';
		quantity.querySelector(".minus-img").src =
			"../static/assets/delete.svg";
	}

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
		if (newValue == 0) {
			let add_to_cart_button = quantity.querySelector(
				".add-to-cart-button"
			);
			add_to_cart_button.style.display = "block";
		}
		if (newValue <= quantityInput.getAttribute("max"))
			plusBtn.style.display = "block";

		if (newValue >= quantityInput.getAttribute("min"))
			quantityInput.textContent = newValue;
		else quantityInput.textContent = quantityInput.getAttribute("min");

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
		"../addToCart?item_id=" +
			itemID +
			"&canteen_id=" +
			cantID +
			"&quantity=" +
			quantity,
		{
			method: "POST",
		}
	);
}

const cartDiv = document.querySelector(".cart");
console.log(cartDiv.textContent);
cart = JSON.parse(cartDiv.textContent.replace(/'/g, '"'));
console.log(cart);

const menuItemDivs = document.getElementsByClassName("item");
let menuItemIds = [];
for (let i = 0; i < menuItemDivs.length; i++) {
	let menuItem = menuItemDivs[i];
	let currItemID = menuItem.getAttribute("itemID");
	menuItemIds.push(currItemID);
}
console.log(menuItemIds);

const cartItemIDs = cart["itemList"];
console.log(cartItemIDs);

const cartItems = cart["items"];
console.log(cartItems);

const canteen_id = cart["canteen_id"];
let cartInd = 0;

if (
	canteen_id == document.getElementById("canteenName").getAttribute("cantID")
) {
	for (let menuInd = 0; menuInd < menuItemDivs.length; menuInd++) {
		let menuItem = menuItemDivs[menuInd];
		let currMenuItemID = menuItem.getAttribute("itemID");
		// console.log(currItemID);
		for (let cartInd = 0; cartInd < cartItemIDs.length; cartInd++) {
			if (currMenuItemID == cartItemIDs[cartInd]) {
				add_to_cart_button = menuItem.querySelector(
					".add-to-cart-button"
				);
				add_to_cart_button.style.display = "none";
				quantity_div = menuItem.querySelector(".quantity");
				quantity_div.style.display = "block";
				quantityInput = quantity_div.querySelector("#quantity");
				// console.log(currItemID);

				// console.log(currMenuItemID);
				// console.log(cartInd);

				// console.log("Q" + cartItems[cartInd]["quantity"]);

				quantityInput.textContent = cartItems[cartInd]["quantity"];
				console.log(quantityInput.textContent);
				if (parseInt(quantityInput.textContent) != 1) {
					console.log("here");
					// let img = quantity_div.getElementsByClassName("minus-img")[0];
					// console.log(img);
					quantity_div.getElementsByClassName("minus-img")[0].src =
						"../static/assets/minus.svg";
				}

				console.log(currMenuItemID, cartItemIDs[cartInd]);
				cartInd++;
			}
		}
	}
}

const canteen_id2 = document
	.getElementById("canteenName")
	.getAttribute("cantID");

function filterItems() {
	var checkboxes = document.querySelectorAll("input[type=checkbox]");

	var checked = Array.prototype.slice
		.call(checkboxes)
		.filter((x) => x.checked)
		.map((x) => x.id);

	console.log(checked);
	const str = checked.join(",");
	console.log(str);

	var url = window.location.href;

	window.location.href = "../canteen/" + canteen_id2 + "?filter=" + str;
}
