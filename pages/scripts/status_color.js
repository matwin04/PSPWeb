// status_color.js

document.addEventListener("DOMContentLoaded", function() {
    var statusElements = document.querySelectorAll('[id^="status"]');
    statusElements.forEach(function(element) {
        if (element.textContent.trim() === "online") {
            element.classList.add("online");
        } else {
            element.classList.add("offline");
        }
    });
});
