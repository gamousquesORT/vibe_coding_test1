"""Data models for the application."""
from dataclasses import dataclass

@dataclass
class StudentData:
    """Represents processed student information."""
    first_name: str
    last_name: str
    student_id: str