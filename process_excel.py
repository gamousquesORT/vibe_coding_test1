import pandas as pd
import streamlit as st
from io import BytesIO

def process_nombre(nombre):
    # Extract Last Name, First Name, and Student ID from the string
    # Format: "Last Name, First Name (Student ID)"
    try:
        # Split the name and ID parts
        name_part = nombre.split('(')[0].strip()
        id_part = nombre.split('(')[1].replace(')', '').strip()
        
        # Split last name and first name
        last_name, first_name = map(str.strip, name_part.split(','))
        
        return first_name, last_name, id_part
    except:
        return '', '', ''

def main():
    # Add logout button in the top right
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("IntedashBoard File Exporter")
    with col2:
        if st.button("Logout", type="primary"):
            st.stop()
            
    st.write("This app processes Excel files containing student information.")

    # File uploader
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        # Input section and output filename
        col1, col2 = st.columns(2)
        with col1:
            section = st.text_input("Enter the section:", "")
        with col2:
            output_filename = st.text_input("Enter output filename:", "processed_students.xlsx")
        
        if not output_filename.endswith('.xlsx'):
            output_filename += '.xlsx'
            
        if st.button("Process File"):
            try:
                # Read the input Excel file
                df = pd.read_excel(uploaded_file)
                
                # Check if 'Nombre' column exists
                if 'Nombre' not in df.columns:
                    st.error("Error: 'Nombre' column not found in the input file")
                    return

                # Process each row and create new columns
                first_names = []
                last_names = []
                student_ids = []

                for nombre in df['Nombre']:
                    first_name, last_name, student_id = process_nombre(str(nombre))
                    first_names.append(first_name)
                    last_names.append(last_name)
                    student_ids.append(student_id)
                
                # Create new DataFrame with required columns
                new_df = pd.DataFrame({
                    'First Name': first_names,
                    'Last Name': last_names,
                    'Email': '',  # Empty column
                    'Student ID': student_ids,
                    'Section': section,  # Apply section to all rows
                    'Team': '',  # Empty column
                    'Remarks': ''  # Empty column
                })

                # Show preview of processed data
                st.write("Preview of processed data:")
                st.dataframe(new_df)

                # Create an in-memory Excel file
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    new_df.to_excel(writer, index=False)
                
                # Create download button
                st.download_button(
                    label="Download processed Excel file",
                    data=buffer.getvalue(),
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("File processed successfully!")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()