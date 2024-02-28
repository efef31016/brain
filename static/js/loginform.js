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
});