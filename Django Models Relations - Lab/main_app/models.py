from datetime import date
from django.db import models

# 01. The Lecturer ---------------------------------------------------------

class Lecturer(models.Model):
    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )


class Subject(models.Model):
    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=10
    )

    lecturer = models.ForeignKey(
        to='Lecturer', 
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f'{self.name}'

# 01. The Student ---------------------------------------------------------
    
class Student(models.Model):
    student_id = models.CharField(
        max_length=10,
        primary_key=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    birth_date = models.DateField()

    email = models.EmailField(
        unique=True
    )

    subjects = models.ManyToManyField(
        'Subject',
        through='StudentEnrollment'
    )

# 03. The Enrollment ---------------------------------------------------------

class StudentEnrollment(models.Model):
    GRADES_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F')
    )

    student = models.ForeignKey(
        to='Student',
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        to='Subject',
        on_delete=models.CASCADE
    )

    enrollment_date = models.DateField(
        default=date.today
    )

    grade = models.CharField(
        max_length=1,
        choices=GRADES_CHOICES
    )

# 04. The Lecturer Profile --------------------------------------------------

class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(
        to='Lecturer',
        on_delete=models.CASCADE
    )

    email = models.EmailField(
        unique=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    office_location = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )