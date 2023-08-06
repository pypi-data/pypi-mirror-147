from .logger import geoLogger
from coopstructs.vectors import Vector2

class DuplicatePointException(Exception):
    def __init__(self, point: Vector2):
        geoLogger.error(f"Unable to process the point {point} because it is a duplicate")
        super().__init__()

