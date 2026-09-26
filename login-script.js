const loginForm = document.getElementById('login-form');
const errorMessage = document.getElementById('error-message');
const passwordInput = document.getElementById('password');
const passwordToggle = document.querySelector('.password-toggle');
const deployedAppUrl = window.RESUTRACK_STREAMLIT_URL || 'http://localhost:8501/';

passwordToggle.addEventListener('click', () => {
  const isHidden = passwordInput.type === 'password';
  passwordInput.type = isHidden ? 'text' : 'password';
  passwordToggle.textContent = isHidden ? 'Hide' : 'Show';
  passwordToggle.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
});

loginForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const username = document.getElementById('username').value;
  const password = passwordInput.value;
  if (username !== 'Vicky' || password !== 'Vicky') {
    errorMessage.textContent = 'Invalid username or password. Please try again.';
    return;
  }
  if (deployedAppUrl.includes('YOUR-STREAMLIT-APP')) {
    errorMessage.textContent = 'Deployment setup is incomplete. Add your Streamlit URL in deploy-config.js.';
    return;
  }
  window.location.href = deployedAppUrl;
});
