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
            alert(data.message); // 顯示成功訊息
            document.getElementById('send-verify-email-btn').style.display = 'none';
            document.getElementById('verification-container').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            showError(error); // 使用showError顯示錯誤
            this.disabled = false; // 請求失敗後啟用按鈕
            this.textContent = '發送電子郵件';
        });
    } else {
        showError('請輸入有效的電子郵件地址。'); // 使用showError顯示錯誤
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
            alert(data.message); // 顯示成功訊息
            document.getElementById('verify-email-btn').disabled = true;
            document.getElementById('email-verified-icon').style.display = 'inline';
        })
        .catch(error => {
            console.error('Error:', error);
            showError(error); // 使用showError顯示錯誤
        });
    } else {
        showError('請輸入驗證碼。'); // 使用showError顯示錯誤
    }
});


// 按下提交表單
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('verification-code').required = false;
    document.getElementById("main-form").addEventListener("submit", function(event) {
        event.preventDefault(); // 阻止表單的預設提交行為

        let formData = new FormData(this);

        // 使用Fetch API傳送數據
        fetch("/api/register-submit-form", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                // 如果HTTP狀態碼不是2xx，則嘗試解析JSON以取得錯誤訊息
                return response.json().then(data => {
                    // 如果能夠解析錯誤訊息，則拋出自定義的錯誤對象
                    throw {isApiError: true, data: data};
                }, () => {
                    // 如果解析JSON失敗，則拋出通用錯誤
                    throw {isApiError: true, message: 'An error occurred. Please try again.'};
                });
            }
            if (response.redirected) {
                window.location.href = response.url;
                return Promise.reject({isApiError: false, message: 'Redirected'}); // 避免後續的then處理邏輯
            }
            return response.json();
        })
        .then(data => {
            if (data && data.error) {
                // 顯示錯誤訊息
                showError(data.error);
            } else {
                // 處理成功邏輯
                window.location.href = "/"; // 或顯示成功訊息
            }
        })
        .catch(error => {
            // 這裡根據錯誤類型決定處理方式
            if (error.isApiError) {
                // 顯示來自API的錯誤訊息
                showError(error.data ? error.data.error : error.message);
            } else {
                // JavaScript錯誤只在控制台顯示
                console.error('JS Error:', error.message);
            }
        });
    });
});

function showError(message) {
    const errorMessageDiv = document.getElementById("error-message");
    errorMessageDiv.textContent = message;
    errorMessageDiv.style.display = "block";
    // 重置樣式以重新開始動畫，如果之前已經淡出
    errorMessageDiv.style.opacity = "1";
    setTimeout(() => {
        errorMessageDiv.style.opacity = "0";
        setTimeout(() => {
            errorMessageDiv.style.display = "none";
        }, 500); // 確保這個時間與CSS中的transition時間相符
    }, 5000); // 5秒後開始淡出
}