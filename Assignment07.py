# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Andy Sul,11/23/2024,Modified Script
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.

class Person:
    """Represents a person"""

    def __init__(self, first_name: str = "", last_name: str = ""):
        self._first_name = first_name
        self._last_name = last_name

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        if not value:
            raise ValueError("First name cannot be empty.")
        self._first_name = value

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if not value:
            raise ValueError("Last name cannot be empty.")
        self._last_name = value

    def __str__(self) -> str:
        return f"Person [First Name: {self.first_name}, Last Name: {self.last_name}]"

class Student(Person):
    """Represents a student"""

    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        super().__init__(first_name, last_name)
        self._course_name = course_name

    @property
    def course_name(self) -> str:
        return self._course_name

    @course_name.setter
    def course_name(self, value: str):
        if not value:
            raise ValueError("Course name cannot be empty.")
        self._course_name = value

    def __str__(self) -> str:
        return f"Student [First Name: {self.first_name}, Last Name: {self.last_name}, Course Name: {self.course_name}]"

# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list) -> list:
        """ This function reads data from a json file and loads it into a list of Student objects

        :param file_name: string data with name of file to read from
        :param student_data: list of Student objects to be filled with file data

        :return: list
        """

        try:
            with open(file_name, "r") as file:
                data = json.load(file)
                for item in data:
                    student = Student(first_name=item["FirstName"], last_name=item["LastName"], course_name=item["CourseName"])
                    student_data.append(student)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)

        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of Student objects

        :param file_name: string data with name of file to write to
        :param student_data: list of Student objects to be written to the file

        :return: None
        """

        try:
            with open(file_name, "w") as file:
                data = []
                for student in student_data:
                    item = {
                        "FirstName": student.first_name,
                        "LastName": student.last_name,
                        "CourseName": student.course_name
                    }
                    data.append(item)
                json.dump(data, file, indent=4)
            print("Data successfully saved to file.")
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)

# Presentation --------------------------------------- #
class IO:

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays custom error messages to the user

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice() -> str:
        """ This function gets a menu choice from the user

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name, last name, and course name from the user

        :param student_data: list of Student objects to be filled with input data

        :return: list
        """
        try:
            student_first_name = input("Enter the student's first name: ").strip()
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ").strip()
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ").strip()
            student = Student(first_name=student_first_name, last_name=student_last_name, course_name=course_name)
            student_data.append(student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the incorrect type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


def output_student_and_course_names(student_data: list):
    """ This function displays the student and course names to the user

    :param student_data: list of Student objects to be displayed

    :return: None
    """
    print("-" * 50)
    for student in student_data:
        if isinstance(student, dict): # Check if the student is a dictionary
            print(f"Student {student['FirstName']} {student['LastName']} is enrolled in {student['CourseName']}")
        else: # Otherwise, treat it as a Student object
            print(f"Student {student.first_name} {student.last_name} is enrolled in {student.course_name}")
    print("-" * 50)


# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while True:

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        output_student_and_course_names(student_data=students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, 3, or 4")

print("Program Ended")

