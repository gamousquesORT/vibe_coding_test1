import pandas as pd
import streamlit as st
from io import BytesIO
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass

# Configuration
CONFIG = {
    'REQUIRED_COLUMNS': ['Nombre'],
    'OUTPUT_COLUMNS': [
        'First Name', 'Last Name', 'Email', 'Student ID', 
        'Section', 'Team', 'Remarks'
    ],
    'DEFAULT_FILENAME': 'processed_students.xlsx'
}

# JavaScript for handling logout
LOGOUT_JS = """
<script>
    function closeTab() {
        // Try to close the tab
        window.close();
        
        // If the tab doesn't close, redirect to a blank page
        setTimeout(function() {
            window.location.href = 'about:blank';
        }, 100);
    }
</script>
"""

@dataclass
class StudentData:
    first_name: str
    last_name: str
    student_id: str

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

class StreamlitUI:
    """Handles the Streamlit user interface components."""
    
    @staticmethod
    def render_header():
        """Renders the application header with logout button."""
        # Initialize session state for logout
        if 'logout_clicked' not in st.session_state:
            st.session_state.logout_clicked = False

        # Inject JavaScript
        st.markdown(LOGOUT_JS, unsafe_allow_html=True)
        
        col1, col2 = st.columns([6, 1])
        with col1:
            st.title("IntedashBoard File Exporter")
        with col2:
            if st.button("Logout", type="primary", on_click=lambda: setattr(st.session_state, 'logout_clicked', True)):
                st.markdown('<script>closeTab();</script>', unsafe_allow_html=True)
                st.stop()
                
        if st.session_state.logout_clicked:
            st.markdown('<script>closeTab();</script>', unsafe_allow_html=True)
            st.stop()
            
        st.write("This app processes Excel files containing student information.")

    @staticmethod
    def render_input_fields() -> Tuple[Optional[str], str]:
        """Renders input fields for section and filename."""
        col1, col2 = st.columns(2)
        with col1:
            section = st.text_input("Enter the section:", "")
        with col2:
            output_filename = st.text_input(
                "Enter output filename:", 
                CONFIG['DEFAULT_FILENAME']
            )
        
        if not output_filename.endswith('.xlsx'):
            output_filename += '.xlsx'
            
        return section, output_filename

    @staticmethod
    def create_excel_download(df: pd.DataFrame, filename: str):
        """Creates and displays the Excel download button."""
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        
        st.download_button(
            label="Download processed Excel file",
            data=buffer.getvalue(),
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

def main():
    """Main application entry point."""
    try:
        # Render UI components
        StreamlitUI.render_header()
        
        # File uploader
        uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            # Get input fields
            section, output_filename = StreamlitUI.render_input_fields()
            
            if st.button("Process File"):
                try:
                    # Read and process the Excel file
                    df = pd.read_excel(uploaded_file)
                    processed_df = ExcelProcessor.process_dataframe(df, section)
                    
                    if processed_df is not None:
                        # Show preview and download button
                        st.write("Preview of processed data:")
                        st.dataframe(processed_df)
                        StreamlitUI.create_excel_download(processed_df, output_filename)
                        st.success("File processed successfully!")
                        
                except ValueError as ve:
                    st.error(f"Validation error: {str(ve)}")
                except Exception as e:
                    st.error(f"An error occurred while processing the file: {str(e)}")
    
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()