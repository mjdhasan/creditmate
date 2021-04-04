# existing tools
# - pdftron.com (licensing kicks in when you are ready to deploy to production)
# - docparser
# - tabula
# - pdftables.com


from init import DIR_DUMPS
import os
l_files = os.listdir(DIR_DUMPS)
filename = [file for file in l_files if ('.pdf' in file) and ('scb' in file)][0]
pdf_path = f'{DIR_DUMPS}/{filename}'

import pdf2md

import pdftotree
pdf_html = pdftotree.parse(pdf_path, favor_figures=True, visualize=True)
html_file = open('pdftohtml_test.html', 'w')
html_file.write(pdf_html)
html_file.close()

dir(pdftotree)
pdftotree.ml

import camelot
pdf_camelot = camelot.read_pdf(pdf_path)


from depdf import DePDF, DePage, Config

c = Config(
    debug_flag=True,
    verbose_flag=True,
    add_line_flag=True
)
pdf = DePDF.load(pdf_path, config=c)
dir(pdf)
pdf.extract_html_pages()
pdf.to_html()
len(pdf.pages)
dir(pdf.pages[0])
pdf.pages[3].to_dict.keys()
[phrase for phrase in pdf.pages[3].to_dict['extract_phrases']()]
l_para = pdf.pages[3]._paragraphs
dir(l_para[0])
l_para[3].soup
# pdf.extract_page_paragraphs()
pdf.to_soup('html')
print(pdf.pages[3].soup)

with DePDF.load(pdf_path) as pdf:
    pdf_html = pdf.to_html
    print(pdf_html)


import tabula
dir(tabula)
# l_tables = tabula.read_pdf_with_template(pdf_path, pages='all', multiple_tables=True, stream=True) #  output_format='json'

l_tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)  # , stream=True output_format='json'
len(l_tables)
l_tables[5]
l_tables[0].loc[16]
dir(l_tables[0])
l_tables[5]
l_tables[0].keys()
l_tables[0]['data']
len(l_tables[0]['data'])
l_tables[0]['data'][0]

import pdfplumber
import json
pdf_doc = pdfplumber.open(pdf_path)
dir(pdf_doc)
pdf_doc.annots
dir(pdf_doc.pages[0])
pdf_doc.pages[4].bbox
json.loads(pdf_doc.pages[4].to_json()).keys()
json.loads(pdf_doc.pages[2].to_json())['images']
print(pdf_doc.pages[4].extract_text())
print(pdf_doc.pages[6].extract_tables())
l_tables = pdf_doc.pages[6].extract_tables()
len(l_tables)
dir(l_tables[0])
l_tables[0].encode('ascii', 'replace')
len(l_tables[0])
l_tables[0][3]
row = l_tables[0][1]
row[6].decode("utf-8")
l_tables[0][3][1].replace(u'\xa0', u' ').replace(u'\n', '')

# extract_pdf_tables(pdf_path)

import pandas as pd
row_num = 0
for row in l_tables[0]:
    l_items = []
    for item in row:
        if item is not None:
            l_items = l_items + [item.replace(u'\xa0', u' ').replace(u'\n', '')]
        else:
            l_items = l_items + ['']
    if row_num == 0:
        df = pd.DataFrame(columns=l_items)
    else:
        df.loc[row_num] = l_items
    row_num = row_num + 1



pdf_doc.pages[4].objects.keys()
pdf_doc.pages[4].objects[0]
pdf_doc.pages[4].objects['curve'][0]
pdf_doc.pages[6].images
print(pdf_doc.pages[6].extract_text())
pdf_doc.pages[6].crop((25, 100, 50, 200)).extract_text()

import matplotlib.pyplot as plt
pdf_doc.pages[4].bbox
len(pdf_doc.pages[4].curves)

page_num = 4
curve_num = 0
pdf_doc.pages[page_num].curves[curve_num]['x1']
pdf_doc.pages[page_num].curves[curve_num + 1]['x0']
image = pdf_doc.pages[page_num].crop((pdf_doc.pages[page_num].curves[curve_num]['x0'],
                                      pdf_doc.pages[page_num].curves[curve_num]['top'],
                                      pdf_doc.pages[page_num].curves[curve_num]['x1'],
                                      pdf_doc.pages[page_num].curves[curve_num]['bottom']),
                                     relative=False
                                     ).to_image()
image.save('./cropped_pdf_image.png')

plt.imshow(image)

pdf_doc.pages[0].extract_text()
pdf_doc.pages[0].cropbox

import pdfplumber
import json
import img2pdf
# import pdf2image
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter  #, PDFPa , PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal, LTCurve, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from PIL import Image

# pdf2image.convert_from_path()
document = open(pdf_path, 'rb')
plumber_doc = pdfplumber.open(pdf_path)
parser = PDFParser(document)
# table of content
parsed_doc = PDFDocument(parser, password='')
# dir(parsed_doc)
# parsed_doc.info
# parsed_doc.is_extractable
# parsed_doc.get_outlines()
#Create resource manager
rsrcmgr = PDFResourceManager()
# # Set parameters for analysis.
# laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
interpreter = PDFPageInterpreter(rsrcmgr, device)
l_pages = [page for page in PDFPage.get_pages(document)]
print('Number of pages: ', len(l_pages))
page_num = 0
l_text = []
for page in l_pages:
    print(f'page_num: {page_num}')
    dir(page)
    # page.attrs['MediaBox']
    # page.attrs['CropBox']
    dir(plumber_doc.pages[page_num])
    interpreter.process_page(page)
    # receive the LTPage object for the page.
    layout = device.get_result()
    l_elements = [element for element in layout]
    l_element_types = [type(element) for element in layout]
    l_figures = [element for element in layout if isinstance(element, LTFigure)]
    element = l_figures[36]
    # len(l_elements)
    elem_num = 0
    for element in l_elements:
        print(f'elem_num: {elem_num}')
        # element.bbox
        # print(type(element))
        if isinstance(element, LTTextBoxHorizontal):
            # print(element.get_text())
            l_text = l_text + [element.get_text()]
        if isinstance(element, LTFigure):
            # element.bbox
            # element._objs
            image = plumber_doc.pages[page_num].crop((element.bbox[0],
                                                      page.attrs['MediaBox'][3] - element.bbox[3],
                                                      element.bbox[2],
                                                      page.attrs['MediaBox'][3] - element.bbox[1])
                                                     ).to_image(resolution=720)
            image.save('./output/cropped_pdf_image.png')
            with open('./output/cropped_pdf_image.pdf', 'wb') as f:
                f.write(img2pdf.convert('./output/cropped_pdf_image.png'))

            # doc_img = open('./output/cropped_pdf_image.pdf', 'rb')
            # l_pages_ = [page for page in PDFPage.get_pages(doc_img)]
            # print('Number of pages: ', len(l_pages_))
            # for page in l_pages_:
            #     interpreter.process_page(page)
            #     # receive the LTPage object for the page.
            #     layout = device.get_result()
            #     l_elements = [element for element in layout]
            #     l_element_types = [type(element) for element in layout]

            # print(f'i: {i}; {element}')
            # dir(element)
            # element.getvalue()

        elem_num = elem_num + 1
    page_num = page_num + 1


