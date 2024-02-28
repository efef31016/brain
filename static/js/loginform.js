document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    const feedback = document.getElementById('feedback');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const login_identifier = document.getElementById('login-identifier').value;
        const password = document.getElementById('password').value;
       
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ login_identifier, password })
            });
            
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || '請檢查 API 端口');
            }

            // 處理登入成功邏輯
            if (data.status === "success") {
                feedback.textContent = data.message; // 使用後端回傳的成功訊息
                feedback.style.color = 'green';
                localStorage.setItem('token', data.token); // 儲存token
                window.location.href = '/';
            } else {
                feedback.textContent = data.message || '登入失敗，請檢查您的使用者名稱或密碼。 ';
                feedback.style.color = 'red';
            }
        } catch (error) {
            feedback.textContent = error.message;
            feedback.style.color = 'red';
        }
    });
});