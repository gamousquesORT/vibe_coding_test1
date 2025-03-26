"""Main entry point for the IntedashBoard File Exporter application."""
import streamlit as st
import pandas as pd
from src.ui import StreamlitUI
from src.excel_processor import ExcelProcessor

def main():
    """Main application entry point."""
    try:
        # Render UI components
        StreamlitUI.render_header()
        
        # File uploader
        uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                # Read the Excel file and create initial DataFrame
                df = pd.read_excel(uploaded_file)
                initial_df = ExcelProcessor.process_dataframe(df, "", {})
                
                # Get input fields
                section, output_filename = StreamlitUI.render_input_fields()
                
                # Show student selection and team assignment interface
                team_assignments = StreamlitUI.render_student_selection(initial_df)
                
                if st.button("Process File"):
                    if section is None:
                        st.error("Please enter a valid section before processing the file.")
                        return
                        
                    try:
                        # Process the Excel file with team assignments
                        processed_df = ExcelProcessor.process_dataframe(df, section, team_assignments)
                        
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
                st.error(f"Error reading file: {str(e)}")
    
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()