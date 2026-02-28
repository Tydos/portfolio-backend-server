from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
import csv
import logging

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

REQUIRED_VARS = ["CLOUDNAME", "CLOUDINARYAPI", "CLOUDINARYAPISECRET"]
for var in REQUIRED_VARS:
    if not os.getenv(var):
        raise RuntimeError(f"Missing environment variable: {var}")

#setup cloudinary config for posting images
cloudinary.config(
        cloud_name=os.getenv("CLOUDNAME"),
        api_key=os.getenv("CLOUDINARYAPI"),
        api_secret=os.getenv("CLOUDINARYAPISECRET"),
        secure=True,
    )


def upload_image(image_folder,cloud_folder_path,output_metadata_file):
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
                response = cloudinary.uploader.upload(file_path,folder=cloud_folder_path)
                uploaded_images.append({
                    'filename': filename,
                    'url': response['secure_url'],
                    'width': response.get('width'),
                    'height': response.get('height'),
                    'category': 'Nature'
                })
                logging.info(f"Response: {response}")
            except Exception as e:
                print(f"Failed to upload {filename}: {e}")
                
            with open(output_metadata_file, 'w', newline='') as csvfile:
                fieldnames = ['filename', 'url', 'width', 'height', 'category']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for img in uploaded_images:
                    writer.writerow(img)


if __name__ == "__main__":
    #Input output directories
    image_folder = '//Users/Patron/Github/portfolio-backend-server/images'
    output_data = '/Users/Patron/Github/portfolio-backend-server/image_metdata.csv'
    cloud_folder_path = 'Photos'
    uploaded_images = []
    upload_image(image_folder=image_folder,cloud_folder_path=cloud_folder_path,output_metadata_file=output_data)
    print(uploaded_images)