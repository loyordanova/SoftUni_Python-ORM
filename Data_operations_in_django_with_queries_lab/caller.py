import os
import django

from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Student

# first_exercise ----------------------------------------------------------------------------------

def add_students():
    student1 = Student(
        student_id="FC5204",
        first_name="John",
        last_name="Doe",
        birth_date="1995-05-15",
        email="john.doe@university.com"
    )
    student1.save()

    student2 = Student(
        student_id="FE0054",
        first_name="Jane",
        last_name="Smith",
        birth_date=None,
        email="jane.smith@university.com"
    )
    student2.save()

    student3 = Student(
        student_id="FH2014",
        first_name="Alice",
        last_name="Johnson",
        birth_date="1998-02-10",
        email="alice.johnson@university.com"
    )
    student3.save()

    student4 = Student(
        student_id="FH2015",
        first_name="Bob",
        last_name="Wilson",
        birth_date="1996-11-25",
        email="bob.wilson@university.com"
    )
    student4.save()

# this can be made with create() also
    
# Student.objects.create(
#    student_id="FH2015",
#    first_name="Bob",
#    last_name="Wilson",
#    birth_date="1996-11-25",
#    email="bob.wilson@university.com" 
# )

# add_students()
# print(Student.objects.all())

# second_exercise -----------------------------------------------------------------------------------------

def get_students_info():
    students_data = []

    for student in Student.objects.all():
        students_data.append(
            f'Student №{student.student_id}: {student.first_name} {student.last_name}; Email: {student.email}'
            )
    
    return '\n'.join(students_data)

# print(get_students_info())

# third_exercise -----------------------------------------------------------------------------------------

def update_students_emails():
    students = Student.objects.all()

    for student in students:
        email_parts = student.email.split('@')
        new_email = f'{email_parts[0]}@uni-students.com'
        student.email = new_email
        student.save()

    # another way to solve this using replace

    # for student in students:
    #     new_email = student.email.replace('university.com', 'uni-students.com')
    #     student.email = new_email
    #     student.save()
        
# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)

# forth_exercise -----------------------------------------------------------------------------------------
    
def truncate_students():
    Student.objects.all().delete()

# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")
