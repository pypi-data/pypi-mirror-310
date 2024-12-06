"""
This script provides a function to convert accelerations between different units of measurement.

The `acceleration_converter` function accepts an acceleration value and converts it from one unit to another using predefined conversion formulas.
It supports a variety of units related to acceleration, including meters per second squared, feet per second squared, and other common units.
The conversion is performed by leveraging the `acceleration_formulas` module, which contains specific methods for handling each unit type.

### Supported Units:
- "meter_per_second_squared" (m/s²)
- "foot_per_second_squared" (ft/s²)
- "centimeter_per_second_squared" (cm/s²)
- "gal" (gal)
- "inch_per_second_squared" (in/s²)
- "kilometer_per_hour_squared" (km/h²)
- "mile_per_hour_squared" (mi/h²)
- "gravity" (g)

### Main Function:
- `acceleration_converter(acceleration: float, from_unit: str, to_unit: str, with_unit: bool = False) -> Union[float, str]`

  Converts the input acceleration (`acceleration`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The `with_unit` parameter allows for an optional
  string output that includes the unit in the result.

### Example Usage:
- Converting 9.8 meters per second squared (m/s²) to feet per second squared (ft/s²):
    ```python
    acceleration_converter(9.8, "meter_per_second_squared", "foot_per_second_squared")
    ```
- Converting 9.8 meters per second squared (m/s²) to feet per second squared (ft/s²) with the unit in the result:
    ```python
    acceleration_converter(9.8, "meter_per_second_squared", "foot_per_second_squared", True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

Dependencies:
- The script uses the `acceleration_formulas` module from the `formulas` package to perform the actual conversion operations.

"""

from typing import Union

from Metricus.formulas import acceleration_formulas as acf

unit_list = [
    "meter_per_second_squared",
    "foot_per_second_squared",
    "centimeter_per_second_squared",
    "gal",
    "inch_per_second_squared",
    "kilometer_per_hour_squared",
    "mile_per_hour_squared",
    "gravity",
]


def acceleration_converter(
    acceleration: float, from_unit: str, to_unit: str, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given acceleration from one unit to another.

    Args:
        acceleration (float): The acceleration value to be converted.
        from_unit (str): The unit of acceleration to convert from.
        to_unit (str): The unit to convert the acceleration to.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.

    Returns:
        Union[float, str]: The converted acceleration. If `with_unit` is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted acceleration.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    The function uses the `acceleration_formulas` module from the `formulas` package to handle the actual conversions.
    The conversion process is determined based on the `from_unit` and `to_unit` parameters.

    Example usage:
        acceleration_converter(9.8, "meter_per_second_squared", "foot_per_second_squared")  # Converts 9.8 m/s² to ft/s²
        acceleration_converter(9.8, "meter_per_second_squared", "foot_per_second_squared", True)  # Converts 9.8 m/s² to ft/s² and includes the unit in the result
    """
    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == "meter_per_second_squared":
        return acf.MeterPerSecondSquared(acceleration, with_unit=with_unit).mps2_to(
            to_unit
        )
    elif from_unit == "foot_per_second_squared":
        return acf.FootPerSecondSquared(acceleration, with_unit=with_unit).fps2_to(
            to_unit
        )
    elif from_unit == "centimeter_per_second_squared":
        return acf.CentimeterPerSecondSquared(
            acceleration, with_unit=with_unit
        ).cmps2_to(to_unit)
    elif from_unit == "gal":
        return acf.Gal(acceleration, with_unit=with_unit).gal_to(to_unit)
    elif from_unit == "inch_per_second_squared":
        return acf.InchPerSecondSquared(acceleration, with_unit=with_unit).ips2_to(
            to_unit
        )
    elif from_unit == "kilometer_per_hour_squared":
        return acf.KilometerPerHourSquared(acceleration, with_unit=with_unit).kmh2_to(
            to_unit
        )
    elif from_unit == "mile_per_hour_squared":
        return acf.MilePerHourSquared(acceleration, with_unit=with_unit).mph2_to(
            to_unit
        )
    elif from_unit == "gravity":
        return acf.Gravity(acceleration, with_unit=with_unit).g_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
