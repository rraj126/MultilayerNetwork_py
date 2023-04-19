import pandas as pd
import numpy as np
from typing import List
import warnings

def clean_data(data_array):
    #function to clean data
    #need additional cleaning steps like normalization
    data_array[np.isnan(data_array)] = 0 # type: ignore

    return data_array

def get_sheet_data(f:dict, sheet:str):
    df = f[sheet]

    data_as_array = df.to_numpy()
    processed_data = clean_data(data_as_array)
    data_size = processed_data.shape
    
    return processed_data, data_size

def get_sheet_labels(f:dict, sheet:str, ncols:int, header:bool):
    df = f[sheet]
    
    if header:
        data_labels = list(df.columns.values)
        if len(data_labels) != ncols:
            raise Exception("improper labels")
    else:
        data_labels = ['<ukn>']*ncols

    return data_labels
        

def read_sheet(f:dict, sheet:str, header:bool = True):
    sheet_dict = {}
    
    data_values, data_size = get_sheet_data(f, sheet)
    sheet_dict['values'] = data_values
    sheet_dict['size'] = data_size
    sheet_dict['labels'] = get_sheet_labels(f, sheet, int(data_size[1]), header)

    return sheet_dict

def read_data_file(file_path:str, header:bool = True, sheets:List[str] = []):
    f = pd.read_excel(file_path, None)
    sheet_names_from_file = str(set(f.keys()))
    
    data_dict = {}
    
    if sheets:
        for sheet in sheets:
            if sheet in sheet_names_from_file:
                data_dict[sheet] = read_sheet(f, sheet, header=header)          
            else:
                warnings.warn(f"sheet {sheet} not in file")
    else:
        for sheet in sheet_names_from_file:
            data_dict[sheet] = read_sheet(f, sheet)
        
    return data_dict


def get_unique_data_labels(data_dict:dict):
    list_of_lists = [data_dict[sheet]['labels'] for sheet in data_dict.keys()]
    list_of_labels = []
    for each_list in list_of_lists:
        for each_label in each_list:
            list_of_labels.append(each_label)

    unique_labels = set(list_of_labels)
    nclass = len(unique_labels)

    return unique_labels, nclass
   

def organize_data_with_labels(data_dict:dict):
    unique_labels, nclass = get_unique_data_labels(data_dict)
    data_dims = [data_dict[sheet]['size'][0] for sheet in data_dict.keys()]
    
    if len(set(data_dims)) != 1:
        raise Exception("inconsistent data dimensions")
    else:
        organized_data = {}
        
        for label in unique_labels:
            labeled_data = np.array([], dtype = np.float64).reshape(data_dims[0], 0)
            for sheet in data_dict.keys():
                data_index = [l == label for l in data_dict[sheet]['labels']]
                np.hstack([labeled_data, data_dict[sheet]['values'][:, data_index]])
            
            organized_data[label] = labeled_data

    return organized_data
