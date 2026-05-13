function pad(n) { return String(n).padStart(2, '0'); }

function updateClock() {
  const now = new Date();
  document.getElementById('live-date').textContent =
    `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}`;
  document.getElementById('live-time').textContent =
    `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
}
updateClock();
setInterval(updateClock, 1000);

const dropZone     = document.getElementById('dropZone');
const fileInput    = document.getElementById('fileInput');
const videoPlayer  = document.getElementById('videoPlayer');
const banner       = document.getElementById('detectionBanner');
const bannerLabel  = document.getElementById('bannerLabel');
const bannerSub    = document.getElementById('bannerSub');
const confPill     = document.getElementById('confPill');
const analyzing    = document.getElementById('analyzing');
const alertCount   = document.getElementById('alertCount');
const systemStatus = document.getElementById('systemStatus');
const liveDot      = document.getElementById('liveDot');
const liveText     = document.getElementById('liveText');
const log          = document.getElementById('log');

let alerts = 0;

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', (e) => {
  e.stopPropagation();
  dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith('video/')) {
    handleVideo(file);
  }
});

fileInput.addEventListener('change', (e) => {
  e.stopPropagation();
  const file = fileInput.files[0];
  if (file) handleVideo(file);
});

function handleVideo(file) {
  console.log('handleVideo çalıştı:', file.name, file.size);

  const url = URL.createObjectURL(file);
  videoPlayer.src = url;
  videoPlayer.classList.remove('hidden');
  dropZone.classList.add('hidden');

  liveDot.style.background = '#BA7517';
  liveText.textContent = 'ANALYZING';
  liveText.style.color = '#BA7517';
  systemStatus.textContent = 'Busy';
  systemStatus.className = 'stat-val';
  analyzing.classList.remove('hidden');
  banner.classList.add('hidden');

  const formData = new FormData();
  formData.append('video', file);

  fetch('http://localhost:5000/predict', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    console.log('Backend cevabı:', data);
    analyzing.classList.add('hidden');
    if (data.error) {
      showResult('Error', data.error, 0);
    } else {
      showResult(data.label, data.label, data.confidence);
    }
  })
  .catch((err) => {
    console.log('Hata:', err);
    analyzing.classList.add('hidden');
    showResult('Error', 'Server connection failed', 0);
  });
}

function showResult(label, sublabel, confidence) {
  banner.className = 'detection-banner';

  if (label === 'Fighting') {
    bannerLabel.textContent = 'Suspicious behavior detected';
    bannerSub.textContent   = 'Fighting detected';
    liveDot.style.background = '#E24B4A';
    liveText.textContent = 'ALERT';
    liveText.style.color = '#E24B4A';
  } else if (label === 'Vandalism') {
    bannerLabel.textContent = 'Suspicious behavior detected';
    bannerSub.textContent   = 'Vandalism detected';
    banner.classList.add('vandalism');
    liveDot.style.background = '#BA7517';
    liveText.textContent = 'ALERT';
    liveText.style.color = '#BA7517';
  } else if (label === 'NormalVideos') {
    bannerLabel.textContent = 'Normal activity';
    bannerSub.textContent   = 'No threat detected';
    banner.classList.add('normal');
    liveDot.style.background = '#1D9E75';
    liveText.textContent = 'LIVE';
    liveText.style.color = '#1D9E75';
  } else {
    bannerLabel.textContent = sublabel;
    bannerSub.textContent   = '';
  }

  confPill.textContent = confidence > 0 ? `${confidence.toFixed(0)}% conf.` : '';
  banner.classList.remove('hidden');
  systemStatus.textContent = 'Ready';
  systemStatus.className   = 'stat-val green';

  if (label === 'Fighting' || label === 'Vandalism') {
    alerts++;
    alertCount.textContent = alerts;
  }

  addLog(label, confidence);
}

function addLog(label, confidence) {
  const empty = log.querySelector('.log-empty');
  if (empty) empty.remove();

  const now  = new Date();
  const time = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;

  const colors  = { 'Fighting': '#E24B4A', 'Vandalism': '#BA7517', 'NormalVideos': '#1D9E75' };
  const classes = { 'Fighting': '', 'Vandalism': 'vandalism', 'NormalVideos': 'normal' };
  const icons   = { 'Fighting': '⚠', 'Vandalism': '⚠', 'NormalVideos': '✓' };
  const names   = { 'Fighting': 'Fighting', 'Vandalism': 'Vandalism', 'NormalVideos': 'Normal' };

  const item = document.createElement('div');
  item.className = `log-item ${classes[label] || ''}`;
  item.innerHTML = `
    <div class="log-type ${label === 'NormalVideos' ? 'normal' : ''}">
      ${icons[label] || '?'} ${names[label] || label}
    </div>
    <div class="log-meta">
      <span>uploaded video</span>
      <span>${time}</span>
    </div>
    <div class="conf-bar">
      <div class="conf-fill" style="width:${confidence.toFixed(0)}%;background:${colors[label] || '#888'};"></div>
    </div>
  `;

  log.insertBefore(item, log.firstChild);
  while (log.children.length > 20) log.removeChild(log.lastChild);
}