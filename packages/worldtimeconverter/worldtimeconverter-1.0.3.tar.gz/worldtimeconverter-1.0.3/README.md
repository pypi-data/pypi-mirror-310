# World Time Converter

![Python Version](https://img.shields.io/pypi/pyversions/worldtimeconverter)
![PyPI Version](https://img.shields.io/pypi/v/worldtimeconverter)
![License](https://img.shields.io/pypi/l/worldtimeconverter)
![Downloads](https://img.shields.io/pypi/dm/worldtimeconverter)

A powerful Python library for handling worldwide time conversions, business hours calculations, and timezone management. Perfect for applications dealing with international time coordination, business hours overlap, and holiday scheduling.

## 🌟 Key Features

- 🌍 **Global Timezone Support**: Convert times between any cities worldwide
- 💼 **Business Hours Management**: Calculate working hours overlap across timezones
- 📅 **Holiday Handling**: Manage holidays and business days
- ⚡ **DST Aware**: Automatic handling of Daylight Saving Time transitions
- 🔍 **Type Hints**: Full typing support for better development experience
- 🛠️ **Extensible**: Easy to customize and extend

## 📦 Installation

```bash
pip install worldtimeconverter
```

## 🚀 Quick Start

```python
from worldtimeconverter import WorldTimeConverter
from worldtimeconverter.types import BusinessHours, HolidayDefinition
from datetime import datetime

# Get current time in any city
london = WorldTimeConverter.get_current_time('London')
print(f"London: {london.formatted_date_time}")
# Output: London: Friday, March 15, 2024 2:30:45 PM GMT

# Convert between cities
tokyo = WorldTimeConverter.convert_time(
    datetime.now(),
    'London',
    'Tokyo'
)
print(f"Tokyo: {tokyo.formatted_date_time}")
# Output: Tokyo: Saturday, March 16, 2024 11:30:45 PM JST
```

## 💡 Advanced Usage

### 🕒 Time Conversion & Formatting

```python
# Multiple ways to specify time
from datetime import datetime

# 1. Using timestamp string
time1 = WorldTimeConverter.convert_time(
    "2024-03-15 14:30:00",
    'New_York',
    'Singapore'
)

# 2. Using Unix timestamp
time2 = WorldTimeConverter.convert_time(
    1710512345,  # Unix timestamp
    'London',
    'Dubai'
)

# 3. Using datetime object
time3 = WorldTimeConverter.convert_time(
    datetime.now(),
    'Paris',
    'Sydney'
)

# Custom formatting
formatted = WorldTimeConverter.convert_time(
    datetime.now(),
    'London',
    'Tokyo',
    format='%Y-%m-%d %H:%M:%S %Z'
)
```

### 💼 Business Hours Management

```python
# Define business hours
london_hours = BusinessHours(
    start="09:00",
    end="17:00",
    timezone="Europe/London"
)

tokyo_hours = BusinessHours(
    start="09:00",
    end="18:00",
    timezone="Asia/Tokyo"
)

# Calculate overlap
overlap = WorldTimeConverter.find_working_hours_overlap(
    'London',
    'Tokyo',
    london_hours,
    tokyo_hours
)

print(f"""
Working Hours Overlap:
Start: {overlap.start_time}
End: {overlap.end_time}
Duration: {overlap.overlap_duration.hours}h {overlap.overlap_duration.minutes}m
Working Days: {', '.join(overlap.working_days)}
""")
```

### 📅 Holiday Management

```python
# Define holidays
christmas = HolidayDefinition(
    name="Christmas Day",
    date="2024-12-25",
    recurring=True,
    type="public"
)

new_year = HolidayDefinition(
    name="New Year's Day",
    date="2024-01-01",
    recurring=True,
    type="public"
)

# Add holidays to cities
WorldTimeConverter.add_holiday('London', christmas)
WorldTimeConverter.add_holiday('London', new_year)

# Check holidays
is_christmas = WorldTimeConverter.is_holiday(
    'London',
    datetime(2024, 12, 25)
)

# Calculate business days
business_days = WorldTimeConverter.get_business_days_between(
    'London',
    '2024-01-01',
    '2024-01-10',
    skip_holidays=True
)
```

### 🌐 Timezone Information

```python
# Get detailed city information
city_info = WorldTimeConverter.get_city_info('London')
print(f"""
City: {city_info.city_name}
Timezone: {city_info.timezone}
Current Offset: {city_info.current_offset}
DST Active: {city_info.is_dst}
Region: {city_info.region}
Subregion: {city_info.subregion}
""")
```

## 📋 Type Definitions

```python
from dataclasses import dataclass
from typing import List

@dataclass
class TimeResult:
    city_name: str
    timezone: str
    local_time: str
    utc_offset: str
    date: str
    day_of_week: str
    is_dst: bool
    epoch: int
    iso8601: str
    formatted_date_time: str

@dataclass
class BusinessHours:
    start: str  # HH:MM format
    end: str    # HH:MM format
    timezone: str

@dataclass
class HolidayDefinition:
    name: str
    date: str  # YYYY-MM-DD format
    recurring: bool
    type: str
```

## 🔍 Error Handling

```python
from worldtimeconverter.exceptions import InvalidCityError, InvalidTimeFormatError

try:
    time = WorldTimeConverter.get_current_time('InvalidCity')
except InvalidCityError as e:
    print(f"City error: {e}")

try:
    hours = BusinessHours(start="9:00", end="17:00", timezone="Europe/London")
except InvalidTimeFormatError as e:
    print(f"Time format error: {e}")
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

For more detailed documentation and examples, visit our [GitHub Wiki](https://github.com/OrenGrinker/worldtimeconverter/wiki).
