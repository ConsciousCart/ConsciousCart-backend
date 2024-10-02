import os
from pdf2image import convert_from_path
from PIL import Image

def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the PDF file name without extension
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Convert PDF to a list of images
    images = convert_from_path(pdf_path, dpi=dpi)

    # Save each image
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'{pdf_name}_page_{i+1}.png')
        image.save(image_path, 'PNG')
        print(f'Saved: {image_path}')

def process_pdf_folder(input_folder, output_folder, dpi=300):
    # Get all PDF files in the input folder
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        convert_pdf_to_images(pdf_path, output_folder, dpi)

# Example usage
input_folder = '/home/manasa/Desktop/Code/hackathon/Jun 24'
output_folder = '/home/manasa/Desktop/Code/hackathon/pdf_images/June'

process_pdf_folder(input_folder, output_folder)