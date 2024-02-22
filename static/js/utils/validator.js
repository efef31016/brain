// 驗證表單
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

// 顯示錯誤訊息
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

// 將函數暴露為模塊的公開接口
export { validateForm, showError };
