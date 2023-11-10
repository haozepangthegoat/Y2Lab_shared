import dpcentre as dp
import numpy as np


class InitialiseData(dp.RawData):
    """
    Renames raw data
    """

    def __init__(self, file_name_input):
        # renaming
        super().__init__(file_name_input)
        self.time = self.a
        self.axial_temperture = self.b
        self.surface_temperture = self.c


class StepChange(InitialiseData):

    def __init__(self, file_name_input):
        super().__init__(file_name_input)
        self.average_external_temperture = np.mean(self.surface_temperture)


class PeriodicChange(InitialiseData):

    def __init__(self, file_name_input):
        InitialiseData.__init__(self, file_name_input)
        self.peaks = dp.local_maximum(self.axial_temperture)
        self.troughs = dp.local_minimum(self.axial_temperture)
        self.amplitude = self.peaks - self.troughs


