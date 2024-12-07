"""
This script provides a function to convert time between different units of measurement.

The `time_converter` function accepts a time and converts it from one unit to another using predefined conversion formulas. 
It supports a wide range of time units, from smaller (milliseconds) to larger (centuries). The conversion is performed by leveraging 
the `time_formulas` module, which contains specific methods for handling each time unit.

### Supported Units:
- "millisecond"
- "second"
- "minute"
- "hour"
- "day"
- "week"
- "month"
- "year"
- "decade"
- "century"

### Main Function:
- `time_converter(time: float, from_unit: str, to_unit: str, with_unit: bool = False) -> Union[float, str]`

  Converts the input time (`time`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The `with_unit` parameter allows for an optional
  string output that includes the unit in the result.

### Example Usage:
- Converting 10 seconds (s) to minutes (min):
    ```python
    time_converter(10, "second", "minute")
    ```
- Converting 10 seconds (s) to minutes (min) with the unit in the result:
    ```python
    time_converter(10, "second", "minute", True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

Dependencies:
- The script uses the `time_formulas` module from the `formulas` package to perform the actual conversion operations.

"""

from typing import Union

from Metricus.formulas import time_formulas as timef

unit_list = [
    "millisecond",  # Milliseconds
    "second",  # Seconds
    "minute",  # Minutes
    "hour",  # Hours
    "day",  # Days
    "week",  # Weeks
    "month",  # Months
    "year",  # Years
    "decade",  # Decades
    "century",  # Centuries
]


def time_converter(
    time: float, from_unit: str, to_unit: str, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given time from one unit to another.

    Args:
        time (float): The time to be converted.
        from_unit (str): The unit of the time to convert from.
        to_unit (str): The unit to convert the time to.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.

    Returns:
        Union[float, str]: The converted time. If `with_unit` is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted time.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    The function uses the `time_formulas` module from the `formulas` package to handle the actual conversions.
    The conversion process is determined based on the `from_unit` and `to_unit` parameters.

    Example usage:
        time_converter(10, "second", "minute")  # Converts 10 seconds to minutes
        time_converter(10, "second", "minute", True)  # Converts 10 seconds to minutes and includes the unit in the result
    """
    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == "millisecond":
        return timef.Millisecond(time, with_unit=with_unit).millisecond_to(to_unit)
    elif from_unit == "second":
        return timef.Second(time, with_unit=with_unit).second_to(to_unit)
    elif from_unit == "minute":
        return timef.Minute(time, with_unit=with_unit).minute_to(to_unit)
    elif from_unit == "hour":
        return timef.Hour(time, with_unit=with_unit).hour_to(to_unit)
    elif from_unit == "day":
        return timef.Day(time, with_unit=with_unit).day_to(to_unit)
    elif from_unit == "week":
        return timef.Week(time, with_unit=with_unit).week_to(to_unit)
    elif from_unit == "month":
        return timef.Month(time, with_unit=with_unit).month_to(to_unit)
    elif from_unit == "year":
        return timef.Year(time, with_unit=with_unit).year_to(to_unit)
    elif from_unit == "decade":
        return timef.Decade(time, with_unit=with_unit).decade_to(to_unit)
    elif from_unit == "century":
        return timef.Century(time, with_unit=with_unit).century_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
