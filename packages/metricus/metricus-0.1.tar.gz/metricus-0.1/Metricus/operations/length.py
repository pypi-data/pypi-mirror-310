"""
This script provides a function to convert lengths between different units of measurement.

The `length_converter` function accepts a length value and converts it from one unit to another using predefined conversion formulas. 
It supports a variety of length units, including millimeters, centimeters, inches, feet, yards, meters, kilometers, miles, and nautical miles. The conversion is performed by leveraging 
the `length_formulas` module, which contains specific methods for handling each length unit.

### Supported Units:
- "millimeter" (mm)
- "centimeter" (cm)
- "inch" (in)
- "foot" (ft)
- "yard" (yd)
- "meter" (m)
- "kilometer" (km)
- "mile" (mi)
- "nautical_mile" (nm)

### Main Function:
- `length_converter(length: float, from_unit: str, to_unit: str, with_unit: bool = False) -> Union[float, str]`

  Converts the input length (`length`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The `with_unit` parameter allows for an optional
  string output that includes the unit in the result.

### Example Usage:
- Converting 10 millimeters (mm) to centimeters (cm):
    ```python
    length_converter(10, "millimeter", "centimeter")
    ```
- Converting 10 millimeters (mm) to centimeters (cm) with the unit in the result:
    ```python
    length_converter(10, "millimeter", "centimeter", True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

Dependencies:
- The script uses the `length_formulas` module from the `formulas` package to perform the actual conversion operations.

"""

from typing import Union

from Metricus.formulas import length_formulas as lf

unit_list = [
    "millimeter",
    "centimeter",
    "inch",
    "foot",
    "yard",
    "meter",
    "kilometer",
    "mile",
    "nautical_mile",
]


def length_converter(
    length: float, from_unit: str, to_unit: str, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given length from one unit to another.

    Args:
        length (float): The length to be converted.
        from_unit (str): The unit of the length to convert from.
        to_unit (str): The unit to convert the length to.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.

    Returns:
        Union[float, str]: The converted length. If `with_unit` is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted length.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    The function uses the `length_formulas` module from the `formulas` package to handle the actual conversions.
    The conversion process is determined based on the `from_unit` and `to_unit` parameters.

    Example usage:
        length_converter(10, "millimeter", "centimeter")  # Converts 10 millimeters to centimeters
        length_converter(10, "millimeter", "centimeter", True)  # Converts 10 millimeters to centimeters and includes the unit in the result
    """
    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == "millimeter":
        return lf.Millimeter(length, with_unit=with_unit).millimeter_to(to_unit)
    elif from_unit == "centimeter":
        return lf.Centimeter(length, with_unit=with_unit).centimeter_to(to_unit)
    elif from_unit == "inch":
        return lf.Inch(length, with_unit=with_unit).inch_to(to_unit)
    elif from_unit == "foot":
        return lf.Foot(length, with_unit=with_unit).foot_to(to_unit)
    elif from_unit == "yard":
        return lf.Yard(length, with_unit=with_unit).yard_to(to_unit)
    elif from_unit == "meter":
        return lf.Meter(length, with_unit=with_unit).meter_to(to_unit)
    elif from_unit == "kilometer":
        return lf.Kilometer(length, with_unit=with_unit).kilometer_to(to_unit)
    elif from_unit == "mile":
        return lf.Mile(length, with_unit=with_unit).mile_to(to_unit)
    elif from_unit == "nautical_mile":
        return lf.NauticalMile(length, with_unit=with_unit).nautical_mile_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
