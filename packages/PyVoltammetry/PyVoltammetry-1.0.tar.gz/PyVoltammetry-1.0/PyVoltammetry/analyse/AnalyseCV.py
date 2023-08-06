
import os
import sys
import numpy as np
#============================================
sys.path.append(os.path.dirname(__file__))
#============================================
import TransferData
#============================================

class AnalyseCV:

    # ============================================
    E_index = 0  # the column number of potential in data
    I_index = 1  # the column number of current in data
    # ============================================

    def __init__(self):
        self._data_nmupy = None


    # Step 1 : Import data
    # from string variable
    def ImportData(self, data_str:str) -> None:
        # potential-current
        self._data_nmupy = TransferData.DataTransfer(data_str, isNeedCopyLastToFirst=True)
        # print(self._data_nmupy)


    # from txt file
    def ImportDataFromTxt(self, file_path) -> None:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()
                self.ImportData(data)
        else:
            print(f'Failed to locate the file: {file_path}')
            exit(1)


    # Step 2 : Fitting the double-layer (DL) with two linear functions
    def FittingDoubleLayer(self, doubleLayer_range: tuple) -> tuple:

        start_point = doubleLayer_range[0]
        end_point = doubleLayer_range[1]
        start_index_list = []
        end_index_list = []

        # traverse all data list to find out the index(list) of start and end point
        potential_np = self._data_nmupy[AnalyseCV.E_index]

        for i in range(1, len(potential_np)):

            if (potential_np[i-1] - start_point) * (potential_np[i] - start_point) < 0:
                start_index_list.append(i)
            if (potential_np[i-1] - end_point) * (potential_np[i] - end_point) < 0:
                end_index_list.append(i)

        # pick up the pair of index
        DCL_region_indexes_lower = (start_index_list[0], end_index_list[0])
        DCL_region_indexes_upper = (start_index_list[1], end_index_list[1])

        # obtain the points between start and end points
        DCL_region_lower = ((self._data_nmupy.T)[DCL_region_indexes_lower[1] : DCL_region_indexes_lower[0]]).T
        DCL_region_upper = ((self._data_nmupy.T)[DCL_region_indexes_upper[0] : DCL_region_indexes_upper[1]]).T

        # obtain the index/value of extremum of each line
        (DCL_extremum_index_lower, DCL_extremum_lower) = self._FindExtremumInNumpy(
            DCL_region_lower[AnalyseCV.I_index], 'max')
        (DCL_extremum_index_upper, DCL_extremum_upper) = self._FindExtremumInNumpy(
            DCL_region_upper[AnalyseCV.I_index], 'min')

        # For upper line of DCL, fitting the point with linear function
        linear_upper_para = np.polyfit(DCL_region_upper[AnalyseCV.E_index], DCL_region_upper[AnalyseCV.I_index], 1)
        self._linear_upper_func = np.poly1d(linear_upper_para)
        k = linear_upper_para[0]

        # For lower line of DCL, shift the upper function
        linear_lower_para = [k, DCL_region_lower[AnalyseCV.I_index][DCL_extremum_index_lower] - \
                             DCL_region_lower[AnalyseCV.E_index][DCL_extremum_index_lower] * k] # I - E * k
        self._linear_lower_func = np.poly1d(linear_lower_para)

        return (self._linear_lower_func, self._linear_upper_func)


    # Step 3 : Extract data of either Pt-H adsorption or Pt-O reduction peak
    def ExtractPeaks(self, peak:str) -> np:

        # === Extract Data Below DL ===

        potential_np = self._data_nmupy[AnalyseCV.E_index]
        current_np = self._data_nmupy[AnalyseCV.I_index]

        # find all intersection of the CV curve and DCL_lower_func
        intersection_indexes_list = []
        for i in range(1, len(potential_np)):

            d1 = (current_np[i-1] - self._linear_lower_func(potential_np[i-1]))
            d2 = (current_np[i] - self._linear_lower_func(potential_np[i]))
            if d1 * d2 < 0:
                intersection_indexes_list.append(i)


        # the min is frot intersection, and max is back intersection
        intersection_index_front = max(intersection_indexes_list) + 1
        intersection_index_back = min(intersection_indexes_list)

        # split data between intersection from all data
        data_belowDCL_np = ((self._data_nmupy.T)[intersection_index_back : intersection_index_front]).T


        # === Extrat peaks from Data below DL ===

        potential_belowDCL_np = data_belowDCL_np[AnalyseCV.E_index]
        current_belowDCL_np = data_belowDCL_np[AnalyseCV.I_index]

        # calcuate the half length of data below DCL
        half_data_length = int(len(potential_belowDCL_np)/2)

        # Find out the lowerest point of H-peak and O-peak
        (lowest_current_Hpeak_index, lowest_current_Hpeak) = self._FindExtremumInNumpy(
            current_belowDCL_np[half_data_length:], 'min')
        lowest_potential_Hpeak = potential_belowDCL_np[lowest_current_Hpeak_index + half_data_length]

        (lowest_current_Opeak_index, lowest_current_Opeak) = self._FindExtremumInNumpy(
            current_belowDCL_np[:half_data_length], 'min')
        lowest_potential_Opeak = potential_belowDCL_np[lowest_current_Opeak_index]

        # Extract region between the lowest point of H-peak and O-peak
        region_between_O_H_np = ((data_belowDCL_np.T)[lowest_current_Opeak_index:lowest_current_Hpeak_index+half_data_length]).T

        # Find out the point to split H-peak and O-peak
        d_min = 1
        d_min_index = -1
        for i in range(len(region_between_O_H_np[AnalyseCV.I_index])):
            d = self._linear_lower_func(region_between_O_H_np[AnalyseCV.E_index][i]) - \
                region_between_O_H_np[AnalyseCV.I_index][i]
            if d < d_min:
                d_min = d
                d_min_index = i

        split_point_current = region_between_O_H_np[AnalyseCV.I_index][d_min_index]
        split_point_index = self._IndexInNump(data_belowDCL_np[AnalyseCV.I_index], split_point_current)

        self._data_Hpeak_np = ((data_belowDCL_np.T)[split_point_index:]).T
        self._data_Opeak_np = ((data_belowDCL_np.T)[:split_point_index]).T

        # return peak data based on selected peak
        if peak == 'H':
            return self._data_Opeak_np
        else:
            return self._data_Opeak_np


    # Calcuate the peak area
    def CalcuatePeakArea(self, scan_rate:float, peak:str) -> float:

        area = 0

        # Choose peak
        if peak == 'H':
            peak_np = self._data_Hpeak_np
        else:
            peak_np = self._data_Opeak_np


        for i in range(1, len(peak_np[AnalyseCV.I_index])):
            # calculate the gap of two potential point and divided by scan rate, this will give time interval
            x1 = peak_np[AnalyseCV.E_index][i]
            x2 = peak_np[AnalyseCV.E_index][i-1]
            dx = abs((x1 - x2) / scan_rate)

            # when calcuate dy, the value of y need to minus the value of DCL function
            y1 = abs(peak_np[AnalyseCV.I_index][i] - self._linear_lower_func(x1))
            y2 = abs(peak_np[AnalyseCV.I_index][i-1] - self._linear_lower_func(x2))

            area += (y1 + y2) * dx / 2

        return area


    # Export raw data
    def ExportData(self):
        return (self._data_nmupy[AnalyseCV.E_index], self._data_nmupy[AnalyseCV.I_index])



    # ==== private functions ====

    def _FindExtremumInNumpy(self, np_array, type):
        li = np_array.tolist()
        if type == 'max':
            n = max(li)
        else:
            n = min(li)
        return (li.index(n), n)


    def _IndexInNump(self, np_array, n):
        li = np_array.tolist()
        return li.index(n)
