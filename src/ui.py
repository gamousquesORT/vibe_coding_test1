"""Handles the Streamlit user interface components."""
from typing import Tuple, Optional, Dict
from io import BytesIO
import streamlit as st
import pandas as pd
from .config import CONFIG, LOGOUT_JS

class StreamlitUI:
    """Handles the Streamlit user interface components."""
    
    @staticmethod
    def render_header():
        """Renders the application header with logout button."""
        # Add custom CSS for improved styling
        st.markdown("""
            <style>
                /* Main title styling */
                .main-title {
                    color: #1E88E5;
                    font-size: 2.5rem;
                    font-weight: 600;
                    margin-bottom: 1rem;
                    padding: 1rem 0;
                    border-bottom: 2px solid #1E88E5;
                }
                
                /* Section headers */
                .section-header {
                    color: #2196F3;
                    font-size: 1.2rem;
                    font-weight: 500;
                    margin: 1rem 0;
                    padding: 0.5rem 0;
                }
                
                /* Labels */
                .stTextInput > label, .stNumberInput > label {
                    font-size: 1.1rem !important;
                    font-weight: 500 !important;
                    color: #1976D2 !important;
                }
                
                /* Student table styling */
                .student-table {
                    height: 400px;
                    overflow-y: scroll;
                    padding: 1rem;
                    border: 1px solid #BBDEFB;
                    border-radius: 8px;
                    margin-bottom: 1rem;
                    background: #FFFFFF;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .student-row {
                    padding: 8px;
                    border-radius: 4px;
                    margin: 4px 0;
                }
                
                .student-row:focus-within {
                    background-color: #E3F2FD;
                }
                
                /* Team summary styling */
                .team-summary {
                    background: #E3F2FD;
                    padding: 1rem;
                    border-radius: 8px;
                    margin-top: 1rem;
                }
                
                .team-count {
                    font-size: 1.1rem;
                    color: #1976D2;
                }
                
                /* Column headers */
                .column-header {
                    font-size: 1.1rem;
                    font-weight: 500;
                    color: #1976D2;
                    padding: 0.5rem 0;
                    border-bottom: 2px solid #BBDEFB;
                    margin-bottom: 0.5rem;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Initialize session state for logout
        if 'logout_clicked' not in st.session_state:
            st.session_state.logout_clicked = False

        # Inject JavaScript
        st.markdown(LOGOUT_JS, unsafe_allow_html=True)
        
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown('<h1 class="main-title">IntedashBoard File Exporter</h1>', unsafe_allow_html=True)
        with col2:
            if st.button("Logout", type="primary", on_click=lambda: setattr(st.session_state, 'logout_clicked', True)):
                st.markdown('<script>closeTab();</script>', unsafe_allow_html=True)
                st.stop()
                
        if st.session_state.logout_clicked:
            st.markdown('<script>closeTab();</script>', unsafe_allow_html=True)
            st.stop()
            
        st.markdown('<p class="section-header">Process and manage student information efficiently</p>', unsafe_allow_html=True)

    @staticmethod
    def render_input_fields() -> Tuple[Optional[str], str, int]:
        """Renders input fields for section, filename, and number of teams."""
        st.markdown('<div class="section-header">Configuration</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            section = st.text_input("📚 Section", "")
            # Validate section input
            if not section or section.strip() == "":
                st.error("Section cannot be empty. Please enter a valid section.")
                section = None
        with col2:
            output_filename = st.text_input(
                "📄 Output Filename", 
                CONFIG['DEFAULT_FILENAME']
            )
        with col3:
            num_teams = st.number_input(
                "👥 Number of Teams",
                min_value=1,
                value=1,
                step=1
            )
        
        if not output_filename.endswith('.xlsx'):
            output_filename += '.xlsx'
            
        return section, output_filename, num_teams

    @staticmethod
    def display_team_summary(team_assignments: Dict[int, int], num_teams: int):
        """Displays a summary of how many students are in each team."""
        st.markdown('<div class="team-summary">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-header">📊 Team Summary</h3>', unsafe_allow_html=True)
        
        # Count students in each team
        team_counts = {i: 0 for i in range(1, num_teams + 1)}
        for team_num in team_assignments.values():
            if team_num in team_counts:
                team_counts[team_num] += 1
        
        # Create rows of 4 teams each for better layout
        teams_per_row = 4
        for i in range(0, num_teams, teams_per_row):
            cols = st.columns(teams_per_row)
            for j in range(teams_per_row):
                team_num = i + j + 1
                if team_num <= num_teams:
                    with cols[j]:
                        st.markdown(
                            f'<div class="team-count">Team {team_num}: <strong>{team_counts[team_num]}</strong> students</div>', 
                            unsafe_allow_html=True
                        )
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def render_student_selection(df: pd.DataFrame, num_teams: int) -> Dict[int, int]:
        """
        Renders the student selection interface with team assignment in a table format.
        Returns a dictionary mapping row indices to team numbers.
        """
        st.markdown('<h3 class="section-header">👨‍🎓 Assign Teams to Students</h3>', unsafe_allow_html=True)
        
        # Initialize session state for team assignments if not exists
        if 'team_assignments' not in st.session_state:
            st.session_state.team_assignments = {}

        # Add CSS to fix spacing
        st.markdown("""
            <style>
                div[data-testid="stHorizontalBlock"] {
                    margin-bottom: 0 !important;
                    padding-bottom: 0 !important;
                }
                div.student-table {
                    margin-top: 0 !important;
                    padding-top: 0.5rem !important;
                }
            </style>
        """, unsafe_allow_html=True)

        # Create column headers
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown('<div class="column-header">Student Name</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="column-header">Team (1-{num_teams})</div>', unsafe_allow_html=True)
        
        # Display student list immediately after headers
        team_assignments = {}
        for idx, row in df.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                student_info = f"{row['Last Name']}, {row['First Name']} ({row['Student ID']})"
                st.markdown(f'<div style="padding: 8px 0;">{student_info}</div>', unsafe_allow_html=True)
            with col2:
                # Get the current team number from session state or default to 0
                current_team = st.session_state.team_assignments.get(idx, 0)
                
                # Create a text input that only accepts numbers
                team_str = st.text_input(
                    "",  # Empty label
                    value=str(current_team),
                    key=f"team_{idx}",
                    label_visibility="collapsed",  # Hides the label completely
                    max_chars=3  # Limit to 3 digits
                )
                
                # Convert input to number and validate
                try:
                    team_num = int(team_str) if team_str.strip() else 0
                    # Validate team number is within range
                    if team_num < 0 or team_num > num_teams:
                        st.error(f"Team number must be between 1 and {num_teams}")
                        team_num = 0
                except ValueError:
                    team_num = 0
                    if team_str.strip():  # Only show error if something was entered
                        st.error("Please enter a valid number")
                    
                if team_num > 0:
                    team_assignments[idx] = team_num
                    st.session_state.team_assignments[idx] = team_num
                elif idx in st.session_state.team_assignments:
                    del st.session_state.team_assignments[idx]

        # Display team summary after all inputs
        StreamlitUI.display_team_summary(team_assignments, num_teams)
            
        return team_assignments

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