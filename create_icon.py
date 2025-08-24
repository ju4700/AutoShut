# from PIL import Image, ImageDraw
import os

def create_icon():
    print("PIL not available, skipping advanced icon creation")
    
    # Create a minimal icon file
    with open('icon.ico', 'w') as f:
        f.write("")  # Empty file - PyInstaller will use default

if __name__ == "__main__":
    print("PIL not available. Creating simple icon...")
    # Create a minimal icon file
    with open('icon.ico', 'w') as f:
        f.write("")  # Empty file - PyInstaller will use default
    print("Placeholder icon created.")
