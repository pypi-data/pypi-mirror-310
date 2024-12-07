"""
This script provides a function to convert areas between different units of measurement.

The `area_converter` function accepts an area and converts it from one unit to another using predefined conversion formulas. 
It supports a range of units, including metric and imperial systems. The conversion is performed by leveraging 
the `area_formulas` module, which contains specific methods for handling each unit type.

### Supported Units:
- Metric: "square_centimeter", "square_meter", "hectare", "square_kilometer"
- Imperial: "square_foot", "square_yard", "acre"

### Main Function:
- `area_converter(area: float, from_unit: str, to_unit: str, with_unit: bool = False) -> Union[float, str]`
  
  Converts the input area (`area`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The `with_unit` parameter allows for an optional
  string output that includes the unit in the result.

### Example Usage:
- Converting 100 square meters to hectares:
    ```python
    area_converter(100, "square_meter", "hectare")
    ```
- Converting 1 acre to square meters with the unit in the result:
    ```python
    area_converter(1, "acre", "square_meter", True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

Dependencies:
- The script uses the `area_formulas` module from the `formulas` package to perform the actual conversion operations.

""

from formulas import area_formulas as af
from typing import Union

unit_list = ['square_centimeter','square_foot','square_meter','square_yard','acre','hectare','square_kilometer']

def area_converter(area: float, from_unit: str, to_unit: str, with_unit: bool = False) -> Union[float, str]:
  if from_unit not in unit_list or to_unit not in unit_list:  
    raise ValueError("The measurement has an unknown unit")
  else:
    if from_unit == 'square_centimeter':
      return af.SquareCentimeter(area, with_unit=with_unit).square_centimeter_to(to_unit)
    elif from_unit == 'square_foot':
      return af.SquareFoot(area, with_unit=with_unit).square_foot_to(to_unit)
    elif from_unit == 'square_meter':
      return af.SquareMeter(area, with_unit=with_unit).square_meter_to(to_unit)
    elif from_unit == 'square_yard':
      return af.SquareYard(area, with_unit=with_unit).square_yard_to(to_unit)
    elif from_unit == 'acre':
      return af.Acre(area, with_unit=with_unit).acre_to(to_unit)
    elif from_unit == 'hectare':
      return af.Hectare(area, with_unit=with_unit).hectare_to(to_unit)
    elif from_unit == 'square_kilometer':
      return af.SquareKilometer(area, with_unit=with_unit).square_kilometer_to(to_unit)
    else:
      raise ValueError("The measurement has an unknown unit")
"""

from typing import Union

from Metricus.formulas import area_formulas as af

unit_list = [
    "square_centimeter",
    "square_foot",
    "square_meter",
    "square_yard",
    "acre",
    "hectare",
    "square_kilometer",
]


def area_converter(
    area: float, from_unit: str, to_unit: str, with_unit: bool = False
) -> Union[float, str]:
    def area_converter(
        area: float, from_unit: str, to_unit: str, with_unit: bool = False
    ) -> Union[float, str]:
        """
        Converts a given area from one unit to another.

        Args:
            area (float): The area to be converted.
            from_unit (str): The unit of the area to convert from. Must be one of the supported units in `unit_list`.
            to_unit (str): The unit to convert the area to. Must be one of the supported units in `unit_list`.
            with_unit (bool, optional): If True, the result will include the unit of measurement as a string. Defaults to False.

        Returns:
            Union[float, str]: The converted area. If `with_unit` is True, the result will include the unit as a string;
                               otherwise, it will return the numeric value of the converted area.

        Raises:
            ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

        Example usage:
            area_converter(100, "square_meter", "hectare")  # Converts 100 square meters to hectares
            area_converter(1, "acre", "square_meter", True)  # Converts 1 acre to square meters and includes the unit in the result
        """

    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")
    else:
        if from_unit == "square_centimeter":
            return af.SquareCentimeter(area, with_unit=with_unit).square_centimeter_to(
                to_unit
            )
        elif from_unit == "square_foot":
            return af.SquareFoot(area, with_unit=with_unit).square_foot_to(to_unit)
        elif from_unit == "square_meter":
            return af.SquareMeter(area, with_unit=with_unit).square_meter_to(to_unit)
        elif from_unit == "square_yard":
            return af.SquareYard(area, with_unit=with_unit).square_yard_to(to_unit)
        elif from_unit == "acre":
            return af.Acre(area, with_unit=with_unit).acre_to(to_unit)
        elif from_unit == "hectare":
            return af.Hectare(area, with_unit=with_unit).hectare_to(to_unit)
        elif from_unit == "square_kilometer":
            return af.SquareKilometer(area, with_unit=with_unit).square_kilometer_to(
                to_unit
            )
        else:
            raise ValueError("The measurement has an unknown unit")
