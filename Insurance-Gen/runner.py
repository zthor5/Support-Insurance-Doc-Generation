import csv
import os
from pdfrw import PdfWriter, PdfReader, IndirectPdfDict, PdfName, PdfDict

INPUT_CSV_FILE = 'Insert-csvFile/input.csv'
TEMPLATE_LOCATION = 'templates/Master.pdf'
OUTPUT_START_PATH = 'Output-Goes-Here/'

data_names= ["Group_Z","Address_Z","City_Z","Zip_Code_Z"]
#Will be replaced with actual data
data_dict = ["Group_Z","Address_Z","City_Z","Zip_Code_Z"]

insured_name = ""

def handle_rows():
    try:
        with open(INPUT_CSV_FILE, encoding='utf-8-sig') as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                if any(row):
                    if not row[1].strip():
                        insured_name = row[0]
                    else:
                        input_row_order = list(row)
                        create_ideal_row(input_row_order)
                        fill_fields(OUTPUT_START_PATH + insured_name + "-Property Certificate-" + data_dict[0] +  '.pdf', data_dict)
    except:
        f = open (OUTPUT_START_PATH + "READ_THIS!_AND_SEND_TO_DEV.txt", "a")
        f.write("Unable to read the format of the input.csv, Please send the input.csv to the DEV." + "\n" + "Sorry!")
        f.close()

def create_ideal_row(input_row):
    result = input_row
    data_dict[0] = result[0]
    data_dict[1] = result[1]
    data_dict[2] = result[2]
    data_dict[3] = result[3] + " " + result[4]

def fill_fields(output_path, data_dict):
    data_dict_cur_pos = -1
    POSITION = 0
    template_pdf = PdfReader(TEMPLATE_LOCATION)
    for name in template_pdf.Root.AcroForm.Fields:
        # Removing the leading and ending parenthesis's
        name = (str(name.T)[1:len(name.T) - 1])
        if name in data_names:
            #print("Found you!")
            data_dict_cur_pos = data_names.index(name)
            template_pdf.Root.AcroForm.Fields[POSITION].V = data_dict[data_dict_cur_pos]
            print(template_pdf.Root.AcroForm.Fields[POSITION].V)
            #this depends on page orientation
            rct = template_pdf.Root.AcroForm.Fields[POSITION].Rect
            height = round(float(rct[3]) - float(rct[1]),2)
            width = round(float(rct[2]) - float(rct[0]),2)

            #create Xobject
            xobj = IndirectPdfDict(BBox = [0, 0, width,height],
            FormType = 1,
            Resources = PdfDict(ProcSet = [PdfName.PDF, PdfName.Text]),
            Subtype = PdfName.Form,
            Type = PdfName.XObject
            )
            #assign a stream to it
            xobj.stream = '''/Tx BMC
            BT
             /Arial 7.0 Tf
             1.0 5.0 Td
             0 g
             (''' + data_dict[data_dict_cur_pos] + ''') Tj
            ET EMC'''

            #put all together
            template_pdf.Root.AcroForm.Fields[POSITION].AP = PdfDict(N = xobj)
            POSITION += 1
            #print("Pos is " + str(POSITION) +". Congrats for making it here!")
            #output to new file
            PdfWriter().write(output_path, template_pdf)

        else:
            POSITION += 1

if __name__ == '__main__':
    handle_rows()
