// Konfiguration des Quanten-Kerns
const bunteSterne = true; // Sollen die Partikel Farben haben?
const anzahlPartikel = 15000; // Wie viele Sterne/Staubpartikel?
const explosionsKraft = 15; // Wie stark ist der Impuls nach außen?

let scene, camera, renderer, particles;
let positions, velocities, colors;

function init() {
    // 1. Szene & Kamera (Die Welt aufbauen)
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
    camera.position.z = 500; // Blickdistanz zum Kern

    // 2. Renderer (Das Bild berechnen)
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    // Fügt das Canvas in den "singularity-node" Container aus deiner HTML ein
    document.getElementById('singularity-node').appendChild(renderer.domElement);

    // 3. Geometrie der Galaxie
    const geometry = new THREE.BufferGeometry();
    positions = new Float32Array(anzahlPartikel * 3);
    velocities = new Float32Array(anzahlPartikel * 3);
    colors = new Float32Array(anzahlPartikel * 3);

    const color = new THREE.Color();

    for (let i = 0; i < anzahlPartikel; i++) {
        // Position: Spiralarme um den Kern berechnen (Vereinfacht)
        const angle = i * 0.1 + Math.random() * 0.5;
        const radius = i * 0.05 + Math.random() * 20;

        positions[i * 3] = radius * Math.cos(angle); // X
        positions[i * 3 + 1] = radius * Math.sin(angle) + (Math.random() - 0.5) * 10; // Y (Höhe)
        positions[i * 3 + 2] = radius * Math.sin(angle) * 0.5; // Z

        // Geschwindigkeit: Standard-Drehung
        velocities[i * 3] = -radius * Math.sin(angle) * 0.01; // VX
        velocities[i * 3 + 1] = radius * Math.cos(angle) * 0.01; // VY
        velocities[i * 3 + 2] = 0; // VZ

        // Farbe: Gold/Orange/Weiß mixen für Nebel-Effekt
        if (bunteSterne) {
            color.setHSL(0.1 + Math.random() * 0.1, 0.9, 0.5 + Math.random() * 0.3);
            colors[i * 3] = color.r;
            colors[i * 3 + 1] = color.g;
            colors[i * 3 + 2] = color.b;
        } else {
            colors[i * 3] = 1; colors[i * 3 + 1] = 0.8; colors[i * 3 + 2] = 0.5; // Gold
        }
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // 4. Material (Wie sehen die Sterne aus?)
    const material = new THREE.PointsMaterial({
        size: 3,
        vertexColors: true, // Nutzt die berechneten Farben
        blending: THREE.AdditiveBlending, // Strahlen-Effekt
        transparent: true,
        depthWrite: false
    });

    // 5. Partikel-System erstellen und zur Szene hinzufügen
    particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Event Listener für den Klick (Auslöser)
    window.addEventListener('click', explode, false);
    window.addEventListener('resize', onWindowResize, false);
}

// 6. Die Animations-Schleife (Rendern und Bewegen)
function animate() {
    requestAnimationFrame(animate);

    // Standard-Drehung der Galaxie
    particles.rotation.z += 0.001;

    // Partikel-Positionen aktualisieren (Falls Explosion läuft)
    const positionsAttribute = particles.geometry.attributes.position;

    for (let i = 0; i < anzahlPartikel; i++) {
        positions[i * 3] += velocities[i * 3];
        positions[i * 3 + 1] += velocities[i * 3 + 1];
        positions[i * 3 + 2] += velocities[i * 3 + 2];

        // Reibung: Partikel bremsen langsam ab
        velocities[i * 3] *= 0.98;
        velocities[i * 3 + 1] *= 0.98;
        velocities[i * 3 + 2] *= 0.98;
    }
    positionsAttribute.needsUpdate = true; // Wichtig: Sagt Three.js, dass sich die Positionen geändert haben

    renderer.render(scene, camera);
}

// 7. Der Explosions-Impuls
function explode() {
    console.log("💥 Singularitäts-Ausbruch initialisiert...");

    // Spielt einen Sound ab (Optional, falls du einen hast)
    // new Audio('/static/assets/sounds/explosion.mp3').play();

    for (let i = 0; i < anzahlPartikel; i++) {
        // Vektor vom Kern zum Partikel berechnen (Richtung)
        const posX = positions[i * 3];
        const posY = positions[i * 3 + 1];
        const posZ = positions[i * 3 + 2];

        const distance = Math.sqrt(posX*posX + posY*posY + posZ*posZ);

        // Impuls radial nach außen geben
        const force = (Math.random() * explosionsKraft) / (distance * 0.1 + 1); // Kraft nimmt mit Entfernung ab

        velocities[i * 3] += (posX / distance) * force;
        velocities[i * 3 + 1] += (posY / distance) * force;
        velocities[i * 3 + 2] += (posZ / distance) * force;
    }
}

// Hilfsfunktion für Fenstergröße
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Starten
init();
animate();