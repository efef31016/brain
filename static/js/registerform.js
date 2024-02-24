document.addEventListener('DOMContentLoaded', function() {
    const formElement = document.getElementById('main-form');
    const emailButton = document.getElementById('send-verify-email-btn');
    const verifyButton = document.getElementById('verify-email-btn');
    const emailInput = document.getElementById('email');
    const verificationCodeInput = document.getElementById('verification-code');
    const overlay = document.getElementById('overlay');

    // 前端驗證規則
    const rules = [
        {
            field: 'snick',
            test: value => /^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}$/.test(value),
            message: '使用者名稱僅支援1-20位的字母、數字、底線和中文字元。',
        },
        {
            field: 'pwd',
            test: value => value.length >= 8,
            message: '密碼需超過8位數。',
        },
        {
            field: 'confirm-pwd',
            test: value => document.getElementById('pwd').value === value,
            message: '確認密碼必須與密碼相等。',
        },
        {
            field: 'email',
            test: value => /\S+@\S+\.\S+/.test(value),
            message: '電子信箱必須填有效格式。',
        }
    ];

    // 綁定即時驗證邏輯
    rules.forEach(({field, test, message}) => {
        const inputElement = formElement.querySelector(`[name=${field}]`);
        inputElement.addEventListener('input', () => validateField(inputElement, {test, message}));
    });

    function validateField(inputElement, {test, message}, showNotificationNow = true) {
        const isValid = test(inputElement.value);
        inputElement.classList.toggle('error', !isValid);
        if (!isValid && showNotificationNow) {
            showNotification(message, false);
        }
        return isValid;
    }

    function validateForm() {
        const isFormValid = rules.every(({field, test, message}) =>
            validateField(formElement.querySelector(`[name=${field}]`), {test, message}, false)
        );
    
        if (!isFormValid) {
            showNotification('請檢查輸入格式是否錯誤', false);
        }
    
        return isFormValid;
    }

    // 提交表單
    formElement.addEventListener("submit", async function(event) {
        event.preventDefault();
        if (!validateForm()) {
            return;
        }

        overlay.style.display = 'flex';

        // 如果前端驗證通過，則處理後端驗證邏輯
        let formData = new FormData(this);
        fetch("/api/register-submit-form", {
            method: "POST",
            body: formData
        })
        .then(handleResponse)
        .catch(handleError);
    });

    // 負責處理伺服器成功傳回的回應（包括處理業務邏輯錯誤，即雖然請求成功，但業務邏輯上存在錯誤）
    async function handleResponse(response) {
        try {
            const data = await response.json();
            if (!response.ok) {
                throw {isApiError: true, message: data.message};
            }
            await delay(1500);
            overlay.style.display = 'none';
            showNotification(data.message, true);
            await delay(1500);
            window.location.href = '/';
        } catch (error) {
            throw {isApiError: true, message: error.message || "Error processing response."};
        }
    }
    
    // 負責處理請求過程中遇到的異常情況，例如網路錯誤、請求配置錯誤等，以及由 handleResponse 拋出的業務邏輯錯誤
    async function handleError(error) {
        let message = "An error occurred. Please try again.";
        if (error.isApiError && error.message) {
            message = error.message;
        }
        await delay(1000);
        overlay.style.display = 'none';
        showNotification(message, false);
    }

    emailButton.addEventListener('click', function() {
        sendEmailVerification(emailInput.value);
    });

    verifyButton.addEventListener('click', function() {
        verifyEmailCode(emailInput.value, verificationCodeInput.value);
    });

    async function sendEmailVerification(email) {
        if (!validateField(emailInput, rules.find(rule => rule.field === 'email'))) {
            showNotification('請輸入有效的電子郵件地址。', false);
            return;
        }
        var email = document.getElementById('email').value;
        if (email) {
            // 顯示載入提示
            this.textContent = '發送...';
            this.disabled = true; // 停用按鈕
            fetch('/api/send-verification-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => Promise.reject(data.message));
                }
                return response.json();
            })
            .then(data => {
                showNotification(data.message, true); // 顯示成功訊息
                document.getElementById('send-verify-email-btn').style.display = 'none';
                document.getElementById('verification-container').style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification(error); // 使用showNotification顯示錯誤
                this.disabled = false; // 請求失敗後啟用按鈕
                this.textContent = '發送電子郵件';
            });
        } else {
            showNotification('請輸入有效的電子郵件地址。'); // 使用showNotification顯示錯誤
        }
    }

    async function verifyEmailCode(email, code) {
        var email = document.getElementById('email').value;
        var code = document.getElementById('verification-code').value;
        if (code) {
            fetch('/api/verify-email-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email, code: code })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => Promise.reject(data.message));
                }
                return response.json();
            })
            .then(data => {
                showNotification(data.message, true); // 顯示成功訊息
                document.getElementById('verify-email-btn').disabled = true;
                document.getElementById('email-verified-icon').style.display = 'inline';
            })
            .catch(error => {
                showNotification(error, true); // 使用showNotification顯示錯誤
            });
        } else {
            showNotification('請輸入驗證碼。'); // 使用showNotification顯示錯誤
        }
    }

    // 顯示通知
    function showNotification(message, isSuccess) {
        // 首先移除已存在的通知
        document.querySelectorAll('.notification').forEach(notification => {
            notification.remove();
        });
    
 
        const notification = document.createElement("div");
        notification.className = `notification ${isSuccess ? 'notification-success' : 'notification-error'}`;
        notification.textContent = message;
        notification.style.opacity = "1";
        notification.style.transition = "opacity 0.5s ease";
    
        document.body.appendChild(notification);
    
        setTimeout(() => {
            notification.style.opacity = "0";
            notification.addEventListener('transitionend', () => {
                notification.remove();
            });
        }, 3000);
    }

    // 停頓
    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
});