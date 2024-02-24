document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    const feedback = document.getElementById('feedback');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const loginIdentifier = document.getElementById('login-identifier').value;
        const password = document.getElementById('password').value;
       
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ loginIdentifier, password })
            });
            
            console.log(response)
            if (!response.ok) {
                throw new Error('登入失敗，請檢查您的使用者名稱或密碼。');
            }

            const data = await response.json();
            // 處理登入成功邏輯，例如跳到首頁
            feedback.textContent = '登入成功，正在跳轉...';
            feedback.style.color = 'green';
            // window.location.href = '/home'; // 實際項目使用
        } catch (error) {
            feedback.textContent = error.message;
            feedback.style.color = 'red';
        }
    });
});