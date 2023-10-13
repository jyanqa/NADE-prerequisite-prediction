from PyPDF2 import PdfReader

# Replace 'input.pdf' with the name of your PDF file
pdf_file_path = 'input.pdf' 

# Replace 'output.txt' with the name of the TXT file you want to create
txt_file_path = '/Users/Jyanqa/Desktop/thesis/prerequisite-text-extracttion/'

reader = PdfReader("input.pdf")
number_of_pages = len(reader.pages)
for i in range(0, 3):
    page = reader.pages[i]
    text = page.extract_text()
    print(text) #string