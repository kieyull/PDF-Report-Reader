import PyPDF2
import re
import pandas as pd

pdf = open('sept18.pdf', 'rb')
reader = PyPDF2.PdfFileReader(pdf)
pages = reader.numPages

first_page = reader.getPage(0)
first_page_text = first_page.extractText()
info = re.findall(r'\b([\w/.,#\' ]*)\n', first_page_text)

# Remove the beginning data
del info[:5]

# Create a list for the column names
x_axis = info[:7]

# Remove column titles and trailing info
del info[:7]
del info[-3:]

def check_vals(tmp, current_val):
    # Pattern [Group Number, BIN, Program, Date, Utilization, Rate, Ammount]
    if not re.match(r'^[A-Z\d]*$', tmp[0]):
        print("Error: Incorrect Group Number - {}".format(tmp[0]))
        del info[current_val - 6]
        return False
        
    if not re.match(r'^[0-9]*$', tmp[1]):
        print("Error: Incorrect Bin Number - {}".format(tmp[1]))
        del info[current_val - 5]
        return False
        
    if not re.match(r'^[A-Za-z-.\' ]*$', tmp[2]):
        print("Error: Incorrect Program Name - {}".format(tmp[2]))
        del info[current_val - 4]
        return False
    
    if not re.match(r'([0-9]\/[0-9])', tmp[3]):
        print("Error: Incorrect Date - {}".format(tmp[3]))
        del info[current_val - 3]
        return False
        
    if not re.match(r'^[0-9]*$', tmp[4]):
        print("Error: Incorrect Utilization Number - {}".format(tmp[4]))
        del info[current_val - 2]
        return False
    
    if not re.match(r'^(\d{2}(,\d{3})*|(\d+))(\.\d{2})$', tmp[5]):
        print("Error: Incorrect Rate Number - {}".format(tmp[5]))
        del info[current_val - 1]
        return False
        
    if not re.match(r'^(\d{2}(,\d{3})*|(\d+))(\.\d{2})$', tmp[6]):
        print("Error: Incorrect Payout Number - {}".format(tmp[6]))
        del info[current_val]
        return False
    return True

df = []
for i in range(len(info)):
    if i != 0 and i % 7 == 0:
        if i == 7:
            # Check the values of the data
            tmp = info[:7]
            if check_vals(tmp, i):
                df.append(info[:7])
            else:
                break
        else:
            tmp = info[i-7:i]
            if check_vals(tmp, i):
                df.append(info[i-7:i])

comms_df = pd.DataFrame(df, columns=x_axis)