import os
import pandas as pd


tmp_csv_path = '/path/to/CSV/already/generated/OSS10/'
final_csv_path = '/path/to/merge/result//'

# create an empty dataframe to compare with the previous dataframe used in read file
temp_df = pd.DataFrame()

def compare(file1, file_name):
    global temp_df

    df2 = pd.read_csv(file1, skip_blank_lines=True)
    frames = [temp_df, df2]
    ndf = pd.concat(frames)
    temp_df = ndf
    ndf.to_csv("{}{}".format(final_csv_path, file_name),index=False)


# if your files like mine our too much(18K CSV) you might want to chuck up your files list to not to destroy your RAM.  
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def read_each_file(files_list):
    for chunk in chunks(files_list, 170):
        for i in range(len(chunk)):
            printProgressBar(i, len(chunk))
            filename = "".join(chunk[i].split('/')[-1])
            compare(chunk[i], filename)


"""
    since we have similar files by name in each folder, its a good idea to create a dictionary with file as a key with value 
    which contains a list folder names
"""
def read_same_files_in_multiple_folder(dirs):
    global temp_df
    file_list = {}

    for dirname in os.listdir(dirs):
        for root, dirs, files in os.walk(tmp_csv_path + dirname):
            for filename in files:
                if filename not in file_list:
                    file_list[filename] = []
                file_list[filename].append(os.path.join(root, filename))

    for filename, files in file_list.items():
        read_each_file(files)
        temp_df = pd.DataFrame()


if __name__ == "__main__":
    read_same_files_in_multiple_folder(tmp_csv_path)
