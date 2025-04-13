document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const input = form.querySelector("input[name='query']");
    const searchBtn = form.querySelector(".search-btn");

    const errorMsg = document.createElement("p");
    errorMsg.className = "error-message";
    errorMsg.style.color = "red";
    errorMsg.style.marginTop = "10px";
    form.appendChild(errorMsg);

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
                    errorMsg.textContent = `User "${username}" does not exist.`;
                }
            })
            .catch(err => {
                console.error("Error:", err);
                errorMsg.textContent = "Server error. :)";
            });
    });
});
