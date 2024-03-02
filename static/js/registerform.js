document.addEventListener('DOMContentLoaded', function() {
    const formElement = document.getElementById('main-form');
    const emailButton = document.getElementById('send-verify-email-btn');
    const verifyButton = document.getElementById('verify-email-btn');
    const emailInput = document.getElementById('email');
    const verificationCodeInput = document.getElementById('verification-code');
    const overlayEmail = document.getElementById('overlay-email');
    const overlayRegister = document.getElementById('overlay-register');
    
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

        overlayRegister.style.display = 'flex';
        animateDots('loadingMessage-register');

        // 如果前端驗證通過，則處理後端驗證邏輯
        let formData = new FormData(this);
        fetch("/api/register-submit-form", {
            method: "POST",
            body: formData
        })
        .then(handleResponse)
        .catch(handleError)
        .finally(() => {
            overlayRegister.style.display = 'none'; // 隱藏覆蓋層
        });
    });

    // 負責處理伺服器成功傳回的回應（包括處理業務邏輯錯誤，即雖然請求成功，但業務邏輯上存在錯誤）
    async function handleResponse(response) {
        try {
            const data = await response.json();
            if (!response.ok) {
                throw {isApiError: true, message: data.message};
            }
            overlayRegister.style.display = 'none';
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
        overlayRegister.style.display = 'none';
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
            overlayEmail.style.display = 'flex';
            const emailAnimationInterval = animateDots('loadingMessage-email');
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
                document.getElementById('email-verified-icon').textContent = '...';
                document.getElementById('email-verified-icon').style.color = 'orange';
                document.getElementById('send-verify-email-btn').style.display = 'none';
                document.getElementById('verification-container').style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification(error); // 使用showNotification顯示錯誤
                this.disabled = false; // 請求失敗後啟用按鈕
                this.textContent = '發送電子郵件';
            })
            .finally(() => {
                clearInterval(emailAnimationInterval);
                overlayEmail.style.display = 'none';
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
                document.getElementById('email-verified-icon').textContent = '✔';
                document.getElementById('email-verified-icon').style.color = 'green';
                document.getElementById('verify-email-btn').disabled = true;
            })
            .catch(error => {
                showNotification(error, false); // 使用showNotification顯示錯誤
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

function animateDots(elementId) {
    let dotCount = 0;
    const maxDots = 3;
    const intervalId = setInterval(() => {
        const element = document.getElementById(elementId);
        if (!element) {
            clearInterval(intervalId); // 如果元素不存在，則停止動畫
            return;
        }

        const baseText = element.textContent.replace(/\.+$/, ''); // 移除末端的點
        dotCount = (dotCount % maxDots) + 1; // 更新點的數量
        const newText = baseText + '.'.repeat(dotCount); // 建立新文字
        element.textContent = newText; // 更新元素的文本
    }, 500); // 每500毫秒更新一次

    return intervalId; // 傳回定時器ID以便於後續可以清除定時器
}