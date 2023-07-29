import pyautogui
from PIL import ImageGrab
from colorsys import rgb_to_hsv

def find_color(target_color):
    while True:
        # Take a screenshot of the entire screen
        screenshot = ImageGrab.grab()

        # Convert the screenshot to RGB mode
        screenshot = screenshot.convert("RGB")

        # Get the width and height of the screenshot
        width, height = screenshot.size

        for x in range(0, width, 5):
            for y in range(0, height, 5):
                # Get the pixel color at (x, y)
                pixel_color = screenshot.getpixel((x, y))
                r, g, b = pixel_color

                # Convert RGB to HSV for color comparison
                hsv = rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

                # Convert target color to HSV for comparison
                target_hsv = rgb_to_hsv(
                    target_color[0] / 255.0, target_color[1] / 255.0, target_color[2] / 255.0
                )

                # Define the tolerance for color matching (adjust as needed)
                tolerance = 0.1

                # Check if the pixel color matches the target color within the tolerance
                if (
                    abs(hsv[0] - target_hsv[0]) < tolerance
                    and abs(hsv[1] - target_hsv[1]) < tolerance
                    and abs(hsv[2] - target_hsv[2]) < tolerance
                ):
                    # Click the target color
                    pyautogui.click(x, y)

# Specify the target color (RGB format)
target_color_rgb = (255, 0, 0)  # Red color in this example

find_color(target_color_rgb)
