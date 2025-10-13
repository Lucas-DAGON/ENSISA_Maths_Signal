time_key = 'time'

def get_data_per_date(data: list[dict], date: str) -> list[dict]:
    """Filters the data for a specific date.

    Args:
        data (list[dict]): The list of dictionaries containing the data.
        date (str): The date to filter by in 'YYYY-MM-DD' format.

    Returns:
        list[dict]: A list of dictionaries containing only the entries for the specified date.
    """
    return [entry for entry in data if entry.get(time_key) == date]

def get_data_per_year(data: list[dict], year: str) -> list[dict]:
    """Filters the data for a specific year.

    Args:
        data (list[dict]): The list of dictionaries containing the data.
        year (str): The year to filter by in 'YYYY' format.

    Returns:
        list[dict]: A list of dictionaries containing only the entries for the specified year.
    """
    return [entry for entry in data if entry.get(time_key, '').startswith(year)]

def get_data_per_month(data: list[dict], year: str, month: str) -> list[dict]:
    """Filters the data for a specific month of a specific year.

    Args:
        data (list[dict]): The list of dictionaries containing the data.
        year (str): The year to filter by in 'YYYY' format.
        month (str): The month to filter by in 'MM' format.

    Returns:
        list[dict]: A list of dictionaries containing only the entries for the specified month and year.
    """
    prefix = f"{year}-{month}"
    return [entry for entry in data if entry.get(time_key, '').startswith(prefix)]

def get_data_per_day_of_week(data: list[dict], day_of_week: int) -> list[dict]:
    """Filters the data for a specific day of the week.

    Args:
        data (list[dict]): The list of dictionaries containing the data.
        day_of_week (int): The day of the week to filter by (0=Monday, 6=Sunday).

    Returns:
        list[dict]: A list of dictionaries containing only the entries for the specified day of the week.
    """
    from datetime import datetime
    return [entry for entry in data if 'time' in entry and datetime.strptime(entry[time_key], '%Y-%m-%d').weekday() == day_of_week]


def get_average_value(data: list[dict], key: str) -> float:
    """Calculates the average value for a specific key in the data.

    Args:
        data (list[dict]): The list of dictionaries containing the data.
        key (str): The key for which to calculate the average.

    Returns:
        float: The average value for the specified key.
    """
    values = [float(entry[key]) for entry in data if key in entry and entry[key].replace('.','',1).isdigit()]
    return sum(values) / len(values) if values else 0.0

def get_max_value(data: list[dict], key: str) -> float:
    """Finds the maximum value for a specific key in the data.

    Args:
        data (list[dict]): The list of dictionaries containing the data.
        key (str): The key for which to find the maximum value.

    Returns:
        float: The maximum value for the specified key.
    """
    values = [float(entry[key]) for entry in data if key in entry and entry[key].replace('.','',1).isdigit()]
    return max(values) if values else float('-inf')

def get_min_value(data: list[dict], key: str) -> float:
    """Finds the minimum value for a specific key in the data.

    Args:
        data (list[dict]): The list of dictionaries containing the data.
        key (str): The key for which to find the minimum value.

    Returns:
        float: The minimum value for the specified key.
    """
    values = [float(entry[key]) for entry in data if key in entry and entry[key].replace('.','',1).isdigit()]
    return min(values) if values else float('inf')