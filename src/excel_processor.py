"""Handles Excel file processing functionality."""
from typing import Optional
import pandas as pd
from .models import StudentData
from .config import CONFIG

class ExcelProcessor:
    """Handles the processing of Excel files containing student information."""
    
    @staticmethod
    def process_nombre(nombre: str) -> StudentData:
        """
        Extracts student information from a formatted string.
        Format: "Last Name, First Name (Student ID)"
        """
        try:
            if not isinstance(nombre, str):
                return StudentData('', '', '')
                
            # Split the name and ID parts
            parts = nombre.split('(', 1)
            if len(parts) != 2:
                return StudentData('', '', '')
                
            name_part = parts[0].strip()
            id_part = parts[1].replace(')', '').strip()
            
            # Split last name and first name
            name_parts = name_part.split(',', 1)
            if len(name_parts) != 2:
                return StudentData('', '', '')
                
            last_name = name_parts[0].strip()
            first_name = name_parts[1].strip()
            
            return StudentData(first_name, last_name, id_part)
        except Exception:
            return StudentData('', '', '')

    @staticmethod
    def process_dataframe(df: pd.DataFrame, section: str) -> Optional[pd.DataFrame]:
        """Processes the input DataFrame and returns a new DataFrame with required columns."""
        if 'Nombre' not in df.columns:
            raise ValueError("'Nombre' column not found in the input file")

        # Process each row and create new columns
        processed_data = []
        for nombre in df['Nombre']:
            student = ExcelProcessor.process_nombre(str(nombre))
            processed_data.append({
                'First Name': student.first_name,
                'Last Name': student.last_name,
                'Email': '',
                'Student ID': student.student_id,
                'Section': section,
                'Team': '',
                'Remarks': ''
            })
        
        return pd.DataFrame(processed_data)