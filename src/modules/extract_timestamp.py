import os
import csv
import pytesseract
from PIL import Image
import re
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def screenshot_to_start(jpg_file):
    hour = int(jpg_file[-12:-10])
    minute = int(jpg_file[-9:-7])
    seconds = int(jpg_file[-6:-4])
    return 3600*hour+minute*60+seconds


def crop_bottom_right(image, width_percent=25, height_percent=10):
    """Crop the bottom right corner of an image"""
    width, height = image.size
    crop_width = int(width * width_percent / 100)
    crop_height = int(height * height_percent / 100)
    
    # Define the region to crop (bottom right)
    right = width
    bottom = int(height*0.95)
    left = right - crop_width
    top = bottom - crop_height
    
    return image.crop((left, top, right, bottom))

def extract_timestamp(image):
    """Extract timestamp from an image using OCR"""
    # Convert to grayscale for better OCR results
    image = image.convert('L')
    
    # Enhance contrast if needed
    # from PIL import ImageEnhance
    # enhancer = ImageEnhance.Contrast(image)
    # image = enhancer.enhance(2.0)
    
    # Extract text
    text = pytesseract.image_to_string(image)
    
    # Try to find timestamp patterns
    # This pattern looks for dates and times in various formats
    patterns = [
        r'\d{1,2}:\d{2}:\d{2}',                        # HH:MM:SS
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
    
    return "00:00:00"

def process_images(directory, duration, output_csv):
    """Process all jpg images in a directory and save timestamps to CSV"""
    # Check if directory exists
    if not os.path.isdir(directory):
        logging.error(f"Directory {directory} does not exist!")
        return
    
    # Create CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Image', 'Timestamp', 'Path', 'Start_time', 'End_time'])
        
        # Get all jpg files
        jpg_files = [f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg'))]
        total_files = len(jpg_files)
        
        if total_files == 0:
            logging.warning(f"No JPG images found in {directory}")
            return
            
        logging.info(f"Found {total_files} JPG images to process")
        
        # Process each image
        for i, filename in enumerate(jpg_files):
            try:
                logging.info(f"Processing {i+1}/{total_files}: {filename}")
                file_path = os.path.join(directory, filename)
                
                # Open image
                img = Image.open(file_path)
                
                # Crop bottom right
                cropped = crop_bottom_right(img)
                
                # Extract timestamp
                timestamp = extract_timestamp(cropped)
                hours, mins, secs = map(int, timestamp.split(':'))
                start_time = screenshot_to_start(filename)
                end_time = start_time + 3600*hours+60*mins+secs
                # Save to CSV
                if timestamp!="00:00:00" and end_time<duration:
                    csv_writer.writerow([filename, timestamp, file_path, start_time, end_time])
                
            except Exception as e:
                logging.error(f"Error processing {filename}: {str(e)}")
    
    logging.info(f"Processing complete. Results saved to {output_csv}")

if __name__ == "__main__":
    # print(screenshot_to_start("screenshot_0020_03-09-59"))
    # parser = argparse.ArgumentParser(description='Extract timestamps from images')
    # parser.add_argument('directory', type=str, help='Directory containing JPG images')
    # parser.add_argument('--output', type=str, default='timestamps.csv', 
    #                     help='Output CSV file name (default: timestamps.csv)')
    # parser.add_argument('--width', type=int, default=25,
    #                     help='Width percentage to crop from right (default: 25%)')
    # parser.add_argument('--height', type=int, default=10,
    #                     help='Height percentage to crop from bottom (default: 10%)')
    
    # args = parser.parse_args()
    directory = "./screenshots/Tangerin_vid_21_09_25"
    sc_dir = "/Tangerin_vid_21_09_25"

    
    process_images(directory,  0 , f"./timestamps{sc_dir}")
 #   print(screenshot_to_start("screenshot_1016435_04-42-20.jpg"))
#    print(screenshot_to_start("screenshot_100744_00-27-59.jpg"))
    
