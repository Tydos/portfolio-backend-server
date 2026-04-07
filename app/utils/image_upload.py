"""Image upload and metadata management utilities."""

import logging
import os
import csv

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
load_dotenv()


def upload_image(image_folder: str, cloud_folder_path: str, output_metadata_file: str):
    """Upload images from local folder to Cloudinary and save metadata to CSV."""
    uploaded_images = []
    existing_files = set()
    
    if os.path.exists(output_metadata_file):
        with open(output_metadata_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_files.add(row['filename'].strip())  # remove trailing spaces

    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            if filename in existing_files:
                logging.info(f"Skipping {filename}, already uploaded")
                continue
            file_path = os.path.join(image_folder, filename)
            try:
                response = cloudinary.uploader.upload(file_path, folder=cloud_folder_path)
                uploaded_images.append({
                    'filename': filename,
                    'url': response['secure_url'],
                    'width': response.get('width'),
                    'height': response.get('height'),
                    'category': 'nature'
                })
                logging.info(f"Response: {response}")
            except Exception as e:
                logging.exception(f"Failed to upload {filename}")

    # Write all uploaded images to CSV after processing all files
    with open(output_metadata_file, 'w', newline='') as csvfile:
        fieldnames = ['filename', 'url', 'width', 'height', 'category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(uploaded_images)

    return uploaded_images


if __name__ == "__main__":
    # Example usage
    image_folder = "images"
    output_metadata_file = "artifacts/image_metdata.csv"
    upload_image(image_folder, "portfolio/images", output_metadata_file)
