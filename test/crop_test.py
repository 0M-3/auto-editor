from PIL import Image

def crop_bottom_right(image, width_percent=25, height_percent=15):
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

if __name__ == '__main__':
    Img= Image.open("screenshot_0000_0-00-00.jpg")
    Cropped = crop_bottom_right(Img)
    Cropped.save("cropped.jpg")