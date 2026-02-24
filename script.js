const analyzeBtn = document.getElementById('analyzeBtn');
const usernameInput = document.getElementById('usernameInput');
const loader = document.getElementById('loader');
const statsGrid = document.getElementById('statsGrid');
const errorMsg = document.getElementById('errorMsg');

// Update your Render URL here after deployment
const API_URL = "https://your-backend-name.onrender.com/api/stats";

analyzeBtn.addEventListener('click', async () => {
    const username = usernameInput.value.trim();
    if (!username) return;

    // UI State Reset
    errorMsg.classList.add('hidden');
    statsGrid.classList.add('hidden');
    loader.classList.remove('hidden');

    try {
        const response = await fetch(`${API_URL}?username=${username}`);
        const data = await response.json();

        if (response.ok) {
            displayStats(data);
        } else {
            throw new Error(data.error);
        }
    } catch (err) {
        errorMsg.classList.remove('hidden');
    } finally {
        loader.classList.add('hidden');
    }
});

function displayStats(data) {
    statsGrid.classList.remove('hidden');
    
    animateNumber('followers', data.followers);
    animateNumber('likes', data.likes);
    animateNumber('videos', data.video_count);
    animateNumber('avgViews', data.avg_views);
}

function animateNumber(id, target) {
    const obj = document.getElementById(id);
    let start = 0;
    const duration = 1500;
    const step = (timestamp) => {
        if (!start) start = timestamp;
        const progress = Math.min((timestamp - start) / duration, 1);
        const current = Math.floor(progress * target);
        obj.innerHTML = current.toLocaleString();
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}
