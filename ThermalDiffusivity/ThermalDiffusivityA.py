"""
Last modified:
Author: Haoze Pang, Kieran Tempest

Description
----------
This script calculates the thermal diffusivity using a step change method.

TODOs
----------
TODO: modify calculate_thermal_diffusivity so it calculates err_thermal_diffusivity as well

"""
from general import StepChange
import numpy as np
import dpcentre as dp


class RegressionData(dp.LSFRInitialise):
    """
    Prepare regression data

    Inputs
    ------
    experiment_data (StepChange)

    """
    def __init__(self, experiment_data: StepChange):
        dp.LSFRInitialise.__init__(self)
        self.experiment_data = experiment_data
        # Prepare
        self.prepare_regression()
        # validate input
        self.validate_input()

    def y_error(self):
        """
        Calculates error on y in LSFR
        Returns: err_y
        """
        # initial error
        err_axial_temperture = 1.0e-3
        err_average_external_temperture = 1.0e-3
        # add
        err_addition = dp.AddError(err_a=err_axial_temperture, err_b=err_average_external_temperture)
        err_addition = err_addition.err_z
        # take ln
        err_logarithm = dp.LnError(err_a=err_addition, a=np.log(np.abs(self.experiment_data.axial_temperture -
                                                                       self.experiment_data.average_external_temperture)))
        err_logarithm = err_logarithm.err_z

        self.err_y = err_logarithm

    def x_and_y(self):
        self.x_i = self.experiment_data.time
        self.y_i = np.log(np.abs(self.experiment_data.axial_temperture -
                                 self.experiment_data.average_external_temperture))

    def prepare_regression(self):
        self.y_error()
        self.x_and_y()


def regression(experiment_name: str):
    """
    Performs regression on StepChange

    Args
    ----------
    experiment_name (str):
        name of the raw data file of each experiment

    Returns
    -------
    lsfr (dp.LSFR)
    """
    # set up basic data
    experiment_data = StepChange(experiment_name)   # experiment data
    lsfr_input = RegressionData(experiment_data)    # regression data
    # perform regression
    lsfr = dp.LSFR(lsfr_input)
    # show results and plot lsfr graph
    lsfr.show_result()
    lsfr.plot_graph(f'cooked_data/{experiment_name.removeprefix("raw_data/").removesuffix(".csv")}_lsfr_result.png')

    return lsfr


def calculate_thermal_diffusivity(experiment_name):
    """
    Calculate the thermal diffusivity using the step change method.

    Parameters
    ----------
    experiment_name

    Returns
    -------
    None
    """
    # inputs
    m = regression(experiment_name).m
    lambda_1 = 2.405
    radius = 7.0e-2
    # thermal diffusivity
    thermal_diffusivity = -(radius ** 2 / lambda_1 ** 2) * m
    # print results
    experiment_name = experiment_name.removeprefix('raw_data/').removesuffix('.csv')
    print(f"thermal diffusivity from {experiment_name} is {thermal_diffusivity: .5e}")


if __name__ == '__main__':
    # import files
    experiment1 = "raw_data/ThermalDiffusivity_StepChange_experiment_1.csv"
    experiment2 = "raw_data/ThermalDiffusivity_StepChange_experiment_2.csv"
    # calculate
    calculate_thermal_diffusivity(experiment1)
    calculate_thermal_diffusivity(experiment2)
