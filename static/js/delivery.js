function takeUpOrder(orderId) {
    console.log(orderId);
	fetch("/takeUpOrder/" + orderId, {
		method: "POST",
	}).then((res) => {
		if (res.status === 200) {
			console.log("takeUpOrder success");
			window.location.href = "/yourDeliveries";
		}
	});
}
