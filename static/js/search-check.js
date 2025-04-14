document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const input = form.querySelector("input[name='query']");
    const searchBtn = form.querySelector(".search-btn");

    form.addEventListener("submit", function(e) {
        e.preventDefault();
    
        const username = input.value.trim();
        if (!username) return;
    
        fetch(`/api/check-user/?username=${encodeURIComponent(username)}`)
            .then(res => res.json())
            .then(data => {
                if (data.exists) {
                    window.location.href = `/user/?query=${encodeURIComponent(username)}`;
                } else {
                    showToast(`User "${username}" does not exist.`);
                }
            });
    });
});

function showToast(message) {
    const toastContainer = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000); // зникне через 3 секунди
}
