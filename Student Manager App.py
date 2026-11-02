std={}

while True:
    print("1. Add Student")
    print("2. View Students")
    print("3. Check Results")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        name = input("Enter student name: ")
        marks = int(input("Enter student marks: "))
        std[name] = marks  #automatically update in dictionary
        print(f"Student {name} added successfully.")
    
    elif choice == '2':
        if not std:
            print("No students found.")
        else:
            print("Student List:")
            for name, marks in std.items(): #
                print(f"Name: {name}, Marks: {marks}")
    
    elif choice == '3':
        name = input("Enter student name to check results: ")
        if name in std:
            marks = std[name] #check dict[key] to get value
            
            if marks >= 40:
                print(f"Name: {name}, Marks: {marks}, Passed")
            else:
                print(f"Name: {name}, Marks: {marks}, Failed")
        else:
            print(f"Student {name} not found.")
    
    elif choice == '4':
        name = input("Enter student name to update: ")
        if name in std:
            marks = int(input("Enter new marks: "))
            std[name] = marks
            print(f"Student {name} updated successfully.")
        else:
            print(f"Student {name} not found.")

    elif choice == '5':
        name = input("Enter student name to delete: ")
        if name in std:
            del std[name]
            print(f"Student {name} deleted successfully.")
        else:
            print(f"Student {name} not found.")
    
    elif choice == '6':
        print("Exiting the program.")
        break
    
    else:
        print("Invalid choice. Please try again.")
        
        
        
        
"""
Output:
1. Add Student
2. View Students
3. Check Results
4. Update Student
5. Delete Student
6. Exit
Enter your choice: 1
Enter student name: Ridhi Patil
Enter student marks: 56
Student Ridhi Patil added successfully.
1. Add Student
2. View Students
3. Check Results
4. Update Student
5. Delete Student
6. Exit
Enter your choice: 1
Enter student name: Aarti Patil
Enter student marks: 32
Student Aarti Patil added successfully.
1. Add Student
2. View Students
3. Check Results
4. Update Student
5. Delete Student
6. Exit
Enter your choice: 2
Student List:
Name: Ridhi Patil, Marks: 56
Name: Aarti Patil, Marks: 32
1. Add Student
2. View Students
3. Check Results
4. Update Student
5. Delete Student
6. Exit
Enter your choice: 3
Enter student name to check results: Aarti Patil
Name: Aarti Patil, Marks: 32, Failed
1. Add Student
2. View Students
3. Check Results
4. Update Student
5. Delete Student
6. Exit
Enter your choice: 4
Enter student name to update: Aarti Patil
Enter new marks: 45
Student Aarti Patil updated successfully.
1. Add Student
2. View Students
3. Check Results
4. Update Student
5. Delete Student
6. Exit
Enter your choice: 2
Student List:
Name: Ridhi Patil, Marks: 56
Name: Aarti Patil, Marks: 45
1. Add Student
2. View Students
3. Check Results
4. Update Student
5. Delete Student
6. Exit
Enter your choice: 5
Enter student name to delete: Ridhi Patil
Student Ridhi Patil deleted successfully.
1. Add Student
2. View Students
3. Check Results
4. Update Student
5. Delete Student
6. Exit
Enter your choice: 2
Student List:
Name: Aarti Patil, Marks: 45
1. Add Student
2. View Students
3. Check Results
4. Update Student
5. Delete Student
6. Exit
Enter your choice: 6
Exiting the program. 
"""