write a python script to read the names on the Nombre column of an input excel file and write a new excel file with the following columns:
First Name
Last Name
Email
Student ID
Section
Team
Remarks

The input file has on the Nombre column a string with the following format Last Name, First Name (Student ID)
Split the Nombre Cell string into the corresponding columns of the output file, use the names
Leave blank the following columns
Email
Section
Team
Remarks

use a virtual environment to install packages
Ask the user to choose the path of the input and output files

---

add to the python script a web user interface using streamlit framewok

the user interface asks for the input file but it does not allow to input the output file

--

change the title Student Data Processor to IntedashBoard file exporter

An error occurred: NDFrame.to_excel() missing 1 required positional argument: 'excel_writer

put classes code in separate files

[process_excel.py]():162-185

do not display thelabel Tem fo `<student>` on each row. make the input more like a table. student and team input filed on the same row

--

add a sumary fields to show how many students are in aevery team while the user inputs the team numbers

---

before the user selects to process file check that all students have a team assigned and warn the user, dont block him


--


there is a empty squared draw under the labels student name and Team and before the student list. remove it
Pasted Image

[config.py]():1-24
