let currentPage = 1;
let totalPages = 1;
let itemsPerPage = 10;
let otpTimer;
const OTP_VALIDITY = 60;

async function generateOTP() {
    const aadharNumber = document.getElementById('aadharNumber').value;
    if (!aadharNumber || aadharNumber.length !== 12) {
        showResult('Please enter a valid 12-digit Aadhaar number', false);
        return;
    }
    
    try {
        const response = await fetch('/generate-otp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ aadhar_number: aadharNumber })
        });
        
        const data = await response.json();
        if (data.success) {
            document.getElementById('otpSection').style.display = 'block';
            document.getElementById('otpTimer').className = 'text-info';
            showResult(`OTP generated: ${data.otp}`, true);
            startOTPTimer();
        } else {
            showResult(data.error, false);
        }
    } catch (error) {
        showResult('Error generating OTP', false);
    }
}

async function verifyOTP() {
    const aadharNumber = document.getElementById('aadharNumber').value;
    const otp = document.getElementById('otp').value;
    const transactionType = document.getElementById('transactionType').value;
    
    try {
        const response = await fetch('/verify-transaction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                aadhar_number: aadharNumber,
                otp: otp,
                transaction_type: transactionType
            })
        });
        
        const data = await response.json();
        showResult(data.message, data.success);
    } catch (error) {
        showResult('Error verifying transaction', false);
    }
}

async function searchHistory() {
    const aadharNumber = document.getElementById('searchAadhar').value;
    if (!aadharNumber || aadharNumber.length !== 12) {
        showResult('Please enter a valid 12-digit Aadhaar number', false);
        return;
    }
    
    try {
        const response = await fetch(`/transaction-history/${aadharNumber}`);
        const data = await response.json();
        
        const historyContent = document.getElementById('historyContent');
        if (data.transactions.length === 0) {
            historyContent.innerHTML = '<div class="alert alert-info">No transactions found</div>';
            return;
        }
        
        historyContent.innerHTML = data.transactions.map(transaction => `
            <div class="card mb-2">
                <div class="card-body">
                    <h5 class="card-title">${transaction.transaction_type}</h5>
                    <p class="card-text">
                        <strong>Status:</strong> ${transaction.verification_status}<br>
                        <strong>Timestamp:</strong> ${transaction.timestamp}
                    </p>
                </div>
            </div>
        `).join('');
    } catch (error) {
        showResult('Error fetching transaction history', false);
    }
}

function showResult(message, success) {
    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'block';
    resultDiv.className = `alert ${success ? 'alert-success' : 'alert-danger'}`;
    resultDiv.textContent = message;
}

async function searchHistory(page = 1) {
    const aadharNumber = document.getElementById('searchAadhar').value;
    if (!aadharNumber || aadharNumber.length !== 12) {
        showResult('Please enter a valid 12-digit Aadhaar number', false);
        return;
    }
    
    const filterType = document.getElementById('filterType').value;
    const sortBy = document.getElementById('sortBy').value;
    const sortOrder = document.getElementById('sortOrder').value;
    
    try {
        const response = await fetch(
            `/transaction-history/${aadharNumber}?page=${page}&per_page=${itemsPerPage}&sort_by=${sortBy}&sort_order=${sortOrder}&filter_type=${filterType}`
        );
        const data = await response.json();
        
        currentPage = data.current_page;
        totalPages = data.total_pages;
        
        updatePagination(data.total_items);
        displayTransactions(data.transactions);
    } catch (error) {
        showResult('Error fetching transaction history', false);
    }
}

function displayTransactions(transactions) {
    const historyContent = document.getElementById('historyContent');
    if (transactions.length === 0) {
        historyContent.innerHTML = '<div class="alert alert-info">No transactions found</div>';
        return;
    }
    
    historyContent.innerHTML = transactions.map(transaction => `
        <div class="card mb-2">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        <h5 class="card-title">${transaction.transaction_type.replace(/_/g, ' ')}</h5>
                        <span class="badge ${getStatusBadgeClass(transaction.verification_status)}">
                            ${transaction.verification_status}
                        </span>
                    </div>
                    <div class="col-md-8">
                        <p class="card-text">
                            <strong>Timestamp:</strong> ${formatDate(transaction.timestamp)}<br>
                            <strong>Transaction ID:</strong> ${transaction.hash || 'N/A'}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function updatePagination(totalItems) {
    const startItem = ((currentPage - 1) * itemsPerPage) + 1;
    const endItem = Math.min(currentPage * itemsPerPage, totalItems);
    
    document.getElementById('showingRange').textContent = `${startItem}-${endItem}`;
    document.getElementById('totalItems').textContent = totalItems;
    document.getElementById('pageInfo').textContent = `Page ${currentPage} of ${totalPages}`;
    
    document.getElementById('prevPage').disabled = currentPage === 1;
    document.getElementById('nextPage').disabled = currentPage === totalPages;
}

function changePage(direction) {
    if (direction === 'prev' && currentPage > 1) {
        searchHistory(currentPage - 1);
    } else if (direction === 'next' && currentPage < totalPages) {
        searchHistory(currentPage + 1);
    }
}

function getStatusBadgeClass(status) {
    switch (status) {
        case 'VERIFIED':
            return 'bg-success';
        case 'PENDING':
            return 'bg-warning';
        case 'FAILED':
            return 'bg-danger';
        default:
            return 'bg-secondary';
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeToggleIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeToggleIcon(newTheme);
}

function updateThemeToggleIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = theme === 'light' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
    }
}

document.addEventListener('DOMContentLoaded', initializeTheme);

function startOTPTimer() {
    let timeLeft = OTP_VALIDITY;
    const timerDisplay = document.getElementById('otpTimer');
    
    clearInterval(otpTimer);
    
    timerDisplay.style.display = 'block';
    
    otpTimer = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = `OTP expires in: ${timeLeft} seconds`;
        
        if (timeLeft <= 0) {
            clearInterval(otpTimer);
            timerDisplay.textContent = 'OTP expired. Please generate a new OTP';
            timerDisplay.className = 'text-danger';
            // Hide OTP input section
            document.getElementById('otpSection').style.display = 'none';
        }
    }, 1000);
}