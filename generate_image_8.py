from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
import random

W, H = 1200, 1200
img = Image.new('RGBA', (W, H), (30, 22, 28, 255))
draw = ImageDraw.Draw(img)

# Create a dark blurred background with soft pink/blue highlights
for cx, cy, r, color in [
    (200, 180, 360, (160, 117, 122, 150)),
    (900, 180, 420, (116, 132, 154, 150)),
    (230, 900, 360, (158, 126, 154, 140)),
    (910, 930, 400, (120, 140, 170, 150)),
    (600, 620, 500, (200, 171, 180, 120)),
]:
    blurred = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(blurred)
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=color)
    img = Image.alpha_composite(img, blurred)

img = img.filter(ImageFilter.GaussianBlur(9))

# Add soft vignette
vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
vdraw = ImageDraw.Draw(vignette)
vdraw.rounded_rectangle((0, 0, W, H), radius=0, fill=(0, 0, 0, 38))
img = Image.alpha_composite(img, vignette)

# Draw tiny floating hearts and sparkles
heart_font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 30)
small_font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
heart_positions = [
    (180, 180), (930, 150), (250, 450), (980, 480),
    (120, 780), (1040, 760), (210, 980), (980, 930),
    (540, 240), (620, 140), (450, 710), (760, 870),
]
for x, y in heart_positions:
    draw.text((x, y), '❤', font=heart_font, fill=(255, 142, 170, 180))

# Add some little sparkles
sparkles = ['✦', '✧', '✦', '✧', '•']
for i in range(28):
    x = random.randint(120, 1080)
    y = random.randint(150, 1000)
    s = random.choice(sparkles)
    draw.text((x, y), s, font=small_font, fill=(255, 195, 210, 120))

# Draw card
card_x, card_y = 170, 210
card_w, card_h = 860, 700
shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow)
shadow_draw.rounded_rectangle((card_x + 18, card_y + 18, card_x + card_w + 18, card_y + card_h + 18), radius=52, fill=(0, 0, 0, 70))
img = Image.alpha_composite(img, shadow)

card = Image.new('RGBA', (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle((card_x, card_y, card_x + card_w, card_y + card_h), radius=52, fill=(243, 238, 236, 255), outline=(244, 185, 205, 255), width=6)
img = Image.alpha_composite(img, card)

# Text content
header_font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 72)
body_font = ImageFont.truetype('C:/Windows/Fonts/calibri.ttf', 31)
body_font_bold = ImageFont.truetype('C:/Windows/Fonts/calibrib.ttf', 33)

# Title
header = 'Iloveyouuu!'
header_bbox = draw.textbbox((0, 0), header, font=header_font)
header_w = header_bbox[2] - header_bbox[0]
header_x = card_x + (card_w - header_w) / 2
header_y = card_y + 48
# draw title in dark plum color
text_color = (75, 48, 64, 255)
draw.text((header_x, header_y), header, font=header_font, fill=text_color)

# Justified body text with blank line before signature
body_lines = [
    'Happy birthday, love. Mag-iingat ka palagi',
    "sa work mo. Andito lang ako palagi",
    "nakasupporta sa'yo. I am always proud of",
    "you, darling! Kakampi mo ako palagi. I can't",
    'wait to build our life together! Imissyouuu',
    'and iloveyousmuch!! I hope nagustuhan',
    'mo ito love hahahha mwaa!'
]

# Full-justify helper

def justify_line(line, max_width, font):
    if not line.strip():
        return line
    words = line.split()
    if len(words) <= 1:
        return line
    text = words[0]
    space_width = draw.textbbox((0, 0), ' ', font=font)[2]
    for word in words[1:]:
        text += ' ' + word
    total_width = draw.textbbox((0, 0), text, font=font)[2]
    if total_width >= max_width:
        return line
    gaps = len(words) - 1
    extra = max_width - total_width
    add_per_gap = extra / gaps
    extra_spaces = max(1, int(round(add_per_gap / space_width)))
    final = words[0]
    for word in words[1:]:
        final += ' ' * (1 + extra_spaces) + word
    return final

# Body layout
body_start_x = card_x + 62
body_start_y = card_y + 170
max_line_width = card_w - 120
current_y = body_start_y
for line in body_lines:
    justified = justify_line(line, max_line_width, body_font)
    linebbox = draw.textbbox((0, 0), justified, font=body_font)
    line_w = linebbox[2] - linebbox[0]
    x = body_start_x + (max_line_width - line_w) / 2
    draw.text((x, current_y), justified, font=body_font, fill=text_color)
    current_y += 52

# Add full blank line before signature
current_y += 36

# Signature line
sig = 'Happy Birthday ulit, darlingggg!'
sig_font = ImageFont.truetype('C:/Windows/Fonts/calibrib.ttf', 34)
sig_bbox = draw.textbbox((0, 0), sig, font=sig_font)
sig_w = sig_bbox[2] - sig_bbox[0]
sig_x = card_x + (card_w - sig_w) / 2
sig_y = current_y + 6
draw.text((sig_x, sig_y), sig, font=sig_font, fill=text_color)

# Final save
out_path = os.path.join('images', 'image_8.png')
os.makedirs('images', exist_ok=True)
img.save(out_path)
print(f'Generated: {out_path}')
