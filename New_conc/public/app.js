// Frontend JavaScript for AI Financial Relationship Manager

// API Configuration
const API_BASE_URL = window.location.origin;

// State
let currentSection = 'overview';
let isLoading = false;

// DOM Elements
const navItems = document.querySelectorAll('.nav-item');
const contentSections = document.querySelectorAll('.content-section');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const clearChatBtn = document.getElementById('clear-chat');
const quickPrompts = document.querySelectorAll('.quick-prompt');

// Navigation
navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const section = item.dataset.section;
        switchSection(section);
    });
});

function switchSection(section) {
    // Update nav active state
    navItems.forEach(item => {
        item.classList.toggle('active', item.dataset.section === section);
    });
    
    // Update content sections
    contentSections.forEach(content => {
        content.classList.toggle('active', content.id === `${section}-section`);
    });
    
    // Update page title
    const titles = {
        overview: 'Financial Overview',
        portfolio: 'Portfolio Holdings',
        transactions: 'Transaction History',
        chat: 'AI Financial Advisor',
        goals: 'Financial Goals'
    };
    document.querySelector('.page-title').textContent = titles[section] || 'Dashboard';
    
    currentSection = section;
}

// Chat Functionality
async function sendMessage(message) {
    if (!message.trim() || isLoading) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';
    
    // Show loading indicator
    isLoading = true;
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<span>Thinking...</span>';
    
    const loadingId = addMessage('Analyzing your request...', 'bot', true);
    
    try {
        // Call chat API
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get response from AI');
        }
        
        const data = await response.json();
        
        // Remove loading message
        document.getElementById(loadingId)?.remove();
        
        // Add AI response
        addMessage(data.response, 'bot');
        
    } catch (error) {
        console.error('Error sending message:', error);
        document.getElementById(loadingId)?.remove();
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
    } finally {
        isLoading = false;
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<span>Send</span>';
    }
}

function addMessage(text, sender, isLoading = false) {
    const messageId = `msg-${Date.now()}`;
    const messageEl = document.createElement('div');
    messageEl.id = messageId;
    messageEl.className = `message ${sender}-message`;
    
    const avatar = sender === 'bot' ? '🤖' : '👤';
    const author = sender === 'bot' ? 'FinanceAI' : 'You';
    
    messageEl.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-author">${author}</div>
            <div class="message-text">${formatMessage(text)}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageEl);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageId;
}

function formatMessage(text) {
    // Convert line breaks and preserve formatting
    return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');
}

// Event Listeners
sendBtn.addEventListener('click', () => {
    sendMessage(chatInput.value);
});

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage(chatInput.value);
    }
});

// Auto-resize textarea
chatInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Quick prompts
quickPrompts.forEach(prompt => {
    prompt.addEventListener('click', () => {
        const message = prompt.dataset.prompt;
        chatInput.value = message;
        sendMessage(message);
    });
});

// Clear chat
clearChatBtn.addEventListener('click', async () => {
    if (confirm('Are you sure you want to clear the chat history?')) {
        try {
            await fetch(`${API_BASE_URL}/api/reset`, { method: 'POST' });
            chatMessages.innerHTML = `
                <div class="message bot-message">
                    <div class="message-avatar">🤖</div>
                    <div class="message-content">
                        <div class="message-author">FinanceAI</div>
                        <div class="message-text">
                            Chat history cleared! How can I help you today?
                        </div>
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Error clearing chat:', error);
        }
    }
});

// Load initial data (simulated - in production would fetch from backend)
function loadDashboardData() {
    // This is simplified - in production, you'd fetch this from the backend
    // which would call the agent tools
    
    // Set some initial values
    document.getElementById('total-portfolio').textContent = '$357,240';
    document.getElementById('total-gain').textContent = '+$38,540';
    document.getElementById('monthly-spending').textContent = '$4,850';
    document.getElementById('available-cash').textContent = '$60,500';
}

// Mock Portfolio Data Loading
function loadPortfolioData() {
    const stocksTable = document.getElementById('stocks-table');
    const fundsTable = document.getElementById('funds-table');
    
    // Mock stock data
    const stocks = [
        { ticker: 'AAPL', company: 'Apple Inc.', shares: 50, avgCost: 150.25, current: 189.50, value: 9475, gain: 1962.50 },
        { ticker: 'MSFT', company: 'Microsoft Corp.', shares: 30, avgCost: 320.50, current: 378.85, value: 11365.50, gain: 1750.50 },
        { ticker: 'GOOGL', company: 'Alphabet Inc.', shares: 25, avgCost: 125.75, current: 142.65, value: 3566.25, gain: 422.50 },
        { ticker: 'JNJ', company: 'Johnson & Johnson', shares: 40, avgCost: 155.00, current: 158.75, value: 6350, gain: 150 },
        { ticker: 'V', company: 'Visa Inc.', shares: 20, avgCost: 245.30, current: 268.90, value: 5378, gain: 472 },
        { ticker: 'TSLA', company: 'Tesla Inc.', shares: 15, avgCost: 245.60, current: 242.84, value: 3642.60, gain: -41.40 }
    ];
    
    stocksTable.innerHTML = stocks.map(stock => {
        const gainClass = stock.gain >= 0 ? 'positive' : 'negative';
        const gainSymbol = stock.gain >= 0 ? '+' : '';
        return `
            <tr>
                <td><strong>${stock.ticker}</strong></td>
                <td>${stock.company}</td>
                <td>${stock.shares}</td>
                <td>$${stock.avgCost.toFixed(2)}</td>
                <td>$${stock.current.toFixed(2)}</td>
                <td>$${stock.value.toLocaleString()}</td>
                <td class="stat-change ${gainClass}">${gainSymbol}$${stock.gain.toFixed(2)}</td>
            </tr>
        `;
    }).join('');
    
    // Mock mutual fund data
    const funds = [
        { name: 'Vanguard Total Stock Market', ticker: 'VTSAX', units: 180, purchaseNAV: 110.50, currentNAV: 123.45, value: 22221, gain: 2331 },
        { name: 'Fidelity 500 Index Fund', ticker: 'FXAIX', units: 120, purchaseNAV: 165.25, currentNAV: 178.92, value: 21470.40, gain: 1640.40 },
        { name: 'Vanguard Emerging Markets', ticker: 'VEIEX', units: 95, purchaseNAV: 32.80, currentNAV: 34.15, value: 3244.25, gain: 128.25 }
    ];
    
    fundsTable.innerHTML = funds.map(fund => {
        const gainClass = fund.gain >= 0 ? 'positive' : 'negative';
        const gainSymbol = fund.gain >= 0 ? '+' : '';
        return `
            <tr>
                <td>${fund.name}</td>
                <td><strong>${fund.ticker}</strong></td>
                <td>${fund.units}</td>
                <td>$${fund.purchaseNAV.toFixed(2)}</td>
                <td>$${fund.currentNAV.toFixed(2)}</td>
                <td>$${fund.value.toLocaleString()}</td>
                <td class="stat-change ${gainClass}">${gainSymbol}$${fund.gain.toFixed(2)}</td>
            </tr>
        `;
    }).join('');
}

// Mock Transactions Data
function loadTransactionsData() {
    const transactionsTable = document.getElementById('transactions-table');
    
    const transactions = [
        { date: '2025-11-20', merchant: 'Whole Foods', category: 'Groceries', amount: -125.50, type: 'debit' },
        { date: '2025-11-19', merchant: 'Shell Gas', category: 'Transportation', amount: -52.30, type: 'debit' },
        { date: '2025-11-18', merchant: 'Netflix', category: 'Entertainment', amount: -15.99, type: 'debit' },
        { date: '2025-11-17', merchant: 'Chipotle', category: 'Dining', amount: -23.75, type: 'debit' },
        { date: '2025-11-16', merchant: 'Amazon', category: 'Shopping', amount: -89.99, type: 'debit' },
        { date: '2025-11-15', merchant: 'Direct Deposit', category: 'Income', amount: 8500.00, type: 'credit' },
        { date: '2025-11-14', merchant: 'Starbucks', category: 'Dining', amount: -12.50, type: 'debit' },
        { date: '2025-11-13', merchant: 'Electric Company', category: 'Utilities', amount: -145.80, type: 'debit' },
        { date: '2025-11-12', merchant: 'Target', category: 'Shopping', amount: -67.45, type: 'debit' },
        { date: '2025-11-11', merchant: 'Stock Purchase - AAPL', category: 'Investment', amount: -1500.00, type: 'investment' }
    ];
    
    transactionsTable.innerHTML = transactions.map(txn => {
        const amountClass = txn.amount >= 0 ? 'positive' : 'negative';
        const amountSymbol = txn.amount >= 0 ? '+' : '';
        return `
            <tr>
                <td>${txn.date}</td>
                <td>${txn.merchant}</td>
                <td><span class="category-badge">${txn.category}</span></td>
                <td class="stat-change ${amountClass}">${amountSymbol}$${Math.abs(txn.amount).toFixed(2)}</td>
                <td>${txn.type}</td>
            </tr>
        `;
    }).join('');
}

// Initialize after DOM loads
document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
    loadPortfolioData();
    loadTransactionsData();
    
    // Set up insight card click handlers
    document.querySelectorAll('.insight-card .btn-link').forEach(btn => {
        btn.addEventListener('click', () => {
            switchSection('chat');
        });
    });
});

// Handle window resize for responsive design
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        // Handle responsive adjustments if needed
    }, 250);
});
