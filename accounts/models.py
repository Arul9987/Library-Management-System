from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('LIBRARIAN', 'Librarian'),
        ('STUDENT', 'Student'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    contact = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    email = models.EmailField(unique=True)

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_librarian(self):
        return self.role == 'LIBRARIAN'

    def is_student(self):
        return self.role == 'STUDENT'

    def is_active_user(self):
        return self.is_active

    def __str__(self):
        return self.username

