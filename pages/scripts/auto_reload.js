function reloadPage() {
    setInterval(function() {
        location.reload();
    }, 15000);
}
document.addEventListener("DOMContentLoaded", reloadPage);