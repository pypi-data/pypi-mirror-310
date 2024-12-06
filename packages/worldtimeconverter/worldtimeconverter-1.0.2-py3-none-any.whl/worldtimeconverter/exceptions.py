# worldtimeconverter/exceptions.py
class WorldTimeConverterError(Exception):
    """Base exception for WorldTimeConverter."""
    pass

class InvalidCityError(WorldTimeConverterError):
    """Raised when a city name is invalid or not found."""
    pass

class InvalidTimeFormatError(WorldTimeConverterError):
    """Raised when time format is invalid."""
    pass