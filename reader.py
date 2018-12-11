import PyPDF2
import re
import pandas as pd

pdf_obj = open('sept18.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_obj)
pages = pdf_reader.numPages

first_page = pdf_reader.getPage(0)
first_page_text = first_page.extractText()

info = re.findall(r'\b([\w/.,#\' ]*)\n', first_page_text)

# Remove the beginning data
del info[:5]

# Create a list for the column names
x_axis = info[:7]

# Remove column titles and trailing info
del info[:7]
del info[-3:]

# Build lists for all data
# groups = info[::5]
# bins = info[1::5]
# utilization = info[2::5]
# rate = info[3::5]
# payout = info[4::5]