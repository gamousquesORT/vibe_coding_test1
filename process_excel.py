import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog

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
    # Create a root window but hide it
    root = tk.Tk()
    root.withdraw()

    # Ask for input file
    print("Please select the input Excel file...")
    input_file = filedialog.askopenfilename(
        title="Select input Excel file",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    
    if not input_file:
        print("No input file selected. Exiting...")
        return

    # Ask for output file location
    print("Please select where to save the output Excel file...")
    output_file = filedialog.asksaveasfilename(
        title="Save output Excel file",
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")]
    )
    
    if not output_file:
        print("No output location selected. Exiting...")
        return

    try:
        # Read the input Excel file
        df = pd.read_excel(input_file)
        
        # Check if 'Nombre' column exists
        if 'Nombre' not in df.columns:
            print("Error: 'Nombre' column not found in the input file")
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

        # Ask for section
        section = simpledialog.askstring("Input", "Please enter the section:")
        if section is None:  # If user clicks Cancel
            section = ""     # Use empty string as default
        
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

        # Save to new Excel file
        new_df.to_excel(output_file, index=False)
        print(f"Successfully processed the file. Output saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()