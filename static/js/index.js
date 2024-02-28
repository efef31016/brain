document.addEventListener('DOMContentLoaded', () => {
    // 登入狀態的檢查
    const token = localStorage.getItem('token');

    const logoutBtn = document.getElementById('logoutBtn');
    const debateBtn = document.querySelector('.debate-btn');
    const registerBtn = document.querySelector('.register-btn');
    const loginBtn = document.querySelector('.login-btn');
    const toggleChartBtn = document.getElementById('toggleChartBtn');

    console.log(logoutBtn);

    if (token) {
        // 登入後的UI調整
        document.getElementById('userNavbar').style.display = 'flex';
        logoutBtn.style.display = 'block'; // 顯示登出按鈕
        debateBtn.style.display = 'inline-block'; // 顯示加入投票或辯論按鈕
        registerBtn.style.display = 'none'; // 隱藏登錄按鈕
        loginBtn.style.display = 'none'; // 隱藏登入按鈕
        toggleChartBtn.style.display = 'block'; // 顯示資料圖表顯示/隱藏按鈕
    } else {
        // 登入前的UI調整
        document.getElementById('userNavbar').style.display = 'none';
        dataChartContainer.style.display = 'none';
        if (toggleChartBtn) toggleChartBtn.style.display = 'none'; // 選擇是否要查看最受歡迎的想法
    }

    // 控制資料圖表顯示/隱藏的按鈕邏輯
    if (toggleChartBtn) { // 確保按鈕存在
        toggleChartBtn.addEventListener('click', () => {
            if (dataChartContainer.style.display === 'none') {
                dataChartContainer.style.display = 'block';
                toggleChartBtn.textContent = '隱藏 資料圖表';
            } else {
                dataChartContainer.style.display = 'none';
                toggleChartBtn.textContent = '展示 資料圖表';
            }
        });
    }

    document.getElementById('debate-topics').addEventListener('change', handleTopicChange);
});

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
