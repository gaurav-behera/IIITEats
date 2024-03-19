const profile = document.querySelector(".profile");
const profileInfo = document.querySelector(".profile-info");

profile.addEventListener("mousein", () => {
	// profileInfo.style.opacity = "1";
	// setTimeout(function () {
	// 	profileInfo.style.opacity = "1.0";
	// }, 500);
	profileInfo.style.opacity = "1.0";
	profileInfo.style.pointerEvents = "auto";
});

profileInfo.addEventListener("mouseout", () => {
	// setTimeout(function () {
	// 	profileInfo.style.opacity = "0.0";
	// }, 500);
	profileInfo.style.opacity = "0.0";
	profileInfo.style.pointerEvents = "none";
});
