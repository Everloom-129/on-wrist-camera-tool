# image preprocessing
# image preprocessing
import os
from PIL import Image

def rename_images(input_folder):
    """
    Rename all images in a folder to sequential numbers (1.jpg, 2.jpg, etc.)
    """
    # Get all files in the folder
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Sort files to ensure consistent ordering
    files.sort()
    
    # Rename files
    for index, filename in enumerate(files, start=1):
        old_path = os.path.join(input_folder, filename)
        new_path = os.path.join(input_folder, f"{index}.jpg")
        os.rename(old_path, new_path)
    
    return len(files)

def compress_images(input_folder, target_width=640, target_height=480):
    """
    Compress images to specified dimensions while maintaining aspect ratio
    """
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            with Image.open(image_path) as img:
                # Resize image maintaining aspect ratio
                img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
                # Save the compressed image, overwriting the original
                img.save(image_path, "JPEG", quality=85)

def process_and_store(input_folder, output_folder, compress=False):
    """
    Process images and store them in a new folder
    Args:
        input_folder: Source folder containing images
        output_folder: Destination folder for processed images
        compress: Optional flag to compress images (default: False)
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # First rename all images
    num_images = rename_images(input_folder)
    
    # Copy files to new location
    for i in range(1, num_images + 1):
        input_path = os.path.join(input_folder, f"{i}.jpg")
        output_path = os.path.join(output_folder, f"{i}.jpg")
        
        # Just copy the file if no compression needed
        if not compress:
            img = Image.open(input_path)
            img.save(output_path)
        else:
            with Image.open(input_path) as img:
                img.thumbnail((640, 480), Image.Resampling.LANCZOS)
                img.save(output_path, "JPEG", quality=85)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python img_pre.py <input_folder> <output_folder>")
        print("Example: python img_pre.py 'Camera Roll' Koch_1210")
        sys.exit(1)
        
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    
    # Optional compression flag
    compress = True
    if len(sys.argv) > 3 and sys.argv[3].lower() == "false":
        compress = False
        
    process_and_store(input_folder, output_folder, compress=compress)