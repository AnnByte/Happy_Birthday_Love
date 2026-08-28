from pathlib import Path
from PIL import Image

base = Path(r"c:\xampp\htdocs\habadu\images")
for name in ["heart1.jpg", "heart2.jpg"]:
    img = Image.open(base / name).convert("RGBA")
    pixels = []
    for r, g, b, a in img.getdata():
        if r > 245 and g > 245 and b > 245:
            pixels.append((255, 255, 255, 0))
        else:
            pixels.append((r, g, b, a))
    img.putdata(pixels)
    out = base / (Path(name).stem + "_transparent.png")
    img.save(out)
    print(out.name)
