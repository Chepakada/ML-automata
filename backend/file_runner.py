import os
import requests
import time
import glob
import pandas as pd


base_url = "http://127.0.0.1:5000"


files_url = base_url +"/files"

def txt_file(file_path):
    return pd.read_fwf(file_path).to_string()
    
def csv_file(file_path):
    print("good ol' csv")
    return pd.read_csv(file_path)

def xlsx_file(file_path):
    return pd.read_excel(file_path)


extensions = {"txt":txt_file, "csv":csv_file, "xlsx":xlsx_file}



def run_new_delete_old(folder_path):
    files = glob.glob(os.path.join(folder_path, "*"))
    if len(files)<1:
        print("no files found")
        return
    print("rearranging the directory")
    files.sort(key = os.path.getatime, reverse=True)

    newest_file = files[0]

    for file in files[1:]:
        os.remove(file)
        print("deleted old files")
    print(os.path.basename(newest_file))
    return newest_file

def readable_table(file):
    file_name = os.path.basename(file)
    print("reading file")
    print(file_name)

    

    file_ext = file_name.split(".", 1)[1]
    print(file_ext)
    if file_ext in extensions:
       return extensions[file_ext](file)
    else:
        return "not supported"


