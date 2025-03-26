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
                
                # Get input fields including number of teams
                section, output_filename, num_teams = StreamlitUI.render_input_fields()
                
                # Show student selection and team assignment interface with validation
                team_assignments = StreamlitUI.render_student_selection(initial_df, num_teams)
                
                if st.button("Process File"):
                    if section is None:
                        st.error("Please enter a valid section before processing the file.")
                        return
                    
                    # Check for unassigned students
                    total_students = len(initial_df)
                    assigned_students = len(team_assignments)
                    if assigned_students < total_students:
                        st.warning(f"⚠️ {total_students - assigned_students} students have not been assigned to any team. You can still proceed if this is intended.")
                    
                    # Validate all team assignments are within range
                    invalid_teams = [team for team in team_assignments.values() 
                                   if team < 1 or team > num_teams]
                    if invalid_teams:
                        st.error(f"All team numbers must be between 1 and {num_teams}")
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