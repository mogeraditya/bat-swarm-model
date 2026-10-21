import glob
import gzip
import pickle

import h5py
import numpy as np
import pandas as pd
from supporting_files.utilities import load_parameters, make_dir
from tqdm.rich import tqdm


def stitch_together_pickle_history_lists_and_store(
    history_output_dir, dir_to_store, id_for_simulation
):
    """Merges lists from all the pickle files together.

    Args:
        history_output_dir (string):

    Returns:
        list: list with all the merged lists from pickle files.
    """

    list_of_dict_files = glob.glob(history_output_dir + "/history_dump_*.pkl.gz")
    list_of_dict_files = np.sort(list_of_dict_files)

    list_containing_data_from_all_pickle_files = []
    for pickle_file in tqdm(list_of_dict_files, desc="reading dict files "):
        with gzip.open(pickle_file, "rb") as f:
            _list_containing_subset = pickle.load(f)
            list_containing_data_from_all_pickle_files.extend(_list_containing_subset)
    print(id_for_simulation)
    parameter_file = glob.glob(history_output_dir + "/parameters_used.json")[0]
    parameter_df = load_parameters(parameter_file)
    print(parameter_df)
    times = [i["time"] for i in list_containing_data_from_all_pickle_files]
    sorting_indices = np.argsort(times)
    list_containing_data_from_all_pickle_files = np.array(
        list_containing_data_from_all_pickle_files
    )
    list_containing_data_from_all_pickle_files = (
        list_containing_data_from_all_pickle_files[sorting_indices]
    )
    # list_containing_data_from_all_pickle_files.append(parameter_df)
    np.append(list_containing_data_from_all_pickle_files, parameter_df)
    make_dir(dir_to_store)
    with gzip.open(dir_to_store + f"/history_{id_for_simulation}.pkl.gz", "wb") as f:
        pickle.dump(list_containing_data_from_all_pickle_files, f)
    return list_containing_data_from_all_pickle_files


def load_history_dump(file_path):
    """Load data from an HDF5 file saved by handle_data_storage_for_plotting.

    Args:
        file_path (str): Path to the .h5 file (e.g., "history_dump_001234567.h5")

    Returns:
        dict: Dictionary containing all stored data (arrays and attributes)
    """
    data = {}
    with h5py.File(file_path, "r") as f:
        # Load datasets (arrays)
        for key in f.keys():
            data[key] = f[key][:]
        # Load attributes (non-array metadata)
        for key in f.attrs.keys():
            data[key] = f.attrs[key]
    return data


def merge_csvs(input_folder, output_file):
    files = glob.glob(f"{input_folder}/**/**/*.csv", recursive=True)
    if not files:
        print("No CSV files found")
        return
    pd.concat([pd.read_csv(f) for f in files]).to_csv(output_file, index=False)
    print(f"Merged {len(files)} files into {output_file}")
