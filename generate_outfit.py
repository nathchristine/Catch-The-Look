from PIL import Image, ImageDraw
import os
import json

# Full theme list with their specific outfit types
theme_definitions = {
    "y2k": ["top", "bottom", "shoes", "accessories"],
    "futuristic": ["top", "bottom", "shoes", "accessories"],
    "glamorous": ["top", "bottom", "shoes", "accessories"],
    "business_casual": ["top", "bottom", "shoes", "accessories"],
    "kidcore": ["top", "bottom", "shoes", "accessories"],
    "cottagecore": ["dresses", "head_pieces", "shoes", "accessories"]
}

variants = ["1", "2", "3"]
base_path = "assets"
outfit_data = []

# Generate folders and dummy images
for theme, types in theme_definitions.items():
    for otype in types:
        folder = os.path.join(base_path, theme, otype)
        os.makedirs(folder, exist_ok=True)
        for v in variants:
            file_path = os.path.join(folder, f"{v}.png")
            if not os.path.exists(file_path):
                img = Image.new("RGBA", (100, 100), (230, 240, 255))
                draw = ImageDraw.Draw(img)
                draw.text((10, 40), f"{otype} {v}", fill="black")
                img.save(file_path)
            outfit_data.append({
                "theme": theme.replace("_", " ").title(),
                "type": otype.replace("_", " ").title(),
                "filename": f"{v}.png",
                "path": os.path.join(folder, f"{v}.png").replace("\\", "/")
            })

# Save metadata to outfits.json
os.makedirs("data", exist_ok=True)
with open("data/outfits.json", "w") as f:
    json.dump(outfit_data, f, indent=2)
