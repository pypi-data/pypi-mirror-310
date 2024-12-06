# worldtimeconverter/converter.py
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import pytz
from dataclasses import dataclass
from .types import (
    TimeResult,
    BusinessHours,
    HolidayDefinition,
    TimeInterval,
    WorkingHoursOverlap,
    CityInfo
)
from .exceptions import InvalidCityError, InvalidTimeFormatError


class WorldTimeConverter:
    """Main class for handling time conversions and calculations."""

    _holidays: Dict[str, List[HolidayDefinition]] = {}

    @classmethod
    def get_current_time(cls, city_name: str) -> TimeResult:
        """Get current time for a specific city."""
        try:
            timezone = cls._get_city_timezone(city_name)
            # Create a naive datetime first
            naive_now = datetime.utcnow()
            # Localize it to UTC
            utc_now = pytz.UTC.localize(naive_now)
            # Convert to target timezone
            now = utc_now.astimezone(timezone)

            return TimeResult(
                city_name=city_name,
                timezone=str(timezone),
                local_time=now.strftime('%H:%M:%S'),
                utc_offset=now.strftime('%z'),
                date=now.strftime('%Y-%m-%d'),
                day_of_week=now.strftime('%A'),
                is_dst=now.dst() != timedelta(0),
                epoch=int(now.timestamp()),
                iso8601=now.isoformat(),
                formatted_date_time=now.strftime('%c')
            )
        except pytz.exceptions.UnknownTimeZoneError:
            raise InvalidCityError(f"Invalid city name: {city_name}")

    @classmethod
    def convert_time(
            cls,
            timestamp: Union[int, str, datetime],
            from_city: str,
            to_city: str,
            format: str = '%Y-%m-%d %H:%M:%S'
    ) -> TimeResult:
        """Convert time between cities."""
        try:
            from_tz = cls._get_city_timezone(from_city)
            to_tz = cls._get_city_timezone(to_city)

            if isinstance(timestamp, int):
                # For Unix timestamp, first create UTC time
                dt = datetime.fromtimestamp(timestamp, pytz.UTC)
            elif isinstance(timestamp, str):
                # For string timestamp, parse as naive then localize
                naive_dt = datetime.strptime(timestamp, format)
                dt = from_tz.localize(naive_dt)
            elif isinstance(timestamp, datetime):
                if timestamp.tzinfo is None:
                    dt = from_tz.localize(timestamp)
                else:
                    dt = timestamp.astimezone(from_tz)
            else:
                raise ValueError("Invalid timestamp format")

            # Convert to target timezone
            converted = dt.astimezone(to_tz)

            return TimeResult(
                city_name=to_city,
                timezone=str(to_tz),
                local_time=converted.strftime('%H:%M:%S'),
                utc_offset=converted.strftime('%z'),
                date=converted.strftime('%Y-%m-%d'),
                day_of_week=converted.strftime('%A'),
                is_dst=converted.dst() != timedelta(0),
                epoch=int(converted.timestamp()),
                iso8601=converted.isoformat(),
                formatted_date_time=converted.strftime(format)
            )
        except (pytz.exceptions.UnknownTimeZoneError, ValueError) as e:
            raise InvalidCityError(str(e))

    @classmethod
    def find_working_hours_overlap(
            cls,
            city1: str,
            city2: str,
            business_hours1: BusinessHours,
            business_hours2: BusinessHours
    ) -> WorkingHoursOverlap:
        """Calculate working hours overlap between two cities."""
        if not all(cls._validate_time_format(t) for t in
                   [business_hours1.start, business_hours1.end,
                    business_hours2.start, business_hours2.end]):
            raise InvalidTimeFormatError("Invalid time format. Use HH:MM format")

        tz1 = cls._get_city_timezone(city1)
        tz2 = cls._get_city_timezone(city2)

        # Use naive datetime for base calculations
        naive_now = datetime.utcnow()
        date_str = naive_now.strftime('%Y-%m-%d')

        # Create naive datetimes first, then localize them
        start1 = tz1.localize(datetime.strptime(f"{date_str} {business_hours1.start}",
                                                '%Y-%m-%d %H:%M'))
        end1 = tz1.localize(datetime.strptime(f"{date_str} {business_hours1.end}",
                                              '%Y-%m-%d %H:%M'))
        start2 = tz2.localize(datetime.strptime(f"{date_str} {business_hours2.start}",
                                                '%Y-%m-%d %H:%M'))
        end2 = tz2.localize(datetime.strptime(f"{date_str} {business_hours2.end}",
                                              '%Y-%m-%d %H:%M'))

        # Convert all times to UTC for comparison
        start1_utc = start1.astimezone(pytz.UTC)
        end1_utc = end1.astimezone(pytz.UTC)
        start2_utc = start2.astimezone(pytz.UTC)
        end2_utc = end2.astimezone(pytz.UTC)

        # Find overlap in UTC
        overlap_start = max(start1_utc, start2_utc)
        overlap_end = min(end1_utc, end2_utc)
        has_overlap = overlap_end > overlap_start

        if has_overlap:
            duration = overlap_end - overlap_start
            overlap_duration = TimeInterval(
                hours=duration.seconds // 3600,
                minutes=(duration.seconds % 3600) // 60
            )
        else:
            overlap_duration = TimeInterval(hours=0, minutes=0)

        return WorkingHoursOverlap(
            start_time=overlap_start.astimezone(tz1).strftime('%H:%M') if has_overlap else '',
            end_time=overlap_end.astimezone(tz1).strftime('%H:%M') if has_overlap else '',
            overlap_duration=overlap_duration,
            has_overlap=has_overlap,
            working_days=cls._get_common_working_days(city1, city2)
        )

    @classmethod
    def add_holiday(cls, city_name: str, holiday: HolidayDefinition) -> None:
        """Add a holiday definition for a city."""
        if city_name not in cls._holidays:
            cls._holidays[city_name] = []
        cls._holidays[city_name].append(holiday)

    @classmethod
    def is_holiday(cls, city_name: str, date: datetime) -> bool:
        """Check if a given date is a holiday in the specified city."""
        city_holidays = cls._holidays.get(city_name, [])
        date_str = date.strftime('%Y-%m-%d')

        return any(
            holiday.date == date_str or
            (holiday.recurring and holiday.date[5:] == date_str[5:])
            for holiday in city_holidays
        )

    @classmethod
    def get_business_days_between(
            cls,
            city_name: str,
            start_date: Union[str, datetime],
            end_date: Union[str, datetime],
            skip_holidays: bool = True
    ) -> int:
        """Calculate business days between two dates."""
        tz = cls._get_city_timezone(city_name)

        if isinstance(start_date, str):
            start = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=tz)
        else:
            start = start_date.astimezone(tz)

        if isinstance(end_date, str):
            end = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=tz)
        else:
            end = end_date.astimezone(tz)

        business_days = 0
        current = start

        while current <= end:
            if (current.weekday() < 5 and  # Mon-Fri
                    (not skip_holidays or not cls.is_holiday(city_name, current))):
                business_days += 1
            current += timedelta(days=1)

        return business_days

    @classmethod
    def get_city_info(cls, city_name: str) -> CityInfo:
        """Get information about a city's timezone."""
        tz = cls._get_city_timezone(city_name)
        now = datetime.now(tz)

        return CityInfo(
            city_name=city_name,
            timezone=str(tz),
            current_offset=now.strftime('%z'),
            is_dst=tz.dst(now) != timedelta(0),
            region=str(tz).split('/')[0],
            subregion=str(tz).split('/')[1]
        )

    @staticmethod
    def _get_city_timezone(city_name: str) -> pytz.timezone:
        """Get timezone for a city."""
        try:
            # Try direct timezone lookup
            return pytz.timezone(city_name)
        except pytz.exceptions.UnknownTimeZoneError:
            # Search through all timezones
            for tz_name in pytz.all_timezones:
                if city_name.lower() in tz_name.lower():
                    return pytz.timezone(tz_name)
            raise InvalidCityError(f"Timezone not found for city: {city_name}")

    @staticmethod
    def _validate_time_format(time_str: str) -> bool:
        """Validate time format (HH:MM)."""
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False

    @classmethod
    def _get_common_working_days(cls, city1: str, city2: str) -> List[str]:
        """Get common working days between two cities."""
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        # Get holidays for both cities
        holidays1 = cls._holidays.get(city1, [])
        holidays2 = cls._holidays.get(city2, [])

        # Start with standard working days (Mon-Fri)
        common_days = weekdays.copy()

        # Get current date for reference
        now = datetime.now()
        current_year = now.year

        # Check each weekday if it's a holiday in either city
        for weekday in weekdays[:]:  # Copy list for iteration
            # Get the next occurrence of this weekday
            day = now
            while day.strftime('%A') != weekday:
                day += timedelta(days=1)

            # Check if this weekday is typically a holiday in either city
            is_holiday1 = any(
                (h.recurring and h.date[5:] == day.strftime('%m-%d')) or
                h.date == day.strftime('%Y-%m-%d')
                for h in holidays1
            )
            is_holiday2 = any(
                (h.recurring and h.date[5:] == day.strftime('%m-%d')) or
                h.date == day.strftime('%Y-%m-%d')
                for h in holidays2
            )

            # If it's a holiday in either city, remove from common days
            if is_holiday1 or is_holiday2:
                common_days.remove(weekday)

        return common_days

    @classmethod
    def find_working_hours_overlap(
            cls,
            city1: str,
            city2: str,
            business_hours1: BusinessHours,
            business_hours2: BusinessHours
    ) -> WorkingHoursOverlap:
        """Calculate working hours overlap between two cities."""
        if not all(cls._validate_time_format(t) for t in
                   [business_hours1.start, business_hours1.end,
                    business_hours2.start, business_hours2.end]):
            raise InvalidTimeFormatError("Invalid time format. Use HH:MM format")

        tz1 = cls._get_city_timezone(city1)
        tz2 = cls._get_city_timezone(city2)

        # Use naive datetime for base calculations
        naive_now = datetime.utcnow()
        date_str = naive_now.strftime('%Y-%m-%d')

        # Create naive datetimes first, then localize them
        start1 = tz1.localize(datetime.strptime(f"{date_str} {business_hours1.start}",
                                                '%Y-%m-%d %H:%M'))
        end1 = tz1.localize(datetime.strptime(f"{date_str} {business_hours1.end}",
                                              '%Y-%m-%d %H:%M'))
        start2 = tz2.localize(datetime.strptime(f"{date_str} {business_hours2.start}",
                                                '%Y-%m-%d %H:%M'))
        end2 = tz2.localize(datetime.strptime(f"{date_str} {business_hours2.end}",
                                              '%Y-%m-%d %H:%M'))

        # Convert all times to UTC for comparison
        start1_utc = start1.astimezone(pytz.UTC)
        end1_utc = end1.astimezone(pytz.UTC)
        start2_utc = start2.astimezone(pytz.UTC)
        end2_utc = end2.astimezone(pytz.UTC)

        # Find overlap in UTC
        overlap_start = max(start1_utc, start2_utc)
        overlap_end = min(end1_utc, end2_utc)
        has_overlap = overlap_end > overlap_start

        if has_overlap:
            duration = overlap_end - overlap_start
            overlap_duration = TimeInterval(
                hours=duration.seconds // 3600,
                minutes=(duration.seconds % 3600) // 60
            )
        else:
            overlap_duration = TimeInterval(hours=0, minutes=0)

        # Get working days
        try:
            working_days = cls._get_common_working_days(city1, city2)
        except Exception:
            # Fallback to standard working days if there's an error
            working_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        return WorkingHoursOverlap(
            start_time=overlap_start.astimezone(tz1).strftime('%H:%M') if has_overlap else '',
            end_time=overlap_end.astimezone(tz1).strftime('%H:%M') if has_overlap else '',
            overlap_duration=overlap_duration,
            has_overlap=has_overlap,
            working_days=working_days
        )