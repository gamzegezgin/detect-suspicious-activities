function pad(n) {
  return String(n).padStart(2, "0");
}

function updateTime() {
  const now = new Date();
  document.getElementById("login-time").textContent =
    `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
}
updateTime();
setInterval(updateTime, 1000);

const loginBtn = document.getElementById("loginBtn");
const errorMsg = document.getElementById("errorMsg");

loginBtn.addEventListener("click", async () => {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !password) {
    errorMsg.classList.remove("hidden");
    return;
  }

  loginBtn.textContent = "AUTHENTICATING...";
  loginBtn.disabled = true;

  try {
    const res = await fetch("http://localhost:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();

    if (res.ok && data.token) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", data.username);
      window.location.href = "index.html";
    } else {
      errorMsg.classList.remove("hidden");
      setTimeout(() => errorMsg.classList.add("hidden"), 3000);
      loginBtn.textContent = "SIGN IN";
      loginBtn.disabled = false;
    }
  } catch (err) {
    errorMsg.textContent = "Server connection failed";
    errorMsg.classList.remove("hidden");
    loginBtn.textContent = "SIGN IN";
    loginBtn.disabled = false;
  }
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Enter") loginBtn.click();
});
