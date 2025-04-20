document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const input = form.querySelector("input[name='query']");
    const loadingPopup = document.getElementById("loading-popup");
    const loadingText = loadingPopup.querySelector("p");

    const loadingMessages = [
        "Reading user’s aura...",
        "Calculating karma balance...",
        "Checking last seen status...",
        "Decrypting personality matrix...",
        "Peeking into digital soul...",
        "Decoding username DNA...",
        "Running vibe check...",
        "Consulting the Oracle...",
        "Summoning data from the void...",
        "Analyzing coffee consumption patterns..."
    ];

    window.addEventListener("pageshow", () => {
        loadingPopup.classList.remove('active');
    });

    form.addEventListener("submit", function(e) {
        e.preventDefault();
    
        const username = input.value.trim();
        if (!username) return;

        fetch(`/api/check-user/?username=${encodeURIComponent(username)}`)
            .then(res => res.json())
            .then(data => {
                if (data.exists) {
                    // Вставляємо випадковий текст
                    const randomIndex = Math.floor(Math.random() * loadingMessages.length);
                    loadingText.textContent = loadingMessages[randomIndex];

                    loadingPopup.classList.add('active');
                    window.location.href = `/user/?query=${encodeURIComponent(username)}`;
                } else {
                    showToast(`User "${username}" does not exist.`);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                loadingPopup.classList.remove('active');
                showToast("An error occurred. Please try again.");
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
        }, 3000);
    }
});
