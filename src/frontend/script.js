// ── Saat & Tarih ─────────────────────────────────────────────
function pad(n) { return String(n).padStart(2, '0'); }

function updateClock() {
  const now = new Date();
  const date = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}`;
  const time = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
  document.getElementById('live-date').textContent = date;
  document.getElementById('live-time').textContent = time;
}
updateClock();
setInterval(updateClock, 1000);

// ── Alert sayacı ─────────────────────────────────────────────
let alertCount = 0;

// ── Detection banner göster ──────────────────────────────────
function showDetection(label, confidence) {
  const banner  = document.getElementById('detectionBanner');
  const lbl     = document.getElementById('bannerLabel');
  const sub     = document.getElementById('bannerSub');
  const pill    = document.getElementById('confPill');

  banner.className = 'detection-banner';

  if (label === 'Fighting') {
    lbl.textContent = 'Suspicious behavior detected';
    sub.textContent = 'Fighting · CAM-01';
  } else if (label === 'Vandalism') {
    lbl.textContent = 'Suspicious behavior detected';
    sub.textContent = 'Vandalism · CAM-01';
    banner.classList.add('vandalism');
  } else {
    lbl.textContent = 'Normal activity';
    sub.textContent = 'No threat detected · CAM-01';
    banner.classList.add('normal');
  }

  pill.textContent = `${confidence.toFixed(0)}% conf.`;
  banner.classList.remove('hidden');

  if (label !== 'NormalVideos') {
    alertCount++;
    document.getElementById('alertCount').textContent = alertCount;
    document.getElementById('alertCount').className = 'stat-val red';
  }

  addLog(label, confidence);
}

// ── Log'a ekle ───────────────────────────────────────────────
function addLog(label, confidence) {
  const log  = document.getElementById('log');
  const now  = new Date();
  const time = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;

  const icons = {
    'Fighting':     '⚠',
    'Vandalism':    '⚠',
    'NormalVideos': '✓'
  };

  const colors = {
    'Fighting':     '#E24B4A',
    'Vandalism':    '#BA7517',
    'NormalVideos': '#1D9E75'
  };

  const classes = {
    'Fighting':     '',
    'Vandalism':    'vandalism',
    'NormalVideos': 'normal'
  };

  const item = document.createElement('div');
  item.className = `log-item ${classes[label]}`;
  item.innerHTML = `
    <div class="log-type ${label === 'NormalVideos' ? 'normal' : ''}">
      ${icons[label]} ${label === 'NormalVideos' ? 'Normal' : label}
    </div>
    <div class="log-meta">
      <span>CAM-01</span>
      <span>${time}</span>
    </div>
    <div class="conf-bar">
      <div class="conf-fill" style="width:${confidence.toFixed(0)}%;background:${colors[label]};"></div>
    </div>
  `;

  log.insertBefore(item, log.firstChild);

  // Maksimum 20 log tut
  while (log.children.length > 20) {
    log.removeChild(log.lastChild);
  }
}

// ── Backend'e her 5 saniyede tahmin iste ────────────────────
async function fetchPrediction() {
  try {
    const res  = await fetch('http://localhost:5000/status');
    const data = await res.json();
    if (data.label) {
      showDetection(data.label, data.confidence);
    }
  } catch (e) {
    console.log('Server bağlantısı yok');
  }
}

setInterval(fetchPrediction, 5000);