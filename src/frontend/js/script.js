const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "login.html";
}

function pad(n) {
  return String(n).padStart(2, "0");
}

function updateClock() {
  const now = new Date();
  document.getElementById("live-date").textContent =
    `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  document.getElementById("live-time").textContent =
    `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
}
updateClock();
setInterval(updateClock, 1000);

const videoPlayer = document.getElementById("videoPlayer");
const banner = document.getElementById("detectionBanner");
const bannerLabel = document.getElementById("bannerLabel");
const bannerSub = document.getElementById("bannerSub");
const confPill = document.getElementById("confPill");
const alertCount = document.getElementById("alertCount");
const log = document.getElementById("log");

let alerts = 0;
let lastVideo = "";

function fetchStatus() {
  fetch("http://localhost:5000/status", {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then((r) => {
      if (r.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "login.html";
        return null;
      }
      return r.json();
    })
    .then((data) => {
      if (!data) return;
      if (data.video && data.video !== lastVideo) {
        lastVideo = data.video;
        videoPlayer.src = "";
        videoPlayer.load();
        videoPlayer.src = `http://localhost:5000/video/${data.video}`;
        videoPlayer.play().catch((e) => console.log("Video play error:", e));
      }
      showResult(data.label, data.confidence);
    })
    .catch((err) => console.log("Bağlantı hatası:", err));
}

function showResult(label, confidence) {
  banner.className = "detection-banner";

  if (label === "Fighting") {
    bannerLabel.textContent = "Suspicious behavior detected";
    bannerSub.textContent = "Fighting detected";
  } else if (label === "Vandalism") {
    bannerLabel.textContent = "Suspicious behavior detected";
    bannerSub.textContent = "Vandalism detected";
    banner.classList.add("vandalism");
  } else {
    banner.classList.add("hidden"); // Normal ise banner'ı gizle
    return; // Buradan çık, log ekleme
  }

  confPill.textContent = `${confidence.toFixed(0)}% conf.`;
  banner.classList.remove("hidden");

  if (label === "Fighting" || label === "Vandalism") {
    alerts++;
    alertCount.textContent = alerts;
  }

  addLog(label, confidence);
}

function addLog(label, confidence) {
  const empty = log.querySelector(".log-empty");
  if (empty) empty.remove();

  const now = new Date();
  const time = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;

  const colors = {
    Fighting: "#E24B4A",
    Vandalism: "#BA7517",
    NormalVideos: "#1D9E75",
  };
  const classes = {
    Fighting: "",
    Vandalism: "vandalism",
    NormalVideos: "normal",
  };
  const icons = { Fighting: "⚠", Vandalism: "⚠", NormalVideos: "✓" };
  const names = {
    Fighting: "Fighting",
    Vandalism: "Vandalism",
    NormalVideos: "Normal",
  };

  const item = document.createElement("div");
  item.className = `log-item ${classes[label] || ""}`;
  item.innerHTML = `
    <div class="log-type ${label === "NormalVideos" ? "normal" : ""}">
      ${icons[label] || "?"} ${names[label] || label}
    </div>
    <div class="log-meta">
      <span>CAM-01</span>
      <span>${time}</span>
    </div>
    <div class="conf-bar">
      <div class="conf-fill" style="width:${confidence.toFixed(0)}%;background:${colors[label] || "#888"};"></div>
    </div>
  `;

  log.insertBefore(item, log.firstChild);
  while (log.children.length > 20) log.removeChild(log.lastChild);
}

fetchStatus();
setInterval(fetchStatus, 3000);

document.getElementById("logoutBtn").addEventListener("click", () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  window.location.href = "login.html";
});
