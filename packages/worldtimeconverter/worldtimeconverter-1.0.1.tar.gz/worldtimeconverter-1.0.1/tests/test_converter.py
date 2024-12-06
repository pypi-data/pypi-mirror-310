import pytest
from datetime import datetime
import pytz
from worldtimeconverter import WorldTimeConverter
from worldtimeconverter.types import BusinessHours, HolidayDefinition
from worldtimeconverter.exceptions import InvalidCityError, InvalidTimeFormatError


class TestWorldTimeConverter:
    def test_get_current_time(self):
        result = WorldTimeConverter.get_current_time('London')

        assert result.city_name == 'London'
        assert 'Europe/London' in result.timezone
        assert result.local_time.count(':') == 2
        assert len(result.date.split('-')) == 3
        assert isinstance(result.is_dst, bool)
        assert isinstance(result.epoch, int)

    def test_invalid_city(self):
        with pytest.raises(InvalidCityError):
            WorldTimeConverter.get_current_time('InvalidCity')

    def test_convert_time(self):
        timestamp = "2024-01-01 12:00:00"
        result = WorldTimeConverter.convert_time(timestamp, 'London', 'Tokyo')

        assert result.city_name == 'Tokyo'
        assert 'Asia/Tokyo' in result.timezone
        assert isinstance(result.epoch, int)

    def test_convert_time_with_unix_timestamp(self):
        timestamp = int(datetime.now().timestamp())
        result = WorldTimeConverter.convert_time(timestamp, 'New_York', 'Paris')

        assert result.city_name == 'Paris'
        assert 'Europe/Paris' in result.timezone

    def test_working_hours_overlap(self):
        business_hours1 = BusinessHours(
            start="09:00",
            end="17:00",
            timezone="Europe/London"
        )
        business_hours2 = BusinessHours(
            start="09:00",
            end="17:00",
            timezone="Asia/Tokyo"
        )

        result = WorldTimeConverter.find_working_hours_overlap(
            'London',
            'Tokyo',
            business_hours1,
            business_hours2
        )

        assert isinstance(result.has_overlap, bool)
        assert isinstance(result.overlap_duration.hours, int)
        assert isinstance(result.overlap_duration.minutes, int)

    def test_invalid_business_hours(self):
        business_hours1 = BusinessHours(
            start="9:00",  # Invalid format
            end="17:00",
            timezone="Europe/London"
        )
        business_hours2 = BusinessHours(
            start="09:00",
            end="17:00",
            timezone="Asia/Tokyo"
        )

        with pytest.raises(InvalidTimeFormatError):
            WorldTimeConverter.find_working_hours_overlap(
                'London',
                'Tokyo',
                business_hours1,
                business_hours2
            )

    def test_holiday_management(self):
        holiday = HolidayDefinition(
            name="Christmas",
            date="2024-12-25",
            recurring=True,
            type="public"
        )

        WorldTimeConverter.add_holiday('London', holiday)

        is_holiday = WorldTimeConverter.is_holiday(
            'London',
            datetime(2024, 12, 25, tzinfo=pytz.UTC)
        )
        assert is_holiday is True

        is_holiday_next_year = WorldTimeConverter.is_holiday(
            'London',
            datetime(2025, 12, 25, tzinfo=pytz.UTC)
        )
        assert is_holiday_next_year is True

    def test_business_days_calculation(self):
        start_date = "2024-01-01"  # Monday
        end_date = "2024-01-05"  # Friday

        days = WorldTimeConverter.get_business_days_between(
            'London',
            start_date,
            end_date
        )
        assert days == 5

        # Test with weekend
        end_date = "2024-01-07"  # Sunday
        days = WorldTimeConverter.get_business_days_between(
            'London',
            start_date,
            end_date
        )
        assert days == 5

    def test_city_info(self):
        result = WorldTimeConverter.get_city_info('London')

        assert result.city_name == 'London'
        assert 'Europe' in result.region
        assert 'London' in result.subregion
        assert isinstance(result.is_dst, bool)