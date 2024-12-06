# worldtimeconverter/types.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

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
class TimeInterval:
    hours: int
    minutes: int

@dataclass
class WorkingHoursOverlap:
    start_time: str
    end_time: str
    overlap_duration: TimeInterval
    has_overlap: bool
    working_days: List[str]

@dataclass
class HolidayDefinition:
    name: str
    date: str  # YYYY-MM-DD format
    recurring: bool
    type: str

@dataclass
class CityInfo:
    city_name: str
    timezone: str
    current_offset: str
    is_dst: bool
    region: str
    subregion: str