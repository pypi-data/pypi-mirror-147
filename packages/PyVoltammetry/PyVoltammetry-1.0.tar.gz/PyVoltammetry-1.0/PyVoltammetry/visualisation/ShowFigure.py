import matplotlib.pyplot as plt
import os
import sys
import io
#============================================
sys.path.append(os.path.dirname(__file__))
#============================================
from ..analyse import AnalyseCV
#============================================


class ShowFigure:

    def __init__(self, AnalyseCV:AnalyseCV):

        self._cv = AnalyseCV

        self._raw_data = self._cv.ExportData()
        self._raw_E = self._raw_data[AnalyseCV.E_index]
        self._raw_I = self._raw_data[AnalyseCV.I_index]

        self.figure = plt
        self.figure.xlabel('Potential / V vs RHE')
        self.figure.ylabel('Current / A')


    # Add original data
    def AddRawData(self, colour='r'):
        self.figure.plot(self._raw_E,
                          self._raw_I,
                          color=colour)


    # Add two linear functions of double-layer
    def AddDoubleLayer(self, colour='b'):
        self.figure.plot(self._raw_E,
                          self._cv._linear_lower_func(self._raw_E),
                          color=colour)
        self.figure.plot(self._raw_E,
                          self._cv._linear_upper_func(self._raw_E),
                          color=colour)


    # Fill the colour in Pt-H or Pt-O peak or two upper peaks
    def FillPeak(self, peak:str, colour='y'):
        if peak == 'H' or peak == 'O':
            if peak == 'H':
                data = self._cv._data_Hpeak_np
            else:
                data = self._cv._data_Opeak_np

            self.figure.fill_between(data[AnalyseCV.E_index],
                                      self._cv._linear_lower_func(data[AnalyseCV.E_index]),
                                      data[AnalyseCV.I_index],
                                      color=colour)
        else:
            self.figure.fill_between(self._raw_E,
                                      self._raw_I,
                                      self._cv._linear_upper_func(self._raw_E),
                                      where=self._raw_I > self._cv._linear_upper_func(self._raw_E),
                                      color=colour)

    # Show figure
    def Show(self):
        self.figure.show()


    # Export figure as bytes
    def ExportToBytes(self):
        buffer = io.BytesIO()
        buffer.seek(0, 0)
        self.figure.savefig(buffer, format='png')
        data = buffer.getvalue()
        buffer.close()
        return data


    # Release the figure
    def Close(self):
        self.figure.close()