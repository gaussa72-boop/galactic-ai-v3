let pulseBase = 0.02;
let typingEffect = 0;

// Erhöht die Puls-Geschwindigkeit beim Tippen
document.getElementById("user-input").addEventListener("keypress", () => {
    typingEffect = 0.05;
    setTimeout(() => { typingEffect = 0; }, 500);
});

function animateFlower() {
    let speed = pulseBase + typingEffect;
    // ... deine Canvas-Zeichen-Logik nutzt 'speed' ...
    requestAnimationFrame(animateFlower);
}