document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    initializeUI(token);

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }

    document.getElementById('debate-topics').addEventListener('change', handleTopicChange);
});

function initializeUI(token) {
    const logoutBtn = document.getElementById('logoutBtn');
    const debateBtn = document.querySelector('.debate-btn');
    const registerBtn = document.querySelector('.register-btn');
    const loginBtn = document.querySelector('.login-btn');
    const toggleChartBtn = document.getElementById('toggleChartBtn');
    const dataChartContainer = document.getElementById('dataChartContainer'); // 確保有這個ID

    // 登入後的UI調整
    if (token) {
        document.getElementById('userNavbar').style.display = 'flex';
        logoutBtn.style.display = 'block';
        debateBtn.style.display = 'inline-block';
        registerBtn.style.display = 'none';
        loginBtn.style.display = 'none';
        toggleChartBtn.style.display = 'block';
    } else {
        // 登入前的UI調整
        updateUIForLoggedOut(false); // 傳入false以避免重新導向
    }

    if (toggleChartBtn) {
        toggleChartBtn.addEventListener('click', () => {
            const isHidden = dataChartContainer.style.display === 'none';
            dataChartContainer.style.display = isHidden ? 'block' : 'none';
            toggleChartBtn.textContent = isHidden ? '隱藏 資料圖表' : '展示 資料圖表';
        });
    }
}

async function logout() {
    const token = localStorage.getItem('access_token'); // 假設已經儲存
    const deviceId = localStorage.getItem('device_id'); // 假設已經儲存
    try {
        const response = await fetch('/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ device_id: deviceId })
        });

        const data = await response.json();
        if (data.status === "success") {
            localStorage.removeItem('access_token');
            localStorage.removeItem('device_id');
            updateUIForLoggedOut(true); // 傳入true以重定向
        } else {
            console.error('Logout failed:', data.message);
        }
    } catch (error) {
        console.error('Logout error:', error);
    }
}

function updateUIForLoggedOut(shouldRedirect = true) {
    // UI調整回未登入狀態
    document.getElementById('userNavbar').style.display = 'none';
    document.querySelector('.debate-btn').style.display = 'none';
    document.querySelector('.register-btn').style.display = 'inline-block';
    document.querySelector('.login-btn').style.display = 'inline-block';
    document.getElementById('toggleChartBtn').style.display = 'none';
    document.getElementById('dataChartContainer').style.display = 'none';

    if (shouldRedirect) {
        window.location.href = '/';
    }
}

function handleTopicChange() {
    const selectElement = document.getElementById('debate-topics');
    const topicId = selectElement.value;
    if (!topicId) return;

    fetch(`/api/topic-info?topic_id=${topicId}`)
        .then(response => response.json())
        .then(data => {
            document.querySelector('h1').textContent = data.page_title;
            document.querySelector('p').textContent = data.welcome_message;
        })
        .catch(error => console.error("Error:", error));
}   