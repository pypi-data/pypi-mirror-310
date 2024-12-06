# Datepulator 📅

A powerful and flexible Python library for advanced date and time manipulation. Datepulator provides an intuitive interface for working with dates, including timezone conversions, business day calculations, date arithmetic, and more.

[![PyPI version](https://badge.fury.io/py/datepulator.svg)](https://badge.fury.io/py/datepulator)
[![Python Support](https://img.shields.io/pypi/pyversions/datepulator.svg)](https://pypi.org/project/datepulator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features 🌟

- 📅 **Date Arithmetic**: Add or subtract years, months, days, hours, minutes, and seconds
- 🌍 **Timezone Support**: Convert dates between any timezone using pytz
- 💼 **Business Days**: Calculate business days considering weekends and holidays
- 📊 **Date Ranges**: Generate sequences of dates with custom intervals
- 🎂 **Age Calculation**: Calculate age with detailed breakdown
- 🔄 **Format Conversion**: Convert between different date formats
- ⚡ **Performance**: Optimized for speed and efficiency
- 🐍 **Type Hints**: Full typing support for better IDE integration

## Installation 📦

```bash
pip install datepulator
```

## Quick Start 🚀

```python
from datepulator import DateManager

# Initialize DateManager
dm = DateManager(default_timezone="UTC")

# Convert date format
result = dm.convert("2023/12/25", from_format="%Y/%m/%d", to_format="%d-%b-%Y")
print(result)  # Output: 25-Dec-2023

# Add time to a date
new_date = dm.add_time("2023-01-15", 
                       years=1, 
                       months=2, 
                       days=10)
print(new_date)  # Output: 2024-03-25T00:00:00

# Calculate age
age = dm.calculate_age("1990-05-20")
print(age)  # Output: {'years': 33, 'months': 7, 'days': 15, 'total_days': 12271}
```

## Detailed Usage 📚

### 1. Date Arithmetic

```python
dm = DateManager()

# Add time
future_date = dm.add_time("2023-01-15",
                         years=1,
                         months=2,
                         days=3,
                         hours=4,
                         minutes=30)

# Subtract time
past_date = dm.subtract_time("2023-01-15",
                           months=3,
                           days=5)
```

### 2. Timezone Conversions

```python
# Convert from UTC to New York time
ny_time = dm.convert_timezone("2023-01-15 10:00:00",
                            from_tz="UTC",
                            to_tz="America/New_York")

# Convert from Tokyo to London time
london_time = dm.convert_timezone("2023-01-15 15:00:00",
                                from_tz="Asia/Tokyo",
                                to_tz="Europe/London")
```

### 3. Business Days

```python
# Define holidays
holidays = [
    "2023-12-25",  # Christmas
    "2023-12-26",  # Boxing Day
    "2024-01-01"   # New Year's Day
]

# Check if it's a business day
is_working = dm.is_business_day("2023-12-25", holidays=holidays)

# Add business days
next_working_day = dm.add_business_days("2023-12-24", 
                                      days=3,
                                      holidays=holidays)
```

### 4. Date Ranges

```python
# Get daily dates
daily_dates = dm.get_date_range("2023-01-01",
                               "2023-01-10",
                               interval="days")

# Get weekly dates
weekly_dates = dm.get_date_range("2023-01-01",
                                "2023-03-01",
                                interval="weeks")

# Get monthly dates
monthly_dates = dm.get_date_range("2023-01-01",
                                 "2023-12-31",
                                 interval="months")
```

### 5. Age Calculation

```python
# Calculate age as of today
current_age = dm.calculate_age("1990-05-20")

# Calculate age as of a specific date
past_age = dm.calculate_age("1990-05-20", 
                          reference_date="2010-01-01")
```

## API Reference 📖

### DateManager Class

#### Constructor

```python
DateManager(default_timezone: str = "UTC")
```

#### Methods

1. `convert(date_str: str, from_format: str = None, to_format: str = "%Y-%m-%d") -> str`
   - Convert date string from one format to another
   - Auto-detects format if `from_format` is None

2. `add_time(date_str: str, years: int = 0, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> str`
   - Add specified time duration to a date
   - Returns ISO format string

3. `subtract_time(date_str: str, years: int = 0, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> str`
   - Subtract specified time duration from a date
   - Returns ISO format string

4. `convert_timezone(date_str: str, from_tz: str, to_tz: str) -> str`
   - Convert date from one timezone to another
   - Uses pytz timezones

5. `get_date_range(start_date: str, end_date: str, interval: str = 'days') -> List[str]`
   - Get list of dates between start_date and end_date
   - Interval options: 'days', 'weeks', 'months'

6. `calculate_age(birth_date: str, reference_date: str = None) -> Dict[str, int]`
   - Calculate age and related information
   - Returns dict with years, months, days, and total_days

7. `is_business_day(date_str: str, holidays: List[str] = None) -> bool`
   - Check if given date is a business day
   - Considers weekends and optional holidays

8. `add_business_days(date_str: str, days: int, holidays: List[str] = None) -> str`
   - Add specified number of business days
   - Skips weekends and holidays

## Error Handling 🚨

All methods include comprehensive error handling and will raise `ValueError` with descriptive messages when:
- Invalid date strings are provided
- Invalid formats are specified
- Invalid timezone names are used
- Other validation errors occur

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

If you have any questions or run into issues, please:
1. Check the [Issues](https://github.com/yourusername/datepulator/issues) page
2. Create a new issue if your problem isn't already listed
3. Provide as much detail as possible about your problem

## Acknowledgments 🙏

- Built with [Python](https://www.python.org/)
- Timezone support by [pytz](https://pythonhosted.org/pytz/)
- Date parsing by [python-dateutil](https://dateutil.readthedocs.io/)

---

Made with ❤️ by [Your Name/Organization]
