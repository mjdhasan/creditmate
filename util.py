from pyhtml2pdf import converter
import os
import pdfkit
from init import DIR_DUMPS

# l_files = os.listdir(DIR_DUMPS)
# filename = [file for file in l_files if ('.html' in file) and ('scb' in file)][0]
# file_path = os.path.join(DIR_DUMPS, filename)
def convert_html_to_pdf(file_path):
    filename, file_extension = os.path.splitext(file_path)
    # converter.convert(f'{file_path}',
    #                   f'{filename}.pdf',
    #                   install_driver=True)
    pdfkit.from_file(f'{file_path}', f'{filename}.pdf')
    pdfkit.from_url('http://www.google.com', 'google.pdf')
    pdfkit.from_url('https://www.sc.com/sg/wealth/investment/', 'output/sc.pdf')

