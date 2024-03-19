function viewOrder(orderId) {
	console.log(orderId);

	fetch("/order/" + orderId, {
		method: "POST",
	})
		.then((response) => response.json())
		.then((data) => {
			console.log(data);
			displayOrder(data);
		});
}

var item = `
<div class="item">
<div style="width: 80%">
    <p>{{itemName}}</p>
</div>
<div style="width: 20%">
    <p>x{{quantity}}</p>
</div>
</div>
`;

function highlightOrder(order) {
	deliveryItems = document.getElementsByClassName("delivery-item");
	for (let i = 0; i < deliveryItems.length; i++) {
		const item = deliveryItems[i];
		if (item.getAttribute("order") == order) {
			item.style.boxShadow = "0px 0px 15px black";
		} else {
			item.style.boxShadow = "none";
		}
	}
}

let itemDiv = `
<div class="item">
<div style="width: 80%">
    <p>{{itemName}}</p>
</div>
<div style="width: 20%">
    <p>x{{itemQuantity}}</p>
</div>
</div>
`;

function createItemDiv(itemName, itemQuantity) {
	var div = itemDiv.replace("{{itemName}}", itemName);
	div = div.replace("{{itemQuantity}}", itemQuantity);
	return div;
}

function getItemsCode(items) {
	items = JSON.parse(items);
	var code = "";
	// console.log(items);

	for (var i = 0; i < items.length; i++)
		code += createItemDiv(items[i].name, items[i].quantity);
	return code;
}

function displayOrder(order) {
	highlightOrder(order["order_id"]);

	console.log("Order " + order);
	var orderDetails = document.getElementsByClassName(
		"delivery-item-details"
	)[0];

	console.log(orderDetails);

	orderDetails.getElementsByClassName("order_id")[0].textContent =
		"Order ID: " + order["order_id"];
	orderDetails.getElementsByClassName("canteen_name")[0].textContent =
		order["canteen_name"];

	// orderDetails.getElementsByClassName("list-of-items")[0].innerHTML = "";
	console.log(order["items"]);
	orderDetails.getElementsByClassName("list-of-items")[0].innerHTML =
		getItemsCode(order["items"]);
	orderDetails.getElementsByClassName("amount")[0].textContent =
		"Order Value: ₹ " + order["amount"];

	orderDetails.getElementsByClassName("custName")[0].textContent =
		"Name: " + order["customer_name"];
	orderDetails.getElementsByClassName("custPhone")[0].textContent =
		"Phone: " + order["customer_phone"];
	console.log(order);

	fetch("/order/status/" + order["order_id"], {
		method: "POST",
	})
		.then((response) => response.json())
		.then((data) => {
			for (let i = 1; i < 5; i++) {
				const j = data["state".concat(i.toString())];
				if (j === 1) {
					document
						.getElementsByClassName("order-tracking")
						[i - 1].classList.add("completed");
				} else {
					document
						.getElementsByClassName("order-tracking")
						[i - 1].classList.remove("completed");
				}
			}
		});
}

firstOrderID = document
	.getElementById("order_id")
	.innerText.replace("Order ID: ", "");
window.onload = function () {
	viewOrder(firstOrderID);
};
