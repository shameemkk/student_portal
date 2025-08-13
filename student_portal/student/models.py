from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=10, unique=True)
    course = models.CharField(max_length=100)
    year_of_study = models.IntegerField()
    address = models.EmailField(unique=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.student_id}"