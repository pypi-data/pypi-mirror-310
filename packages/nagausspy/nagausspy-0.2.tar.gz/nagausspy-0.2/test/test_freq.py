import pytest
import os
import numpy as np
from nagausspy import GaussianLog, Units

ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]

@pytest.fixture
def frequencylog():
    flog = os.path.join(ACTUAL_PATH, "data/output_freq.log")
    return GaussianLog(flog)


def test_modes(frequencylog):
    assert len(frequencylog.frequencies.frequencies) == 33

def test_low(frequencylog):
    low = np.array([-2.38580000e+00, -2.28630000e+00, -7.89300000e-01,
                    -3.50000000e-03, 4.10000000e-03, 5.80000000e-03,
                    1.72462000e+01, 2.30836000e+01, 2.97682000e+01])
    assert np.allclose(low, frequencylog.frequencies.low_frequencies)

def test_generate_spectra(frequencylog):
    freq, intensity = frequencylog.frequencies.generate_spectra()
    assert len(freq) == len(intensity)

def test_thermo(frequencylog):
    result = ("Sum of electronic and zero-point Energies = -3472.858647 Ha\n"
              "Sum of electronic and thermal Energies = -3472.842107 Ha\n"
              "Sum of electronic and thermal Enthalpies = -3472.841163 Ha\n"
              "Sum of electronic and thermal Free Energies = -3472.910891 Ha\n"
              "Total CV = 8.081181378309116e-05 Ha/K\n"
              "Translational CV = 4.750448953627315e-06 Ha/K\n"
              "Rotational CV = 4.750448953627315e-06 Ha/K\n"
              "Vibrational CV = 7.131091587583655e-05 Ha/K\n")

    assert result == str(frequencylog.frequencies.thermochemistry)

def test_substract(frequencylog):
    result = ("Sum of electronic and zero-point Energies = 0.0 Ha\n"
              "Sum of electronic and thermal Energies = 0.0 Ha\n"
              "Sum of electronic and thermal Enthalpies = 0.0 Ha\n"
              "Sum of electronic and thermal Free Energies = 0.0 Ha\n"
              "Total CV = 0.0 Ha/K\n"
              "Translational CV = 0.0 Ha/K\n"
              "Rotational CV = 0.0 Ha/K\n"
              "Vibrational CV = 0.0 Ha/K\n")
    delta = frequencylog.frequencies.thermochemistry
    delta = delta - delta

    assert str(delta) == result

def test_product(frequencylog):
    result = ("Sum of electronic and zero-point Energies = -3472.858647 Ha\n"
              "Sum of electronic and thermal Energies = -3472.842107 Ha\n"
              "Sum of electronic and thermal Enthalpies = -3472.841163 Ha\n"
              "Sum of electronic and thermal Free Energies = -3472.910891 Ha\n"
              "Total CV = 8.081181378309116e-05 Ha/K\n"
              "Translational CV = 4.750448953627315e-06 Ha/K\n"
              "Rotational CV = 4.750448953627315e-06 Ha/K\n"
              "Vibrational CV = 7.131091587583655e-05 Ha/K\n")

    delta = frequencylog.frequencies.thermochemistry
    delta = 2*delta - delta

    assert str(delta) == result

def test_change_units(frequencylog):
    result = ("Sum of electronic and zero-point Energies = -9118137.966065178 kJmol\n"
              "Sum of electronic and thermal Energies = -9118094.539592266 kJmol\n"
              "Sum of electronic and thermal Enthalpies = -9118092.061080148 kJmol\n"
              "Sum of electronic and thermal Free Energies = -9118275.134907424 kJmol\n"
              "Total CV = 0.21217485140050754 kJmol/K\n"
              "Translational CV = 0.012472505610713908 kJmol/K\n"
              "Rotational CV = 0.012472505610713908 kJmol/K\n"
              "Vibrational CV = 0.18722984017907976 kJmol/K\n")

    thermo = frequencylog.frequencies.thermochemistry

    thermo.units = Units.kJmol

    assert str(thermo) == result
