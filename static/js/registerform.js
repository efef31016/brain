document.getElementById('send-verify-email-btn').addEventListener('click', function() {
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
                return response.json().then(data => Promise.reject(data.error));
            }
            return response.json();
        })
        .then(data => {
            showNotification(data.message); // 顯示成功訊息
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
});

document.getElementById('verify-email-btn').addEventListener('click', function() {
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
            showNotification(data.message); // 顯示成功訊息
            document.getElementById('verify-email-btn').disabled = true;
            document.getElementById('email-verified-icon').style.display = 'inline';
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification(error); // 使用showNotification顯示錯誤
        });
    } else {
        showNotification('請輸入驗證碼。'); // 使用showNotification顯示錯誤
    }
});



// 按下提交表單
document.addEventListener('DOMContentLoaded', function() {
    const formElement = document.getElementById('main-form');
    const errorContainer = document.getElementById('error-message');

    // 前端驗證規則
    const rules = [
        {
            field: 'snick',
            test: (value) => /^[a-zA-Z0-9_\u4e00-\u9fff]{3,20}$/.test(value),
            message: 'Invalid username. Username should be 3-20 characters long and can contain letters, numbers, and underscores.',
        },
        {
            field: 'pwd',
            test: (value) => value.length >= 8,
            message: 'Password must be at least 8 characters long.',
        },
        {
            field: 'confirm-pwd',
            test: (value) => {
                const password = document.getElementById('pwd').value;
                return password === value;
            },
            message: 'Passwords do not match.',
        }
    ];

    formElement.addEventListener("submit", function(event) {
        event.preventDefault(); // 阻止表單的預設提交行為

        // 清除先前的錯誤訊息
        errorContainer.style.display = 'none';

        // 執行前端驗證
        const validationResult = validateForm(this, rules);
        if (!validationResult.isValid) {
            showNotification(validationResult.errors.join('. '));
            return;
        }

        // 如果前端驗證通過，則處理表單提交
        let formData = new FormData(this);
        console.log(this);
        fetch("/api/register-submit-form", {
            method: "POST",
            body: formData
        })
        .then(handleResponse)
        .catch(handleError);
    });

    // 處理響應
    async function handleResponse(response) {
        const data = await response.json();
        if (!response.ok) {
            throw {isApiError: true, data: data};
        }
        showNotification(data.message, true);
        await delay(2000);
        window.location.href = '/';
    }

    // 失敗
    function handleError(error) {
        let message = "An error occurred. Please try again.";
        if (error.isApiError && error.data && error.data.error) {
            message = error.data.error;
        } else if (error.message) {
            message = error.message;
        }
        showNotification(message, false); // 顯示錯誤訊息
   }
});

function validateForm(form, rules) {
    const result = {
        isValid: true,
        errors: [],
    };

    rules.forEach(rule => {
        const { field, test, message } = rule;
        const value = form.querySelector(`[name=${field}]`).value;

        if (!test(value)) {
            result.isValid = false;
            result.errors.push(message);
        }
    });

    return result;
}
  
function showNotification(message, isSuccess = false) {
    const notification = document.createElement("div");
    notification.className = `notification ${isSuccess ? 'notification-success' : 'notification-error'}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = "0";
        notification.style.top = "10px"; // 建立一個向上移動淡出的效果
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500); // 這裡的時間應與CSS中的transition時間相符
    }, 3000); // 3秒後開始淡出
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }