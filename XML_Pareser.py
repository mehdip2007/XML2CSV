import csv
import os
from xml.etree import ElementTree as ET
from pathlib import Path


xmlpath = '/Path/To/XML/Files/'
tmp_csv_path = '/Path/To/CSV/'


""" 
    First determine which tags you want to extract the Data and pass the file as an argument to the fuction
    and create a dictionary mapping for converting to CSV by Calling function dict_to_csv which takes a Dictionary 
    and an input argument
"""
def read_xml_attribute(file):
    data_dict = {}

    tree = ET.parse(file)
    root = tree.getroot()

    for child in root:
        if child.attrib:
            _1st_child = child.attrib
            data_dict['NE'] = [_1st_child]
        else:
            for tag in child.findall('TABLE'):
                table_attrname = tag.get('attrname')
                data_dict[table_attrname] = []

                for row in tag.findall('ROWDATA/ROW'):
                    row_data = row.attrib
                    data_dict[table_attrname].append(row_data)

    # pprint(data_dict)
    dict_to_csv(data_dict)



""" 
    Then iterate thru our dictionry which is imported as an argument to our function and use csv.Dictwriter library,
    and for the header since our files header our differs from each other in length need to iterate thru our keys.
"""
def dict_to_csv(dictionary):
    for outer_key, outer_val in dictionary.items():
        with open("{}.csv".format(outer_key), 'w') as file:
            writer = csv.DictWriter(file, fieldnames=[k for k, v in outer_val[0].items()], quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            writer.writerows(outer_val)



""" 
    Since there were too many files per folders, first need to iterate thru all files and get the list of the names from folder
    and create a result one with the same format but with the name of our XML file  but for files we need to use seperate filename
    mentioned in TABLE tag in our XML files. 
"""
def xml_to_csv():
    for root, dirname, files in os.walk(xmlpath):
        for file in files:
            file_name = file
            csv_output_path = "{}{}".format(tmp_csv_path, file_name.strip(".xml"))
            Path(csv_output_path).mkdir(parents=True, exist_ok=True)
            os.chdir(csv_output_path)
            read_xml_attribute("{}{}".format(root, file))


""" 
    in case after you have been told to add new column you can use the following snippet to get your desired tag as a column
"""
def read():
    for filename in os.listdir(tmp_csv_path):
        ident = get_ident("{}{}".format(tmp_csv_path, filename))
        csv_column_append("{}{}".format(tmp_csv_path, filename), ident)


def get_ident(dirs):
    for f in os.listdir(dirs):
        file_path = dirs + "/" + f
        if 'NE.csv' in f:
            with open(file_path, 'r') as file:
                ne_lines = file.readlines()
                identifier = ne_lines[1][10:18].replace(",", "").replace('"', '')

                return identifier


def csv_column_append(dirs, ident):
    for f in os.listdir(dirs):
        file_path = dirs + "/" + f
        if 'NE.csv' not in f:
            with open(file_path, 'r') as read_obj:
                content = read_obj.readlines()
                with open("{}_res.csv".format(file_path.strip(".csv")), 'w') as write_obj:
                    cnt = 0
                    for c in content:
                        if cnt > 0:
                            new_content = ident + "," + c
                            write_obj.write(new_content)
                        else:
                            new_content = "identifier" + "," + c
                            write_obj.write(new_content)
                        cnt += 1



if __name__ == "__main__":
    xml_to_csv()
    read()


""" Execute the following command in the shell in the folder to remove the unncessary files
 ### delete all files EXCEPT the pattern *.txt
  --->  find . -type f ! -name '*_res.csv' -delete
  
"""
