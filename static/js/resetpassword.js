document.addEventListener('DOMContentLoaded', function() {
    const formElement = document.getElementById('resetpassword-form');
    const submitButton = document.querySelector('.submit-btn'); // 取得提交按鈕
    const feedbackElement = document.getElementById('feedback'); // 取得回饋資訊元素
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    document.getElementById('token').value = token;

    formElement.addEventListener('submit', async function(e) {
        e.preventDefault(); // 阻止表單的預設提交行為

        const newPassword = document.getElementById('new_password').value;
        const confirmedNewPassword = document.getElementById('confirmed_new_password').value;

        // 驗證新密碼的長度
        if (newPassword.length < 8) {
            updateFeedback('新的密碼需超過8位數。', false);
            return;
        }

        // 驗證兩次輸入的密碼是否匹配
        if (newPassword !== confirmedNewPassword) {
            updateFeedback('確認密碼必須與密碼相等。', false);
            return;
        }

        // 停用提交按鈕以防止重複提交
        submitButton.disabled = true;

        try {
            const response = await fetch('/api/reset-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    token: token,
                    new_password: newPassword
                })
            });
            const data = await response.json();

            if (response.ok) {
                updateFeedback(data.message, true);
                setTimeout(() => {
                    window.location.href = '/login-form'; // 成功後跳到登入頁面
                }, 1500);
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            updateFeedback(error.message, false);
            submitButton.disabled = false; // 請求失敗後重新啟用按鈕
        }
    });

    function updateFeedback(message, isSuccess) {
        feedbackElement.textContent = message;
        feedbackElement.style.color = isSuccess ? 'green' : 'red';
    }
});