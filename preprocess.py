import pandas as pd
import numpy as np
from typing import List
import warnings

def read_sheet(f:dict, sheet:str, header:bool = True):
    sheet_dict = {}
    
    df = f[sheet]
    data_as_array = df.to_numpy()
    data_as_array[np.isnan(data_as_array)] = 0
    
    sheet_dict['values'] = data_as_array
    
    if header:
        sheet_dict['labels'] = list(df.columns.values)
    else:
        sheet_dict['labels'] = None
        
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