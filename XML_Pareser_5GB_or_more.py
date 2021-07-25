from xml.etree import ElementTree as ET
import os
import pandas as pd
from datetime import datetime
from itertools import islice


def chunks(data, size=10000):
    it = iter(data)
    for i in range(0, len(data), size):
        yield {k: data[k] for k in islice(it, size)}


print("Start ---> ", datetime.now())


def dict_to_csv(di, filename):
    df = pd.DataFrame.from_dict(di, orient='index').T
    csv_result = '{}.csv'.format(filename)

    # since we are using append mode need to be sure the header for another dataframes are not in our data
    # need check whether the file exists or not if exists we can start from the second line
    if not os.path.isfile(csv_result):
        df.to_csv(csv_result, header=[k for k, v in di.items()], index=False, chunksize=1000)
    else:
        df.to_csv(csv_result, mode='a', header=False, index=False, chunksize=1000)


def xml_parser(file):
    # Read XML file tag by tag using iterparse and create a dictionary for our dataframe
    context = ET.iterparse(file, events=("start", "end"))

    for event, element in context:
        if element.tag == "<your desire tag>":

            # chunking the dictionary for creating data frame
            for item in chunks(element.attrib):
                d = {}
                _class = []
                distname = []
                version = []
                _id = []
                name = []

                # loop thru chucked dictionary
                for k, v in item.items():
                    if k == 'attrib1':
                        _class.append(v)
                    if k == 'attrib2':
                        distname.append(v)
                    if k == 'attrib3':
                        version.append(v)
                    if k == 'attrib4':
                        _id.append(v)
                    if k == 'attrib5':
                        name.append(v)

                d['attrib1'] = _class
                d['attrib2'] = distname
                d['attrib3'] = version
                d['attrib4'] = _id
                # print(d)

                # create a csv from our dictionary
                dict_to_csv(d, '/path/to/your/csv/data')
                # dict_to_csv(d, '/Users/mehdi/PycharmProjects/Discovery/Radio/asb')


        # make sure to use clear funtion to not to destroy your RAM
        element.clear()
        print("END ---> ", datetime.now())


if __name__ == "__main__":
    xml_parser('/path/to/your/data.xml')
    # xml_parser('/Users/mehdi/Desktop/xml_sample.xml')
