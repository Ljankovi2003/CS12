/* scripts.js */

document.getElementById("navigate-form").addEventListener("submit", function(event) {
    event.preventDefault();
    let target = document.getElementById("target").value.trim();

    fetch("/navigate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: target })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        let images = data.map_images;
        let index = 0;
        let arrivalSwitch = document.getElementById("arrival-switch");
        let progressBar = document.getElementById("progress-bar");

        function updateImage() {
            if (index < images.length) {
                document.getElementById("map-image").src = "data:image/png;base64," + images[index];
                index++;
                setTimeout(updateImage, 500);
            } else {
                arrivalSwitch.checked = true;
                startBatterySwap();
            }
        }

        function startBatterySwap() {
            let progress = 0;
            let interval = setInterval(() => {
                if (progress >= 100) {
                    clearInterval(interval);
                } else {
                    progress += 10;
                    progressBar.style.width = progress + "%";
                    progressBar.textContent = progress + "%";
                    progressBar.style.background = "linear-gradient(135deg, #00ff99, #00cc66)";
                }
            }, 500);
        }

        updateImage();
    })
    .catch(error => console.error("Error:", error));
});
