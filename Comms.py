import PyPDF2
import re

class Comms:
    def __init__(self, pdf):
        self.pdf = pdf
        self.pages = 0
        self.data = []

    def read(self):
        with open(self.pdf, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            self.pages = reader.numPages

            for i in range(self.pages):
                page = reader.getPage(i).extractText()
                page = page.split("\n")
                self.data.append(self.clean(page))
                


    def clean(self, page_array):
        # Remove Header
        del page_array[:5]

        # Create a list for the column names
        x_axis = page_array[:7]

        # Remove column titles and trailing info
        del page_array[:7]
        del page_array[-4:]

        # Loop through list and build a new list with clean data
        df = []
        for i in range(len(page_array)):
            if i != 0 and i % 7 == 0:
                # First row
                if i == 7:
                    # Clean the $ off the last two columns
                    if page_array[i-2][0] == "$":
                        page_array[i-2] = page_array[i-2][1:]
                        
                    if page_array[i-1][0] == "$":
                        page_array[i-1] = page_array[i-1][1:]

                    # Check the values of the data
                    tmp = page_array[:7]
                    # If the value is okay, append it to the data frame
                    if self.check_vals(tmp, i):
                        df.append(page_array[:7])
                    else:
                        break
                else:
                    # If there is a space after the program name, this is because there is a word wrap.
                    # The next index will be the rest of the name, so we need to add the following
                    # value to the current one, then delete the following value from the list
                    if page_array[i - 5][-1] == " " or page_array[i - 5][-1] == "-":
                        page_array[i - 5] = page_array[i - 5] + page_array[i - 4]
                        del page_array[i - 4]
                    
                    # Clean the $ off the last two columns
                    if page_array[i-2][0] == "$":
                        page_array[i-2] = page_array[i-2][1:]
                        
                    if page_array[i-1][0] == "$":
                        page_array[i-1] = page_array[i-1][1:]

                    tmp = page_array[i-7:i]
                    if self.check_vals(tmp, i, ):
                        df.append(page_array[i-7:i])

        return df


    def check_vals(self, tmp, current_val):
        # Pattern [Group Number, BIN, Program, Date, Utilization, Rate, Ammount]
        if not re.match(r'^[A-Z\d]*$', tmp[0]):
            print("Error: Incorrect Group Number - {}".format(tmp[0]))
            return False
            
        if not re.match(r'^[0-9]*$', tmp[1]):
            print("Error: Incorrect Bin Number - {}".format(tmp[1]))
            return False
        
        if not re.match(r'^[A-Za-z0-9-.\' ]*$', tmp[2]):
            print("Error: Incorrect Program Name - {}".format(tmp[2]))
            return False
        
        if not re.match(r'([0-9]{1,2}\/[0-9]{1,2})', tmp[3]):
            print("Error: Incorrect Date - {}".format(tmp[3]))
            return False
            
        if not re.match(r'^[0-9]*$', tmp[4]):
            print("Error: Incorrect Utilization Number - {}".format(tmp[4]))
            return False        
            
        if not re.match(r'^(\d(,\d{3})*|(\d+))(\.\d{2})$', tmp[5]):
            print("Error: Incorrect Rate Number - {}".format(tmp[5]))
            return False
            
        if not re.match(r'^(\d(,\d{3})*|(\d+))(\.\d{2})$', tmp[6]):
            print("Error: Incorrect Payout Number - {}".format(tmp[6]))
            return False
        return True

