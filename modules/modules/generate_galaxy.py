import matplotlib.pyplot as plt
import numpy as np
import os
import time


def generate_galaxy():
    # Mathematische Spirale für die Galaxien-Arme
    n_stars = 2000
    theta = np.linspace(0, 8 * np.pi, n_stars)
    r = theta ** 1.5

    # Rauschen hinzufügen für Realismus
    x = r * np.cos(theta) + np.random.normal(0, 10, n_stars)
    y = r * np.sin(theta) + np.random.normal(0, 10, n_stars)
    colors = np.arctan2(y, x)

    plt.figure(figsize=(6, 6), facecolor='black')
    plt.scatter(x, y, c=colors, cmap='magma', s=1, alpha=0.6)
    plt.axis('off')

    # Dateiname mit Zeitstempel, um Überschreiben zu verhindern
    filename = f"galaxy_{int(time.time())}.jpg"
    path = os.path.join("static", "images", filename)

    plt.savefig(path, bbox_inches='tight', pad_inches=0, facecolor='black')
    plt.close()
    print(f"Galaxie gespeichert unter: {path}")


if __name__ == "__main__":
    generate_galaxy()