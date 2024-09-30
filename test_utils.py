import os
from utils import convert_pdf_to_images, process_images_with_gemini
from PIL import Image
import io

# Test the convert_pdf_to_images function
def test_convert_pdf_to_images():
    # Ensure you have a sample PDF file in the same directory as this script
    pdf_path = "sample.pdf"
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found. Please ensure the sample PDF file exists.")
        return

    with open(pdf_path, "rb") as f:
        pdf_content = f.read()

    images = convert_pdf_to_images(pdf_content)
    print(f"Number of images generated: {len(images)}")

    # Optionally, save the first image to verify content
    if images:
        first_image = Image.open(io.BytesIO(images[0]))
        first_image.save("first_page.png")
        print("First page saved as 'first_page.png'")

# Test the process_images_with_gemini function
def test_process_images_with_gemini():
    image_path = "first_page.png"  # Use the image generated from the PDF
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found. Please run the PDF conversion test first.")
        return

    with open(image_path, "rb") as f:
        image_content = f.read()

    result = process_images_with_gemini([image_content])
    print(f"Gemini processing result:\n{result[:500]}...")  # Print first 500 characters # Print first 500 characters

if __name__ == "__main__":
    print("Testing convert_pdf_to_images function:")
    test_convert_pdf_to_images()
    print("\nTesting process_images_with_gemini function:")
    test_process_images_with_gemini()