const live_users = document.getElementById("live_users");

function animateNumber(finalNumber, duration = 1000, startNumber = 0, callback) {
    const startTime = performance.now();
    
    function easeOutQuad(t) {
        return 1 - Math.pow(1 - t, 3);
    }
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easedProgress = easeOutQuad(progress);
        const currentNumber = Math.floor(easedProgress * (finalNumber - startNumber) + startNumber);
      
        callback(currentNumber);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    requestAnimationFrame(update);
}

document.addEventListener("DOMContentLoaded", () => {
    const infoBtn = document.getElementById("info-button");
    if (infoBtn) {
        infoBtn.addEventListener("click", () => {
            const url = infoBtn.dataset.url;
            window.location.href = url;
        });
    }

    document.querySelectorAll('form').forEach(form => form.reset());
});

document.addEventListener('DOMContentLoaded', () => {
    const infoButton = document.getElementById('info-button');
    const infoUrl = infoButton.dataset.infoUrl;
    infoButton.style.backgroundImage = `url('${infoUrl}')`;

    animateNumber(386, 2000, 0, (n) => {
        live_users.textContent = n;
    });

    const changing_text = document.getElementById('changing-text');

    const words = ['ANALYSIS', 'STATISTICS', 'BEHAVIOR'];
    const word_colors = ['rgb(255, 207, 189)', 'rgb(197, 255, 189)', 'rgb(255, 189, 225)'];
    let currentIndex = 0;
    
    setInterval(() => {
        currentIndex = (currentIndex + 1) % words.length;
        changing_text.textContent = words[currentIndex];
        changing_text.style.color = word_colors[currentIndex];
    }, 5000);
});
  