import shutil
import pytesseract

# Check if Tesseract is installed
if not shutil.which("tesseract"):
    raise EnvironmentError("Tesseract is not installed or not found in PATH. Please install it following the instructions in the README.")


import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from pathlib import Path

def pdf2image_ocr(pdf_paths, output_file="ocr_results.md"):
    """
    Converts PDF(s) to images, applies OCR, and saves results to a Markdown file.
    
    Parameters:
    - pdf_paths: A single PDF path (str) or a list of PDF paths.
    - output_file: The Markdown file to save OCR results.
    """
    # If a single PDF path is provided as a string, convert it to a list
    if isinstance(pdf_paths, str):
        pdf_paths = [pdf_paths]
    
    # Open the output file in append mode
    with open(output_file, "a") as md_file:
        # Process each PDF in the list
        for pdf_index, pdf_path in enumerate(pdf_paths, start=1):
            # Open the PDF document
            doc = fitz.open(pdf_path)
            # Get the name of the PDF file for documentation in the output
            pdf_name = Path(pdf_path).name
            
            # Log to console that this PDF is being processed
            print(f"Processing PDF {pdf_index} of {len(pdf_paths)}: {pdf_name}")
            # Write a header for this PDF file in the Markdown output
            md_file.write(f"# OCR Results for {pdf_name}\n\n")
            
            # Process each page within the current PDF
            for page_num in range(doc.page_count):
                # Render the page as an image with high resolution (DPI of 300 for OCR accuracy)
                page = doc[page_num]
                pix = page.get_pixmap(dpi=300)
                
                # Convert the rendered image to a format compatible with OCR (PIL Image)
                img = Image.open(io.BytesIO(pix.tobytes("png")))

                # Perform OCR on the image to extract text
                text = pytesseract.image_to_string(img)

                # Write the extracted text to the Markdown file with page-specific heading
                md_file.write(f"## Page {page_num + 1}\n\n")
                md_file.write(text + "\n\n")
                
                # Log to console that this page has been processed
                print(f"  - Processed page {page_num + 1} of {doc.page_count} in {pdf_name}")
            
            # Close the document after processing all its pages
            doc.close()
            # Log to console that this PDF has been fully processed
            print(f"Finished processing {pdf_name}\n")

    # Final log message to confirm all results have been saved
    print(f"OCR results have been saved to {output_file}")


### function to capture only the text and not save to md file

# Check if Tesseract is installed
if not shutil.which("tesseract"):
    raise EnvironmentError("Tesseract is not installed or not found in PATH. Please install it following the instructions in the README.")

def pdf2image_ocr_text(pdf_paths):
    """
    Converts PDF(s) to images, applies OCR, and returns the OCRed text as a single string.

    Parameters:
    - pdf_paths: A single PDF path (str) or a list of PDF paths.

    Returns:
    - str: A single string containing the OCRed text, with each page prefixed by its filename and page number.
    """
    # If a single PDF path is provided as a string, convert it to a list
    if isinstance(pdf_paths, str):
        pdf_paths = [pdf_paths]
    
    # Initialize a variable to hold all OCR results as a single string
    ocr_results = ""

    # Process each PDF in the list
    for pdf_index, pdf_path in enumerate(pdf_paths, start=1):
        # Open the PDF document
        doc = fitz.open(pdf_path)
        # Get the name of the PDF file without the extension
        pdf_name = Path(pdf_path).stem

        # Log to console that this PDF is being processed
        print(f"Processing PDF {pdf_index} of {len(pdf_paths)}: {pdf_name}")
        
        # Process each page within the current PDF
        for page_num in range(doc.page_count):
            # Render the page as an image with high resolution (DPI of 300 for OCR accuracy)
            page = doc[page_num]
            pix = page.get_pixmap(dpi=300)
            
            # Convert the rendered image to a format compatible with OCR (PIL Image)
            img = Image.open(io.BytesIO(pix.tobytes("png")))

            # Perform OCR on the image to extract text
            text = pytesseract.image_to_string(img)

            # Add the title and text for the page to the results
            page_title = f"{pdf_name}_page_{page_num + 1}"
            ocr_results += f"## {page_title}\n{text}\n\n"
            
            # Log to console that this page has been processed
            print(f"  - Processed page {page_num + 1} of {doc.page_count} in {pdf_name}")
        
        # Close the document after processing all its pages
        doc.close()
        # Log to console that this PDF has been fully processed
        print(f"Finished processing {pdf_name}\n")

    # Final log message to confirm all processing is complete
    print("All PDFs have been processed.")
    
    return ocr_results



