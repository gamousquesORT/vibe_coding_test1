"""Handles the Streamlit user interface components."""
from typing import Tuple, Optional
from io import BytesIO
import streamlit as st
import pandas as pd
from .config import CONFIG, LOGOUT_JS

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
            # Validate section input
            if not section or section.strip() == "":
                st.error("Section cannot be empty. Please enter a valid section.")
                section = None
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