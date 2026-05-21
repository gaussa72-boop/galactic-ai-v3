import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import random

# Zielordner
output_folder = "static/images"
os.makedirs(output_folder, exist_ok=True)

def generate_galactic_image(filename, width=1024, height=1024):
    # Hintergrund: dunkler Weltraum
    base_color = (0, 0, 20)  # dunkelblau-schwarz
    img = Image.new("RGB", (width, height), base_color)
    draw = ImageDraw.Draw(img)

    # Galaktischer Nebel
    for _ in range(random.randint(50, 150)):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(30, 150)
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )
        opacity = random.randint(20, 80)
        layer = Image.new("RGBA", (width, height))
        ldraw = ImageDraw.Draw(layer)
        ldraw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color+(opacity,))
        img = Image.alpha_composite(img.convert("RGBA"), layer)

    # Singularität in der Mitte
    cx, cy = width // 2, height // 2
    for i in range(200):
        radius = random.randint(5, 100)
        angle = random.random() * 2 * np.pi
        dx = int(np.cos(angle) * radius)
        dy = int(np.sin(angle) * radius)
        color = (
            random.randint(200, 255),
            random.randint(180, 255),
            random.randint(100, 255),
        )
        draw.ellipse((cx+dx-5, cy+dy-5, cx+dx+5, cy+dy+5), fill=color)

    # Leichte Unschärfe für Traum-Effekt
    img = img.filter(ImageFilter.GaussianBlur(radius=2))

    # Speichern
    img = img.convert("RGB")
    img.save(os.path.join(output_folder, filename))

# Bildnummerierung
existing = [f for f in os.listdir(output_folder) if f.startswith("galactic_")]
num = len(existing) + 1
filename = f"galactic_{num:03d}.png"

# Bild generieren
generate_galactic_image(filename)
print(f"Bild gespeichert: {filename}")