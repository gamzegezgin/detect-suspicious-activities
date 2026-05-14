function pad(n) { return String(n).padStart(2, '0'); }

function updateTime() {
  const now = new Date();
  document.getElementById('login-time').textContent =
    `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
}
updateTime();
setInterval(updateTime, 1000);

const loginBtn = document.getElementById('loginBtn');
const errorMsg = document.getElementById('errorMsg');

// Zaten giriş yapılmışsa direkt dashboard'a git
if (localStorage.getItem('auth') === 'true') {
  window.location.href = 'index.html';
}

loginBtn.addEventListener('click', () => {
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  // Admin credentials
  if (username === 'admin' && password === 'admin123') {
    localStorage.setItem('auth', 'true');
    localStorage.setItem('user', username);
    window.location.href = 'index.html';
  } else {
    errorMsg.classList.remove('hidden');
    setTimeout(() => errorMsg.classList.add('hidden'), 3000);
  }
});

// Enter tuşu ile giriş
document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') loginBtn.click();
});