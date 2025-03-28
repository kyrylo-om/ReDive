const accountsData = [
    { username: "user123", posts: "512", comments: "246", bot_percentage: "8" },
    { username: "superpider", posts: "47", comments: "5", bot_percentage: "55" },
    { username: "ke1roo", posts: "11", comments: "52", bot_percentage: "81" },
    { username: "ke1roo", posts: "11", comments: "52", bot_percentage: "81" },
    { username: "ke1roo", posts: "11", comments: "52", bot_percentage: "81" },
    { username: "ke1roo", posts: "11", comments: "52", bot_percentage: "81" },
    { username: "ke1roo", posts: "11", comments: "52", bot_percentage: "81" }
];

function renderAccounts(accounts) {
    const container = document.getElementById("accounts-container");
    
    // Перевірка, чи контейнер існує
    if (!container) {
        console.error("Контейнер 'accounts-container' не знайдено!");
        return;
    }

    container.innerHTML = "";

    accounts.forEach(account => {
        const accountDiv = document.createElement("div");
        accountDiv.classList.add("account");
        accountDiv.innerHTML = `
            <div class="avatar">
                <img src="https://i.pravatar.cc/50?u=${account.username}" alt="${account.username}">
            </div>
            <div class="account-content">
                <div class="username">${account.username}</div>
                <div class="stats">
                    <p>Posts: ${account.posts}</p>
                    <p>Comments: ${account.comments}</p>
                </div>
                <p class="bot-percentage">${account.bot_percentage}%</p>
            </div>
        `;
        container.appendChild(accountDiv);
    });
}

// Запускаємо рендеринг після завантаження сторінки
document.addEventListener("DOMContentLoaded", () => {
    renderAccounts(accountsData);
});
