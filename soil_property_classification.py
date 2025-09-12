"""
Helper function to classify soil property (N,P,K, pH)
values to either "LOW", "MODERATE" or "HIGH"
based on given thresholds
"""


def get_nitrogen_classification(pH_value):
    """
    returns the classification of Nitrogen in location
    """
    pH_value = float(pH_value)
    if pH_value is None or pH_value <= 1.5:
        return "LOW"
    elif pH_value > 1.5 and pH_value <= 5.0:
        return "MODERATE"
    else:
        return "HIGH"



def get_phosphorous_classification(phosphorous_value):
    """
    returns the classification of Phosphorous in location
    """
    phosphorous_value = float(phosphorous_value)
    if phosphorous_value is None or phosphorous_value <= 10:
        return "LOW"
    elif phosphorous_value > 10 and phosphorous_value <= 50:
        return "MODERATE"
    else:
        return "HIGH"



def get_potassium_classification(potassium_value):
    """
    returns the classification of Potassium in location
    """
    potassium_value = float(potassium_value)
    if potassium_value is None or potassium_value <= 39:
        return "LOW"
    elif potassium_value > 39 and potassium_value <= 195:
        return "MODERATE"
    else:
        return "HIGH"



def get_ph_classification(pH_value):
    """
    returns the classification of pH in location
    """
    pH_value = float(pH_value)
    if pH_value is None or pH_value <= 5.3:
        return "LOW"
    elif pH_value > 5.3 and pH_value <= 7.3:
        return "MODERATE"
    else:
        return "HIGH"