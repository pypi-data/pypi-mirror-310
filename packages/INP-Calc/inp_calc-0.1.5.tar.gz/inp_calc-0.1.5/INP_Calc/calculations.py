from math import log, pi
import numpy as np

def FF_to_conc(ff, volume, concentration):
    return_list = []
    for i in ff:
        if 0 < i < 1:  # Ensure that 1 - i is positive
            result = -np.log(1 - i) / (volume * concentration)  # Use np.log for logarithm
            return_list.append(result)
        else:
            return_list.append(float('nan'))  # Append NaN for invalid values
    return return_list

def FF_to_volume(ff, diameter, volume, concentration):
    return_list = []
    for i in ff:
        if 0 < i < 1:  # Ensure that 1 - i is positive
            return_list.append(-log(1 - i) / (volume * concentration * (4/3) * pi * ((diameter/2) ** 3)))
        else:
            return_list.append(float('nan'))  # Append NaN for invalid values
    return return_list

def FF_to_surface(ff, diameter, volume, concentration):
    return_list = []
    for i in ff:
        if 0 < i < 1:  # Ensure that 1 - i is positive
            return_list.append(-log(1 - i) / (volume * concentration * 4 * pi * ((diameter / 2) ** 2)))
        else:
            return_list.append(float('nan'))  # Append NaN for invalid values
    return return_list

def FF_to_mass(ff, volume, mass_concentration):
    return_list = []
    for i in ff:
        if 0 < i < 1:  # Ensure that 1 - i is positive
            return_list.append(-log(1 - i) / (volume * mass_concentration))
        else:
            return_list.append(float('nan'))  # Append NaN for invalid values
    return return_list


def calculateDifferentialSpectra(temperatures, V, delta_T):
    """
    Calculate k(T) values for binned temperature data from -40 to 0.

    Parameters:
    V (float): Volume of droplets (constant).
    temperatures (list of float): List of temperature values.
    delta_T (float): Size of the interval.

    Returns:
    temp_bins (list of float): List of bin midpoints for the chart.
    Diff_Nuclei_Conc (list of float): Calculated k(T) values corresponding to the bin midpoints.
    """
    # Define bin edges from -40 to 5 with the specified delta_T
    bin_edges = np.arange(-40, 6, delta_T)

    # Create bins for the temperatures
    counts, _ = np.histogram(temperatures, bins=bin_edges)

    temp_bins = []
    Diff_Nuclei_Conc = []

    # Calculate k(T) for each bin
    for i in range(len(counts)):
        delta_N = counts[i]  # Number of frozen droplets in this bin

        # Calculate N(T) as the number of unfrozen droplets (count in bins of lower value than this)
        N_T = np.sum(counts[:i])  # Sum counts of all lower temperature bins

        # Ensure N(T) is not zero to avoid division by zero
        if N_T == 0:
            continue  # Skip the calculation for this bin if N(T) is zero

        # Calculate bin midpoint for plotting
        bin_midpoint = (bin_edges[i] + bin_edges[i + 1]) / 2

        if delta_N > 0:  # Only calculate k(T) for bins with data
            # Check to avoid log(0) or log of negative number
            fraction = delta_N / N_T
            if fraction >= 1:
                continue  # Skip calculation if delta_N is greater than or equal to N(T)

            k_T = - (1 / (V * delta_T)) * np.log(1 - fraction)
            temp_bins.append(bin_midpoint)
            Diff_Nuclei_Conc.append(k_T)

    return temp_bins, Diff_Nuclei_Conc
