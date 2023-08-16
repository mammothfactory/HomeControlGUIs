from PIL import Image

def load_and_convert_bmp(file_path):
    # Open the BMP image
    img = Image.open(file_path)

    # Resize the image to 64x64 pixels
    #img = img.resize((64, 64), Image.ANTIALIAS)

    # Convert the image to grayscale
    img = img.convert('L')

    # Convert the image data into a 2D list of pixel values
    pixel_data = list(img.getdata())
    pixel_matrix = [pixel_data[i:i+64] for i in range(0, 64*64, 64)]

    return pixel_matrix

# Replace 'your_image.bmp' with the path to your BMP image file
bmp_file_path = 'BWfanLogo64x64.bmp'
pixel_matrix = load_and_convert_bmp(bmp_file_path)

# Define a function to visualize the pixel matrix (for demonstration purposes)
def visualize_pixel_matrix(pixel_matrix):
    for row in pixel_matrix:
        print(' '.join(['#' if pixel > 128 else '.' for pixel in row]))

# Visualize the pixel matrix (optional)
visualize_pixel_matrix(pixel_matrix) 