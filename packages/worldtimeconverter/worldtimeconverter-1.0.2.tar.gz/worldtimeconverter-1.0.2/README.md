# World Time Converter

A comprehensive Python library for handling worldwide time conversions, business hours calculations, and timezone management.

## Features

- Global timezone conversion
- Business hours overlap calculation
- Holiday management
- Business days calculation
- DST handling
- Timezone information
- Type hints support

## Installation

```bash
pip install worldtimeconverter
```

## Quick Start

```python
from worldtimeconverter import WorldTimeConverter
from worldtimeconverter.types import BusinessHours

# Get current time in a city
london_time = WorldTimeConverter.get_current_time('London')
print(london_time.local_time)  # '14:30:45'

# Convert time between cities
tokyo_time = WorldTimeConverter.convert_time(
    "2024-01-01 12:00:00",
    'London',
    'Tokyo'
)
print(tokyo_time.local_time)  # '21:00:00'

# Calculate business hours overlap
overlap = WorldTimeConverter.find_working_hours_overlap(
    'London',
    'Tokyo',
    BusinessHours(start="09:00", end="17:00", timezone="Europe/London"),
    BusinessHours(start="09:00", end="17:00", timezone="Asia/Tokyo")
)
print(f"Overlap duration: {overlap.overlap_duration.hours}h {overlap.overlap_duration.minutes}m")
```

## Detailed Usage

### Time Conversion

```python
# Using Unix timestamp
timestamp = int(datetime.now().timestamp())
paris_time = WorldTimeConverter.convert_time(
    timestamp,
    'New_York',
    'Paris'
)

# Using datetime string
custom_time = WorldTimeConverter.convert_time(
    "2024-01-01 15:30:00",
    'London',
    'Tokyo',
    format='%Y-%m-%d %H:%M:%S'
)
```

### Holiday Management

```python
from worldtimeconverter.types import HolidayDefinition

# Add a holiday
holiday = HolidayDefinition(
    name="Christmas Day",
    date="2024-12-25",
    recurring=True,
    type="public"
)
WorldTimeConverter.add_holiday('London', holiday)

# Check if date is a holiday
is_holiday = WorldTimeConverter.is_holiday(
    'London',
    datetime(2024, 12, 25)
)
```

### Business Days Calculation

```python
# Calculate business days between dates
days = WorldTimeConverter.get_business_days_between(
    'London',
    '2024-01-01',
    '2024-01-05',
    skip_holidays=True
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```
