#########################################
# This version is coded based on numpy
#########################################

import os
import numpy as np


def DataTransfer(data_str: str, isNeedCopyLastToFirst=False) -> np:
    temp_data_list = []

    # remove \n\t[space] at the begainning and end
    data_str = data_str.strip(' \n\t')

    # transfer str to 2d-list
    for line in data_str.split('\n'):
        temp_data_list.append(line.split('\t'))

    # in some case, the last line will be copy to first to make curve complete
    if isNeedCopyLastToFirst:
        temp_data_list.append(temp_data_list[0])

    # transfer 2d-list to numpy and transpose
    data_numpy = np.array(temp_data_list, dtype=float).T

    return data_numpy