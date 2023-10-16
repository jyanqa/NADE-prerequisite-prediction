import os
from PyPDF2 import PdfReader

# Replace this with the directory path where your PDF files are located
pdf_directory = '/Users/Jyanqa/Desktop/thesis/prerequisite-text-extracttion/LectureBank-crawling/pdf2txt-pptx2txt/pdf/'
txt_file_path = '/Users/Jyanqa/Desktop/thesis/prerequisite-text-extracttion/LectureBank-crawling/pdf2txt-pptx2txt/'+ 'output.txt'
# Loop through files in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        full_path = os.path.join(pdf_directory, filename)
        # Process the PDF file
        with open(full_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            number_of_pages = len(reader.pages)
            for i in range(0, number_of_pages):
                page = reader.pages[i]
                text = page.extract_text()
                with open(txt_file_path, 'a') as f:   
                    f.write(text)           # write text to txt file 
                    f.write('\n')           # add new line
        # Close the PDF file when done
        pdf_file.close()
