document.addEventListener("DOMContentLoaded", () => {
    const infoBtn = document.getElementById("info-button");
    if (infoBtn) {
        infoBtn.addEventListener("click", () => {
            const url = infoBtn.dataset.url;
            window.location.href = url;
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const infoButton = document.getElementById('info-button');
    const infoUrl = infoButton.dataset.infoUrl;
    infoButton.style.backgroundImage = `url('${infoUrl}')`;
  });
  