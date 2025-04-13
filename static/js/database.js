let accountsData = []; // Массив для збереження акаунтів
let currentPage = 1;    // Поточна сторінка
let itemsPerPage = 10;  // Кількість акаунтів на сторінці
let currentSort = null; // Поточне сортування

// Функція для отримання даних з бекенду
function fetchAccountsData(sort = null, page = 1) {
    let url = `/api/accounts/?page=${page}&limit=${itemsPerPage}`;
    
    // Додаємо параметри сортування, якщо вони є
    if (sort) {
        url += `&sort=${sort.key}&direction=${sort.direction}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error("Failed to fetch data");
            return response.json();
        })
        .then(data => {
            const newAccounts = data.accounts; // беремо масив з data.accounts
            const totalCount = data.totalCount; // отримуємо загальну кількість
        
            if (page === 1) {
                accountsData = newAccounts;
            } else {
                accountsData = [...accountsData, ...newAccounts];
            }
        
            renderAccounts(accountsData, totalCount); // Передаємо totalCount в рендер
        })        
        .catch(error => {
            console.error("Error fetching accounts data:", error);
        });
}

// Функція для рендерингу акаунтів
function renderAccounts(accounts, totalCount) {
    const container = document.getElementById("accounts-container");

    if (!container) {
        console.error("Container 'accounts-container' not found!");
        return;
    }

    container.innerHTML = "";

    accounts.forEach(account => {
        const accountDiv = document.createElement("div");
        accountDiv.classList.add("account");

        accountDiv.addEventListener("click", () => {
            window.location.href = `${baseAnalysisURL}?name=${encodeURIComponent(account.username)}`;
        });

        accountDiv.innerHTML = `
            <div class="avatar">
                <img src="${account.pic}" alt="${account.username}">
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

    const loadMoreBtn = document.getElementById("load-more-btn");
    if (accounts.length < totalCount) {
        loadMoreBtn.style.display = "block";
    } else {
        loadMoreBtn.style.display = "none";
    }
}

// Обробка завантаження додаткових акаунтів
document.getElementById("load-more-btn").addEventListener("click", () => {
    currentPage += 1;  // Збільшуємо номер сторінки
    fetchAccountsData(currentSort, currentPage);  // Завантажуємо наступну порцію акаунтів
});

// Ініціалізація при завантаженні сторінки
document.addEventListener("DOMContentLoaded", () => {
    fetchAccountsData(); // Початкове завантаження акаунтів

    const filtersBtn = document.getElementById('filters-btn');
    const filterPopup = document.getElementById('filter-popup');
    const applyBtn = document.getElementById('apply-filters');
    const resetBtn = document.getElementById('reset-filters');
    
    // Перемикання видимості попапу
    filtersBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        filterPopup.classList.toggle('active');
    });
    
    // Закриття попапу при кліку поза ним
    filterPopup.addEventListener('click', (e) => {
        if (e.target === filterPopup) {
            filterPopup.classList.remove('active');
        }
    });
    
    // Застосування сортування
    applyBtn.addEventListener('click', () => {
        const selectedSortRadio = document.querySelector('input[name="sort"]:checked');
    
        if (selectedSortRadio && selectedSortRadio.value !== 'none') {
            const [key, direction] = selectedSortRadio.value.split('-');
            currentSort = { key, direction };  // Оновлюємо сортування
            currentPage = 1;  // Скидаємо сторінку на першу
            fetchAccountsData(currentSort, currentPage);  // Перезавантажуємо акаунти
        } else {
            currentSort = null;  // Якщо сортування не вибрано
            currentPage = 1;
            fetchAccountsData();  // Завантажуємо акаунти без сортування
        }
    
        filterPopup.classList.remove('active');
    });
    
    // Скидання сортування
    resetBtn.addEventListener('click', () => {
        document.querySelector('input[name="sort"][value="none"]').checked = true;
        currentSort = null;  // Скидаємо сортування
        currentPage = 1;  // Скидаємо сторінку на першу
        fetchAccountsData();  // Завантажуємо акаунти без сортування
    });
    
    // Закриття попапу при натисканні клавіші Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && filterPopup.classList.contains('active')) {
            filterPopup.classList.remove('active');
        }
    });
});
