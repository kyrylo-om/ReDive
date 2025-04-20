let accountsData = [];
let currentPage = 1;
let itemsPerPage = 10;
let currentSort = null;

function fetchAccountsData(sort = null, page = 1) {
    let url = `/api/accounts/?page=${page}&limit=${itemsPerPage}`;

    if (sort) {
        url += `&sort=${sort.key}&direction=${sort.direction}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error("Failed to fetch data");
            return response.json();
        })
        .then(data => {
            const newAccounts = data.accounts;
            const totalCount = data.totalCount;
        
            if (page === 1) {
                accountsData = newAccounts;
            } else {
                accountsData = [...accountsData, ...newAccounts];
            }
        
            renderAccounts(accountsData, totalCount);
        })        
        .catch(error => {
            console.error("Error fetching accounts data:", error);
        });
}

function renderAccounts(accounts, totalCount) {
    const container = document.getElementById("accounts-container");
    const analysisUrl = container.getAttribute("data-analysis-url");

    if (!container) {
        console.error("Container 'accounts-container' not found!");
        return;
    }

    container.innerHTML = "";

    accounts.forEach(account => {
        const accountDiv = document.createElement("div");
        accountDiv.classList.add("account");

        accountDiv.addEventListener("click", () => {
            window.location.href = `${analysisUrl}?query=${encodeURIComponent(account.username)}`;
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

document.getElementById("load-more-btn").addEventListener("click", () => {
    currentPage += 1;
    fetchAccountsData(currentSort, currentPage);
});

document.addEventListener("DOMContentLoaded", () => {
    fetchAccountsData();

    const filtersBtn = document.getElementById('filters-btn');
    const filterPopup = document.getElementById('filter-popup');
    const applyBtn = document.getElementById('apply-filters');
    const resetBtn = document.getElementById('reset-filters');

    filtersBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        filterPopup.classList.toggle('active');
    });

    filterPopup.addEventListener('click', (e) => {
        if (e.target === filterPopup) {
            filterPopup.classList.remove('active');
        }
    });

    applyBtn.addEventListener('click', () => {
        const selectedSortRadio = document.querySelector('input[name="sort"]:checked');
    
        if (selectedSortRadio && selectedSortRadio.value !== 'none') {
            const [key, direction] = selectedSortRadio.value.split('-');
            currentSort = { key, direction };
            currentPage = 1;
            fetchAccountsData(currentSort, currentPage);
        } else {
            currentSort = null;
            currentPage = 1;
            fetchAccountsData();
        }
    
        filterPopup.classList.remove('active');
    });

    resetBtn.addEventListener('click', () => {
        document.querySelector('input[name="sort"][value="none"]').checked = true;
        currentSort = null;
        currentPage = 1;
        fetchAccountsData();
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && filterPopup.classList.contains('active')) {
            filterPopup.classList.remove('active');
        }
    });

    const searchBtn = document.querySelector('.search-btn');
    const searchInput = document.querySelector('.searchbar input[name="query"]');

    searchBtn.addEventListener('click', (e) => {
        e.preventDefault();

        const query = searchInput.value.trim();

        if (!query) return;

        const url = `/api/accounts/search/?query=${encodeURIComponent(query)}&limit=${itemsPerPage}&page=1`;

        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error("Search request failed");
                return response.json();
            })
            .then(data => {
                const foundAccounts = data.accounts || [];
                const totalCount = data.totalCount || 0;

                accountsData = foundAccounts;
                currentPage = 1;
                renderAccounts(accountsData, totalCount);
            })
            .catch(error => {
                console.error("Search error:", error);
            });
    });
});
