import sys

sys.path.extend(
    [
        "./src/bat-swarm-model/",
        "./src/bat-swarm-model/core/",
        "./src/bat-swarm-model/plot/",
    ]
)
from data_storage.combine_files_post_storage import merge_summary_files

data_storage_dir = "/home/adityamoger/Documents/sensitivity_run_21_10_26_storage/"
merge_summary_files(data_storage_dir, data_storage_dir + "summary_merged.csv")
