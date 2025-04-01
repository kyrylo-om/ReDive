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

// Filter popup functionality
document.addEventListener('DOMContentLoaded', () => {
    const filtersBtn = document.getElementById('filters-btn');
    const filterPopup = document.getElementById('filter-popup');
    const applyBtn = document.getElementById('apply-filters');
    const resetBtn = document.getElementById('reset-filters');
    
    // Toggle popup visibility
    filtersBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent immediate close when clicking button
        filterPopup.classList.toggle('active');
    });
    
    // Close popup when clicking outside
    filterPopup.addEventListener('click', (e) => {
        if (e.target === filterPopup) {
            filterPopup.classList.remove('active');
        }
    });
    
    // Apply filters
    applyBtn.addEventListener('click', () => {
        const selectedFilters = [];
        document.querySelectorAll('input[name="filter"]:checked').forEach(checkbox => {
            selectedFilters.push(checkbox.value);
        });
        
        // Here you would implement your actual filtering logic
        console.log('Applied filters:', selectedFilters);
        filterPopup.classList.remove('active');
        
        // Example: filterAccounts(selectedFilters);
    });
    
    // Reset filters
    resetBtn.addEventListener('click', () => {
        document.querySelectorAll('input[name="filter"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        // Here you would reset your filtered view
        console.log('Filters reset');
        // Example: resetAccountFilters();
    });
    
    // Close with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && filterPopup.classList.contains('active')) {
            filterPopup.classList.remove('active');
        }
    });
});
