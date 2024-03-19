let parDiv = document.getElementsByClassName("parentDiv")[0];
console.log(parDiv);

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

let rtDiv = `
<div class="delivery-item-details">
    <div style="width: 80%">
        <p
            style="
                font-size: 50px;
                font-weight: 800;
                line-height: 10px;
            "
        >
            Order ID: {{order_id}}
        </p>
        <p
            style="
                font-size: 40px;
                font-weight: 600;
                line-height: 10px;
            "
        >
            {{canteen_name}}
        </p>
        <p style="font-size: 26px">Items Ordered:</p>
        <div class="list-of-items">
        {{items}}
        </div>
        <p
            style="
                font-size: 26px;
                margin-left: 8px;
                font-weight: 600;
            "
        >
            Order Value: ₹ {{order['total']}}
            <br />
            Delivery Amount : ₹ {{order['del_charges']}}
        </p>
    </div>

    <div style="width: 60%">
        <div class="customer-details">
            <p
                style="
                    font-size: 26px;
                    line-height: 40px;
                    font-weight: 400;
                "
            >
                Customer Name: {{customer_name}}
                <br />
                Delivery Address: {{address}}
                <br />
                Contact Number: {{customer_phone}}
            </p>
        </div>

        <div class="order-status" status = {{status}}>
            <p style="font-size: 30px; font-weight: 600">
                Update Order Status
            </p>
            <div class="radio-group">
                <input
                    type="radio"
                    id="option1"
                    name="options"
                    value="option1"
                />
                <label for="option1">Order Accepted</label>
            </div>
            <div class="radio-group">
                <input
                    type="radio"
                    id="option2"
                    name="options"
                    value="option2"
                />
                <label for="option2">Cooking </label>
            </div>
            <div class="radio-group">
                <input
                    type="radio"
                    id="option3"
                    name="options"
                    value="option3"
                />
                <label for="option3">Picked Up</label>
            </div>
            <div class="radio-group">
                <input
                    type="radio"
                    id="option4"
                    name="options"
                    value="option4"
                />
                <label for="option4">Delivered</label>
            </div>
            <button type="submit" id="submit-btn">
                Update Status
            </button>
        </div>
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

function createDeliveryDiv(order) {
	var code = rtDiv.replace("{{order_id}}", order.order_id);
	code = code.replace("{{canteen_name}}", order.canteen_name);
	code = code.replace("{{customer_name}}", order.customer_name);
	code = code.replace("{{address}}", order.address);
	code = code.replace("{{customer_phone}}", order.customer_phone);
	code = code.replace("{{order['total']}}", order.total);
	code = code.replace("{{order['del_charges']}}", order.del_charges);
	code = code.replace("{{items}}", getItemsCode(order.items));

	return code;
}

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

function openOrder(orderID) {
	highlightOrder(orderID);
	fetch("/viewOrder/" + orderID).then((response) => {
		response.json().then((data) => {
			console.log(data);
			parDiv.innerHTML =
				"<div class='left-div'>" +
				document.getElementsByClassName("left-div")[0].innerHTML +
				"</div>";
			console.log(parDiv);
			parDiv.innerHTML +=
				'<div class="right-div">' + createDeliveryDiv(data) + "</div>";

			var status = data.status;
			parDiv.innerHTML = parDiv.innerHTML.replace("{{status}}", status);

			var radiogroups = document.getElementsByClassName("radio-group");

			var radioBtns = document.querySelectorAll("input[type='radio']");

			console.log(radioBtns);
			let j = 0;
			if (status != 0) {
				for (j = 0; j < status - 1; j++) {
					radioBtns[j].disabled = true;
					radioBtns[j].style.pointerevents = "none";
					radiogroups[j].querySelector("label").style.textDecoration =
						"line-through";
				}
				radioBtns[j].checked = true;
			}

			var submit_btn = document.getElementById("submit-btn");
			submit_btn.addEventListener("click", () => {
				status = updateOnClick();

				fetch(
					"/updateOrder?status=" + status + "&order_id=" + orderID,
					{
						method: "POST",
					}
				).then(window.location.reload());
			});
		});
	});
}

function updateOnClick() {
	console.log("fdfsdf");
	var radioBtns = document.querySelectorAll("input[type='radio']");
	console.log(radioBtns);
	for (let i = 0; i < radioBtns.length; i++) {
		if (radioBtns[i].checked) {
			console.log(i + 1);
			return i + 1;
		}
	}
	console.log(0);
	return 0;
}

firstOrderID = document
	.getElementsByClassName("delivery-item")[0]
	.getAttribute("order");
console.log(firstOrderID);
window.onload = function () {
	openOrder(firstOrderID);
};
