from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np
import os
import glob

# Spør bruker om filnavn
pdf_path = input("Hva heter PDF-filen? (f.eks. 'input.pdf'): ").strip()

# Output-mappe
output_folder = "slides"
dpi = 200
os.makedirs(output_folder, exist_ok=True)

print(f"Konverterer '{pdf_path}' til bilder...")
try:
    pages = convert_from_path(pdf_path, dpi=dpi)
except Exception as e:
    print(f"Kunne ikke åpne '{pdf_path}': {e}")
    exit(1)

slide_counter = 1

for page_index, page in enumerate(pages):
    print(f"\nBehandler side {page_index + 1}...")
    img = np.array(page)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda cnt: cv2.boundingRect(cnt)[1])

    slides_found = 0

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if w < 500 or h < 100:
            continue

        # Crop ut slide
        slide_img = img[y : y + h, x : x + w]

        # Fjern nederste 1%
        crop_bottom = int(h * (1 - 0.04))
        slide_img_cropped = slide_img[0:crop_bottom, :]

        slide_pil = Image.fromarray(slide_img_cropped)
        filename = f"{output_folder}/slide_{slide_counter:03}.png"
        slide_pil.save(filename)
        print(
            f"   Lagret slide {slide_counter:03} (x={x}, y={y}, w={w}, h={crop_bottom})"
        )
        slide_counter += 1
        slides_found += 1

    if slides_found == 0:
        print("   Ingen slides funnet på denne siden.")

print("\nKonverterer PNG-bilder til én PDF...")

slide_files = sorted(glob.glob(f"{output_folder}/slide_*.png"))
images = [Image.open(f).convert("RGB") for f in slide_files]

if images:
    images[0].save("output.pdf", save_all=True, append_images=images[1:])
    print(f"Laget 'output.pdf' med {len(images)} slides.")
else:
    print("Fant ingen bilder å konvertere til PDF.")
