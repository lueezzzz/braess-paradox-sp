import pandas as pd
import numpy as np
import openmatrix as omx
import importlib.util
import sys
from pathlib import Path
from utils import PathUtils

def import_network_from_py(python_file_path: str):
    path = Path(python_file_path)
    if not path.exists():
        raise FileNotFoundError(f"Could not find the data file at: {path.absolute()}")

    module_name = path.stem
    spec = importlib.util.spec_from_file_location(module_name, str(path.absolute()))
    
    if spec is None:
        raise ImportError(f"Could not load spec for {python_file_path}. Is it a valid .py file?")

    data_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = data_module
    spec.loader.exec_module(data_module)
    
    net_df = pd.DataFrame(data_module.network_data)
    demand_df = pd.DataFrame(data_module.demand_data)
    
    return net_df, demand_df


def _net_file2df(network_file: str):
    net_df = pd.read_csv(network_file, skiprows=8, sep='\t')

    trimmed_columns = [s.strip().lower() for s in net_df.columns]
    net_df.columns = trimmed_columns

    net_df.drop(['~', ';'], axis=1, inplace=True)
    return net_df

def _demand_file2trips(demand_file: str):

    f = open(demand_file, 'r')
    all_rows = f.read()
    f.close()
    blocks = all_rows.split('Origin')[1:]
    tripSet = {}
    for k in range(len(blocks)):
        orig = blocks[k].split('\n')
        dests = orig[1:]
        orig = int(orig[0])
        d = [eval('{' + a.replace(';', ',').replace(' ', '') + '}') for a in dests]
        destinations = {}
        for i in d:
            destinations = {**destinations, **i}
        tripSet[orig] = destinations

    return tripSet

def _demand_file2matrix(demand_file: str, omx_write_file_path: str = None):  # Remember .omx

    f = open(demand_file, 'r')
    all_rows = f.read()
    f.close()
    blocks = all_rows.split('Origin')[1:]
    matrix = {}
    for k in range(len(blocks)):
        orig = blocks[k].split('\n')
        dests = orig[1:]
        orig = int(orig[0])
        d = [eval('{' + a.replace(';', ',').replace(' ', '') + '}') for a in dests]
        destinations = {}
        for i in d:
            destinations = {**destinations, **i}
        matrix[orig] = destinations
    zones = max(matrix.keys())

    mat = np.zeros((zones, zones))
    for i in range(zones):
        for j in range(zones):
            # We map values to a index i-1, as Numpy is base 0
            mat[i, j] = matrix.get(i + 1, {}).get(j + 1, 0)

    if omx_write_file_path:
        index = np.arange(zones) + 1
        myfile = omx.open_file(omx_write_file_path, 'w')
        myfile['matrix'] = mat
        myfile.create_mapping('taz', index)
        myfile.close()

    return mat

