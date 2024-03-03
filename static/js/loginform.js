// 定義和取得裝置ID
function getOrCreateDeviceId() {
    let deviceId = localStorage.getItem('device_id');
    if (!deviceId) {
        deviceId = `device-${Math.random().toString(36).slice(2, 11)}-${new Date().getTime()}`; // 1970年1月1日00:00:00 UTC到目前時間的毫秒數
        localStorage.setItem('device_id', deviceId);
    }
    return deviceId;
}

// 登入使用者的函數
async function loginUser(loginIdentifier, password, deviceId) {
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login_identifier: loginIdentifier, password, device_id: deviceId })
        });
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// 更新頁面回饋資訊的函數
function updateFeedback(message, isSuccess) {
    const feedback = document.getElementById('feedback');
    feedback.textContent = message;
    feedback.style.color = isSuccess ? 'green' : 'red';
}

// 當文件載入完畢時，設定表單提交的監聽器
document.addEventListener('DOMContentLoaded', () => {
    const deviceId = getOrCreateDeviceId();
    const form = document.getElementById('login-form');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const loginIdentifier = document.getElementById('login-identifier').value;
        const password = document.getElementById('password').value;

        try {
            const data = await loginUser(loginIdentifier, password, deviceId);
            if (data.status === "success") {
                localStorage.setItem('access_token', data.access_token); // 儲存token
                window.location.href = '/';
            } else {
                throw new Error(data.message || '登入失敗，請檢查您的使用者名稱或密碼。');
            }
        } catch (error) {
            updateFeedback(error.message, false);
        }
    });

    // 處理「忘記密碼」連結的邏輯
    document.getElementById('reset-password-link').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('reset-password-modal').style.display = 'block';
    });

    // 關閉模態對話框
    document.getElementsByClassName('close-button')[0].addEventListener('click', function() {
        document.getElementById('reset-password-modal').style.display = 'none';
    });

    // 提交「重置密碼」請求
    document.getElementById('submit-reset').addEventListener('click', function() {
        var email = document.getElementById('email-for-reset').value;
        // 傳送電子郵件地址到後端
        fetch('/api/request-reset-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('網路回應不是OK');
            }
            return response.json();
        })
        .then(data => {
            // 使用從後端回傳的訊息更新回饋訊息
            updateFeedback(data.message, true);
        })
        .catch(error => {
            console.error('發送重設密碼請求失敗:', error);
            updateFeedback('發送重設密碼請求失敗，請稍後再試。', false);
        });
   
        // 關閉模態視窗
        document.getElementById('reset-password-modal').style.display = 'none';
   });
});