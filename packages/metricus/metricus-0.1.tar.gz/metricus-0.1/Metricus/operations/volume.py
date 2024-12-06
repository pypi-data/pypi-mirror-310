"""
This script provides a function to convert volumes between different units of measurement.

The `volume_converter` function accepts a volume and converts it from one unit to another using predefined conversion formulas. 
It supports a wide range of units, including both metric and imperial systems. The conversion is performed by leveraging 
the `volume_formulas` module, which contains specific methods for handling each unit type.

### Supported Units:
- Metric: "mL" (Milliliters), "cm3" (Cubic Centimeters), "L" (Liters), "m3" (Cubic Meters)
- Imperial: "fl_oz" (Fluid Ounces), "cup" (Cups), "pt" (Pints), "qt" (Quarts), "gal" (Gallons), "bbl" (Barrels)
- Alternative representations: "cm³", "m³"

### Main Function:
- `volume_converter(volume: float, from_unit: str, to_unit: str, with_unit: bool = False) -> Union[float, str]`
  
  Converts the input volume (`volume`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The `with_unit` parameter allows for an optional
  string output that includes the unit in the result.

### Example Usage:
- Converting 10 milliliters (mL) to liters (L):
    ```python
    volume_converter(10, "mL", "L")
    ```
- Converting 10 milliliters (mL) to liters (L) with the unit in the result:
    ```python
    volume_converter(10, "mL", "L", True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

Dependencies:
- The script uses the `volume_formulas` module from the `formulas` package to perform the actual conversion operations.

"""

from typing import Union

from Metricus.formulas import volume_formulas as vf

unit_list = [
    "mL",  # Milliliters
    "cm3",  # Cubic Centimeters
    "cm³",  # Cubic Centimeters (alternative notation)
    "fl_oz",  # Fluid Ounces
    "cup",  # Cups
    "pt",  # Pints
    "qt",  # Quarts
    "L",  # Liters
    "gal",  # Gallons
    "bbl",  # Barrels
    "m3",  # Cubic Meters
    "m³",  # Cubic Meters (alternative notation)
]


def volume_converter(
    volume: float, from_unit: str, to_unit: str, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given volume from one unit to another.

    Args:
        volume (float): The volume to be converted.
        from_unit (str): The unit of the volume to convert from.
        to_unit (str): The unit to convert the volume to.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.

    Returns:
        Union[float, str]: The converted volume. If `with_unit` is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted volume.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    The function uses the `volume_formulas` module from the `formulas` package to handle the actual conversions.
    The conversion process is determined based on the `from_unit` and `to_unit` parameters.

    Example usage:
        volume_converter(10, "mL", "L")  # Converts 10 milliliters to liters
        volume_converter(10, "mL", "L", True)  # Converts 10 milliliters to liters and includes the unit in the result
    """
    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == "mL":
        return vf.Milliliter(volume, with_unit=with_unit).mL_to(to_unit)
    elif from_unit == "cm3" or from_unit == "cm³":
        return vf.Milliliter(volume, with_unit=with_unit).mL_to(to_unit)
    elif from_unit == "fl_oz":
        return vf.FluidOunce(volume, with_unit=with_unit).fl_oz_to(to_unit)
    elif from_unit == "cup":
        return vf.Cup(volume, with_unit=with_unit).cup_to(to_unit)
    elif from_unit == "pt":
        return vf.Pint(volume, with_unit=with_unit).pt_to(to_unit)
    elif from_unit == "qt":
        return vf.Quart(volume, with_unit=with_unit).qt_to(to_unit)
    elif from_unit == "L":
        return vf.Liter(volume, with_unit=with_unit).liter_to(to_unit)
    elif from_unit == "gal":
        return vf.Gallon(volume, with_unit=with_unit).gal_to(to_unit)
    elif from_unit == "bbl":
        return vf.Barrel(volume, with_unit=with_unit).bbl_to(to_unit)
    elif from_unit == "m3" or from_unit == "m³":
        return vf.CubicMeter(volume, with_unit=with_unit).m3_to(to_unit)
