"""
Counts the number of pixels of each color in an image and writes the information to a file.

Usage:
    color-counter.py image.png [output.txt]

Args:
    image.png: The path to the image file.
    [output.txt]: The path to the output file. Defaults to "count.txt".
"""

import sys
import PIL
from PIL import Image, ImageDraw

def rgb_to_hex(rgb):
    """Converts RGB to HEX."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def get_contrast_color(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Calculates the contrast color (black or white) based on the luminance of the background color.

    Args:
        rgb (tuple[int, int, int]): A tuple with the RGB components of the color.

    Returns:
        tuple[int, int, int]: A tuple with the RGB components of the contrast color (black or white).
    """
    luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
    return (0, 0, 0) if luminance > 0.5 else (255, 255, 255)

def count_colors(image_path, output_file="count.txt"):
    """
    Counts the number of pixels of each color in an image and writes the information to a file.

    Args:
        image_path (str): The path to the image file.
        output_file (str): The path to the output file. Defaults to "count.txt".
    """
    try:
        # Try to open the image
        im1 = Image.open(image_path)
    except FileNotFoundError:
        print("File not found.")
        return
    except Exception as e:
        print(f"Error opening file: {e}")
        return

    # Convert the image to a palette of 256 colors
    im = im1.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=256)
    pict_pal = im.getpalette()  # Get the palette of colors
    colors_num = im.getcolors()  # Get the number of each color

    # Write the information about the colors to a file
    with open(output_file, "w") as file:
        file.write(f'Number of colors in image = {len(colors_num)}\n\nPixel count by color:\n\n')
        
        n = 0  # Index for iterating over the palette
        color_images = []  # List to store all the images with colors
        for i, (count, _) in enumerate(colors_num):
            # Get the RGB value of the color
            color = (pict_pal[n], pict_pal[n+1], pict_pal[n+2])
            # Convert RGB to HEX
            hex_color = rgb_to_hex(color)
            # Write the information about the color to the file
            file.write(f"{count} {color} {hex_color}\n")
            # Print the information about the color
            print(f"Color {i}: {color} {hex_color} - {count} pixels")

            # Create an image with a sample of the color
            img = Image.new('RGB', (200, 100), color)  # Increase the size of the image for text
            img_drawer = ImageDraw.Draw(img)
            
            # Get the contrast color for the text
            text_color = get_contrast_color(color)
            
            # Text with information about the color
            text = f"Color {i}\nRGB: {color}\nHEX: {hex_color}\nCount: {count}"
            img_drawer.text((10, 10), text, fill=text_color)  # Contrast text
            
            # Save the image
            img.save(f"color_0{i}.png")
            color_images.append(img)  # Add the image to the list
            n += 3  # Move to the next color in the palette

        # Write the final information to the file
        file.write("\n---------------------------------------------\n")
        file.write("image colors counter by nodeus 2018-2025")

        # Create a final image with all the colors
        if color_images:
            # Determine the number of columns and rows for the grid
            num_images = len(color_images)
            cols = 4  # Number of columns in the grid
            rows = (num_images + cols - 1) // cols  # Number of rows

            # Size of each image
            img_width, img_height = color_images[0].size

            # Create a canvas for the final image
            final_image = Image.new('RGB', (cols * img_width, rows * img_height), (255, 255, 255))

            # Paste all the images onto the canvas
            for idx, img in enumerate(color_images):
                x = (idx % cols) * img_width
                y = (idx // cols) * img_height
                final_image.paste(img, (x, y))

            # Save the final image
            final_image.save("all_colors.png")
            print("All the colors saved in all_colors.png")

if __name__ == "__main__":
    # Check the arguments
    if len(sys.argv) > 1:
        # If the second argument is specified, use it as the output file
        output_file = sys.argv[2] if len(sys.argv) > 2 else "count.txt"
        # Call the function to count the colors
        count_colors(sys.argv[1], output_file)
    else:
        # Error message if the arguments are missing
        print("Arguments are missing. The call should be in the format: color-counter.py image.png [output.txt]")

