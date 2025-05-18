from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np
import os

# 📥 Spør bruker om filnavn
pdf_path = input("📄 Hva heter PDF-filen? (f.eks. 'input.pdf'): ").strip()

# 📁 Output-mappe
output_folder = "slides"
dpi = 200

# ➕ Lag mappe hvis den ikke finnes
os.makedirs(output_folder, exist_ok=True)

print(f"📈 Konverterer '{pdf_path}' til bilder...")
try:
    pages = convert_from_path(pdf_path, dpi=dpi)
except Exception as e:
    print(f"❌ Klarte ikke å åpne '{pdf_path}': {e}")
    exit(1)

slide_counter = 1

for page_index, page in enumerate(pages):
    print(f"\n🖼️ Behandler side {page_index + 1}...")
    img = np.array(page)

    # Gråskala
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Binariser: gjør mørke områder svarte
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # Finn konturer
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sorter konturene ovenfra og ned
    contours = sorted(contours, key=lambda cnt: cv2.boundingRect(cnt)[1])

    slides_found = 0

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Filtrer bort små "støy"områder
        if w < 500 or h < 100:
            continue

        slide_img = img[y : y + h, x : x + w]
        slide_pil = Image.fromarray(slide_img)
        filename = f"{output_folder}/slide_{slide_counter:03}.png"
        slide_pil.save(filename)
        print(
            f"   ✅ Lagret slide {slide_counter:03} (pos: x={x}, y={y}, w={w}, h={h})"
        )
        slide_counter += 1
        slides_found += 1

    if slides_found == 0:
        print("   ⚠️ Ingen slides funnet på denne siden.")

print(
    f"\n🎉 Ferdig! Totalt {slide_counter - 1} slides lagret i mappa '{output_folder}/'"
)
