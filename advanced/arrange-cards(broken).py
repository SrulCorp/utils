import os
from PIL import Image

# --- SETTINGS ---
input_folder = r"C:\Users\SrulC\downloads\mtg images"  # Change if needed
resized_folder = os.path.join(input_folder, "resized")
pages_folder = os.path.join(input_folder, "pages")
output_pdf = os.path.join(input_folder, "cards.pdf")

# Card size in pixels (2.5 x 3.5 inches at 300 DPI)
card_width, card_height = 750, 1050

# Page size in pixels (US Letter, 8.5 x 11 inches at 300 DPI)
page_width, page_height = 2550, 3300

# Grid layout (3x3)
cols, rows = 3, 3
cards_per_page = cols * rows

# --- CREATE FOLDERS IF NEEDED ---
os.makedirs(resized_folder, exist_ok=True)
os.makedirs(pages_folder, exist_ok=True)

# --- STEP 1: FIND ALL PNG AND JPG/JPEG IMAGES RECURSIVELY ---
image_files = []
for root, dirs, files in os.walk(input_folder):
    for f in files:
        if f.lower().endswith((".png", ".jpg", ".jpeg")):
            # skip files in the output folders to avoid recursion issues
            if resized_folder not in os.path.join(root, f) and pages_folder not in os.path.join(root, f):
                image_files.append(os.path.join(root, f))

if not image_files:
    raise SystemExit(f"No PNG or JPG files found in {input_folder}")

print(f"Found {len(image_files)} image files. Resizing...")

# --- STEP 2: RESIZE IMAGES ---
resized_images = []

for i, img_path in enumerate(image_files):
    img = Image.open(img_path)
    img.thumbnail((card_width, card_height), Image.LANCZOS)
    new_img = Image.new("RGBA", (card_width, card_height), (255, 255, 255, 255))
    x = (card_width - img.width) // 2
    y = (card_height - img.height) // 2
    new_img.paste(img, (x, y))
    resized_path = os.path.join(resized_folder, f"{i:03}.png")
    new_img.save(resized_path)
    resized_images.append(resized_path)

print("Resizing complete.")

# --- STEP 3: CREATE PAGES ---
print("Creating pages...")
page_images = []

for i in range(0, len(resized_images), cards_per_page):
    page_img = Image.new("RGB", (page_width, page_height), "white")
    for j, card_path in enumerate(resized_images[i:i + cards_per_page]):
        card_img = Image.open(card_path).convert("RGB")
        col = j % cols
        row = j // cols
        x = col * card_width + (page_width - cols * card_width) // 2
        y = row * card_height + (page_height - rows * card_height) // 2
        page_img.paste(card_img, (x, y))
    page_path = os.path.join(pages_folder, f"page_{i//cards_per_page:02}.png")
    page_img.save(page_path)
    page_images.append(page_path)

print(f"Created {len(page_images)} pages.")

# --- STEP 4: SAVE AS PDF ---
print("Saving PDF...")
pdf_images = [Image.open(p).convert("RGB") for p in page_images]
pdf_images[0].save(output_pdf, save_all=True, append_images=pdf_images[1:], resolution=300)

print(f"Done! PDF saved to: {output_pdf}")
