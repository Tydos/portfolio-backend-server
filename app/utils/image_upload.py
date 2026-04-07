# Image upload and metadata management utilities.

import logging
import os
import csv

from app.utils.cloudinary_uploader import CloudinaryUploader

logging.basicConfig(level=logging.DEBUG)


def upload_image(
    image_folder: str,
    cloud_folder_path: str,
    output_metadata_file: str,
    uploader: CloudinaryUploader | None = None,
):
    # Upload images from local folder to cloud storage and save metadata to CSV.
    if uploader is None:
        uploader = CloudinaryUploader()

    existing_images = []
    existing_files = set()
    
    if os.path.exists(output_metadata_file):
        with open(output_metadata_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_images.append(row)
                existing_files.add(row['filename'].strip())

    new_uploads = []
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            if filename in existing_files:
                logging.info(f"Skipping {filename}, already uploaded")
                continue
            file_path = os.path.join(image_folder, filename)
            try:
                result = uploader.upload(file_path, folder=cloud_folder_path)
                new_uploads.append({
                    'filename': filename,
                    'url': result['url'],
                    'width': result.get('width'),
                    'height': result.get('height'),
                    'category': 'nature'
                })
                logging.info(f"Uploaded {filename}: {result['url']}")
            except Exception as e:
                logging.exception(f"Failed to upload {filename}")

    # Write existing + new images to CSV, preserving previous entries
    all_images = existing_images + new_uploads
    with open(output_metadata_file, 'w', newline='') as csvfile:
        fieldnames = ['filename', 'url', 'width', 'height', 'category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_images)

    return new_uploads


if __name__ == "__main__":
    # Example usage
    image_folder = "images"
    output_metadata_file = "artifacts/image_metadata.csv"
    upload_image(image_folder, "portfolio/images", output_metadata_file)
