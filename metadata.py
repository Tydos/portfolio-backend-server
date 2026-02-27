import csv
from PIL import Image
from PIL.ExifTags import TAGS
import os

def generate_image_metadata(image_path):
    if not os.path.exists(image_path):
        return {"error": "File does not exist"}

    metadata = {}
    
    try:
        with Image.open(image_path) as img:
            metadata["filename"] = os.path.basename(image_path)
            metadata["format"] = img.format
            metadata["mode"] = img.mode
            metadata["width"], metadata["height"] = img.size
            
            # Extract EXIF data
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    metadata[f"exif_{tag}"] = value
            # No EXIF available
            else:
                metadata["exif"] = None
                
    except Exception as e:
        return {"error": str(e)}

    return metadata

def save_metadata_to_csv(metadata, csv_file):
    # Ensure metadata is a list of dicts
    if isinstance(metadata, dict):
        metadata = [metadata]
    
    # Get all possible keys (columns)
    keys = set()
    for m in metadata:
        keys.update(m.keys())
    keys = list(keys)
    
    # Write CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for m in metadata:
            writer.writerow(m)

# Example usage
image_path = "/Users/Patron/Github/portfolio-backend-server/example.jpeg"
meta = generate_image_metadata(image_path)
save_metadata_to_csv(meta, "image_metadata.csv")
print("Metadata saved to image_metadata.csv")