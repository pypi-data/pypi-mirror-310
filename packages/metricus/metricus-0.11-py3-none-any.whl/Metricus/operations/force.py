"""
This script provides a function to convert forces between different units of measurement.

The `force_converter` function accepts a force value and converts it from one unit to another using predefined conversion formulas.
It supports a variety of units related to force, including newton, pound force, and other common units.
The conversion is performed by leveraging the `force_formulas` module, which contains specific methods for handling each unit type.

### Supported Units:
- "newton" (N)
- "dyne" (dyn)
- "kilonewton" (kN)
- "pound_force" (lbf)
- "ounce_force" (ozf)
- "ton_force" (tonf)
- "kilogram_force" (kgf)
- "gram_force" (gf)
- "millinewton" (mN)
- "poundal" (pdl)
- "slug_force" (slf)

### Main Function:
- `force_converter(force: float, from_unit: str, to_unit: str, with_unit: bool = False) -> Union[float, str]`

  Converts the input force (`force`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The `with_unit` parameter allows for an optional
  string output that includes the unit in the result.

### Example Usage:
- Converting 10 newtons (N) to pound-force (lbf):
    ```python
    force_converter(10, "newton", "pound_force")
    ```
- Converting 10 newtons (N) to pound-force (lbf) with the unit in the result:
    ```python
    force_converter(10, "newton", "pound_force", True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

Dependencies:
- The script uses the `force_formulas` module from the `formulas` package to perform the actual conversion operations.
"""

from typing import Union

from Metricus.formulas import force_formulas as ff

unit_list = [
    "newton",
    "dyne",
    "kilonewton",
    "pound_force",
    "ounce_force",
    "ton_force",
    "kilogram_force",
    "gram_force",
    "millinewton",
    "poundal",
    "slug_force",
]


def force_converter(
    force: float, from_unit: str, to_unit: str, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts the input force from a given unit to another.

    Args:
        force (float): The force value to be converted.
        from_unit (str): The unit of force to convert from.
        to_unit (str): The unit to convert the force to.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.

    Returns:
        Union[float, str]: The converted force. If `with_unit` is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted force.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    Example usage:
        force_converter(10, "newton", "pound_force")  # Converts 10 N to lbf
        force_converter(10, "newton", "pound_force", True)  # Converts 10 N to lbf and includes the unit in the result
    """
    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == "newton":
        return ff.Newton(force, with_unit=with_unit).newton_to(to_unit)
    elif from_unit == "dyne":
        return ff.Dyne(force, with_unit=with_unit).dyne_to(to_unit)
    elif from_unit == "kilonewton":
        return ff.Kilonewton(force, with_unit=with_unit).kilonewton_to(to_unit)
    elif from_unit == "pound_force":
        return ff.PoundForce(force, with_unit=with_unit).pound_force_to(to_unit)
    elif from_unit == "ounce_force":
        return ff.OunceForce(force, with_unit=with_unit).ounce_force_to(to_unit)
    elif from_unit == "ton_force":
        return ff.TonForce(force, with_unit=with_unit).ton_force_to(to_unit)
    elif from_unit == "kilogram_force":
        return ff.KilogramForce(force, with_unit=with_unit).kilogram_force_to(to_unit)
    elif from_unit == "gram_force":
        return ff.GramForce(force, with_unit=with_unit).gram_force_to(to_unit)
    elif from_unit == "millinewton":
        return ff.Millinewton(force, with_unit=with_unit).millinewton_to(to_unit)
    elif from_unit == "poundal":
        return ff.Poundal(force, with_unit=with_unit).poundal_to(to_unit)
    elif from_unit == "slug_force":
        return ff.SlugForce(force, with_unit=with_unit).slug_force_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
