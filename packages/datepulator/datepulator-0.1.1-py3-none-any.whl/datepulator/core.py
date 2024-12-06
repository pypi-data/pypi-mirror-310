from datetime import datetime
import pandas as pd
from typing import Dict, Union, List, Any
import pytz
from dateutil import parser
from datetime import timedelta

class DateManager:
    """Main class for date manipulation and formatting."""
    
    def __init__(self, default_timezone: str = "UTC"):
        """
        Initialize DateManager with default settings.
        
        Args:
            default_timezone (str): Default timezone for date operations
        """
        self.default_timezone = pytz.timezone(default_timezone)

    def convert(self, date_str: str, from_format: str = None, to_format: str = "%Y-%m-%d") -> str:
        """
        Convert date string from one format to another.
        
        Args:
            date_str (str): Input date string
            from_format (str, optional): Input date format. If None, will try to parse automatically
            to_format (str): Desired output format
            
        Returns:
            str: Formatted date string
        """
        try:
            if from_format:
                date_obj = datetime.strptime(date_str, from_format)
            else:
                date_obj = parser.parse(date_str)
            
            return date_obj.strftime(to_format)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to convert date: {str(e)}")

    def extract_info(self, date_str: str, from_format: str = None) -> Dict[str, Any]:
        """
        Extract information from a date string.
        
        Args:
            date_str (str): Input date string
            from_format (str, optional): Input date format. If None, will try to parse automatically
            
        Returns:
            dict: Dictionary containing date components
        """
        try:
            if from_format:
                date_obj = datetime.strptime(date_str, from_format)
            else:
                date_obj = parser.parse(date_str)

            return {
                "year": date_obj.year,
                "month": date_obj.month,
                "day": date_obj.day,
                "weekday": date_obj.strftime("%A"),
                "weekday_number": date_obj.weekday(),
                "week_of_year": int(date_obj.strftime("%V")),
                "is_weekend": date_obj.weekday() >= 5,
                "quarter": (date_obj.month - 1) // 3 + 1
            }
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to extract date info: {str(e)}")

    def process_dataframe(self, df: pd.DataFrame, date_column: str,
                         to_format: str = None, extract_info: bool = False) -> pd.DataFrame:
        """
        Process dates in a pandas DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            date_column (str): Name of the column containing dates
            to_format (str, optional): If provided, convert dates to this format
            extract_info (bool): If True, extract date information into new columns
            
        Returns:
            pd.DataFrame: Processed DataFrame
        """
        df = df.copy()
        
        try:
            if to_format:
                df[f"{date_column}_formatted"] = df[date_column].apply(
                    lambda x: self.convert(str(x), to_format=to_format)
                )
            
            if extract_info:
                info_df = pd.DataFrame(
                    df[date_column].apply(lambda x: self.extract_info(str(x))).tolist()
                )
                df = pd.concat([df, info_df.add_prefix(f"{date_column}_")], axis=1)
            
            return df
        except Exception as e:
            raise ValueError(f"Failed to process DataFrame: {str(e)}")

    def validate_date(self, date_str: str, format: str = None) -> bool:
        """
        Validate if a string is a valid date.
        
        Args:
            date_str (str): Input date string
            format (str, optional): Expected date format
            
        Returns:
            bool: True if valid date, False otherwise
        """
        try:
            if format:
                datetime.strptime(date_str, format)
            else:
                parser.parse(date_str)
            return True
        except (ValueError, TypeError):
            return False

    def add_time(self, date_str: str, years: int = 0, months: int = 0, days: int = 0,
                 hours: int = 0, minutes: int = 0, seconds: int = 0) -> str:
        """
        Add specified time duration to a date.
        
        Args:
            date_str (str): Input date string
            years (int): Number of years to add
            months (int): Number of months to add
            days (int): Number of days to add
            hours (int): Number of hours to add
            minutes (int): Number of minutes to add
            seconds (int): Number of seconds to add
            
        Returns:
            str: Resulting date string in ISO format
        """
        try:
            date_obj = parser.parse(date_str)
            
            # Add years and months
            if years or months:
                new_year = date_obj.year + years
                new_month = date_obj.month + months
                
                while new_month > 12:
                    new_month -= 12
                    new_year += 1
                
                while new_month < 1:
                    new_month += 12
                    new_year -= 1
                
                # Handle month end dates properly
                day = min(date_obj.day, self._days_in_month(new_year, new_month))
                date_obj = date_obj.replace(year=new_year, month=new_month, day=day)
            
            # Add other time components
            date_obj += timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
            
            return date_obj.isoformat()
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to add time: {str(e)}")

    def subtract_time(self, date_str: str, years: int = 0, months: int = 0, days: int = 0,
                     hours: int = 0, minutes: int = 0, seconds: int = 0) -> str:
        """
        Subtract specified time duration from a date.
        """
        return self.add_time(date_str, -years, -months, -days, -hours, -minutes, -seconds)

    def compare_dates(self, date_str1: str, date_str2: str) -> Dict[str, Union[int, bool]]:
        """
        Compare two dates and return their relationship.
        
        Returns:
            dict: Contains difference in days and boolean comparisons
        """
        try:
            date1 = parser.parse(date_str1)
            date2 = parser.parse(date_str2)
            
            diff = date1 - date2
            
            return {
                "days_difference": diff.days,
                "is_before": date1 < date2,
                "is_after": date1 > date2,
                "is_equal": date1 == date2
            }
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to compare dates: {str(e)}")

    def convert_timezone(self, date_str: str, from_tz: str, to_tz: str) -> str:
        """
        Convert date from one timezone to another.
        """
        try:
            date_obj = parser.parse(date_str)
            from_zone = pytz.timezone(from_tz)
            to_zone = pytz.timezone(to_tz)
            
            # Localize the date to source timezone
            localized = from_zone.localize(date_obj)
            # Convert to target timezone
            converted = localized.astimezone(to_zone)
            
            return converted.isoformat()
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to convert timezone: {str(e)}")

    def get_date_range(self, start_date: str, end_date: str, interval: str = 'days') -> List[str]:
        """
        Get a list of dates between start_date and end_date.
        
        Args:
            start_date (str): Start date
            end_date (str): End date
            interval (str): Interval type ('days', 'weeks', 'months')
            
        Returns:
            list: List of dates in ISO format
        """
        try:
            start = parser.parse(start_date)
            end = parser.parse(end_date)
            
            if start > end:
                start, end = end, start
            
            dates = []
            current = start
            
            while current <= end:
                dates.append(current.isoformat())
                
                if interval == 'days':
                    current += timedelta(days=1)
                elif interval == 'weeks':
                    current += timedelta(weeks=1)
                elif interval == 'months':
                    # Move to first day of next month
                    if current.month == 12:
                        current = current.replace(year=current.year + 1, month=1)
                    else:
                        current = current.replace(month=current.month + 1)
                
            return dates
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to generate date range: {str(e)}")

    def calculate_age(self, birth_date: str, reference_date: str = None) -> Dict[str, int]:
        """
        Calculate age and related information from birth date.
        
        Returns:
            dict: Contains years, months, and days
        """
        try:
            birth = parser.parse(birth_date)
            ref_date = parser.parse(reference_date) if reference_date else datetime.now()
            
            years = ref_date.year - birth.year
            months = ref_date.month - birth.month
            days = ref_date.day - birth.day
            
            if days < 0:
                months -= 1
                days += self._days_in_month(ref_date.year, ref_date.month - 1)
            
            if months < 0:
                years -= 1
                months += 12
            
            return {
                "years": years,
                "months": months,
                "days": days,
                "total_days": (ref_date - birth).days
            }
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to calculate age: {str(e)}")

    def is_business_day(self, date_str: str, holidays: List[str] = None) -> bool:
        """
        Check if the given date is a business day.
        """
        try:
            date_obj = parser.parse(date_str)
            
            # Weekend check
            if date_obj.weekday() >= 5:  # Saturday = 5, Sunday = 6
                return False
            
            # Holiday check
            if holidays:
                holiday_dates = [parser.parse(h).date() for h in holidays]
                if date_obj.date() in holiday_dates:
                    return False
            
            return True
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to check business day: {str(e)}")

    def add_business_days(self, date_str: str, days: int, holidays: List[str] = None) -> str:
        """
        Add specified number of business days to a date.
        """
        try:
            date_obj = parser.parse(date_str)
            remaining_days = days
            
            while remaining_days > 0:
                date_obj += timedelta(days=1)
                if self.is_business_day(date_obj.isoformat(), holidays):
                    remaining_days -= 1
            
            return date_obj.isoformat()
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to add business days: {str(e)}")

    def _days_in_month(self, year: int, month: int) -> int:
        """Helper method to get the number of days in a month."""
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        return (next_month - datetime(year, month, 1)).days
