import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

folder = "static/images"
os.makedirs(folder, exist_ok=True)

def lebensblume(draw, cx, cy, r):

    for a in range(0,360,30):

        x = cx + r*np.cos(np.radians(a))
        y = cy + r*np.sin(np.radians(a))

        draw.ellipse(
            (x-r/2,y-r/2,x+r/2,y+r/2),
            outline=(255,215,0),
            width=2
        )

def generate():

    w = 1024
    h = 1024

    img = Image.new("RGB",(w,h),(0,0,20))
    draw = ImageDraw.Draw(img)

    # Nebel
    for i in range(200):

        x=random.randint(0,w)
        y=random.randint(0,h)

        r=random.randint(20,200)

        color=(
            random.randint(50,255),
            random.randint(50,255),
            random.randint(50,255)
        )

        draw.ellipse((x-r,y-r,x+r,y+r),fill=color)

    # Singularität

    cx=w//2
    cy=h//2

    for i in range(400):

        angle=random.random()*np.pi*2
        radius=random.randint(0,200)

        x=int(cx+np.cos(angle)*radius)
        y=int(cy+np.sin(angle)*radius)

        draw.ellipse((x-3,y-3,x+3,y+3),fill=(255,220,120))

    # Lebensblume
    lebensblume(draw,cx,cy,250)

    img=img.filter(ImageFilter.GaussianBlur(2))

    count=len(os.listdir(folder))+1
    name=f"galaxy_{count}.png"

    img.save(os.path.join(folder,name))

    print("Generated:",name)

generate()