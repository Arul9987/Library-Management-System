from typing import Any

from datetime import datetime

from django.db import models
from django.conf import settings



class Category(models.Model):
    name: models.CharField[str] = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name



class Book(models.Model):
    title: models.CharField[str] = models.CharField(max_length=200)
    author: models.CharField[str] = models.CharField(max_length=200)
    category: models.ForeignKey[Category] = models.ForeignKey(Category, on_delete=models.CASCADE)
    edition: models.CharField[str] = models.CharField(max_length=50)
    volume: models.CharField[str] = models.CharField(max_length=50)
    total_copies: models.PositiveIntegerField[int] = models.PositiveIntegerField()
    available_copies: models.PositiveIntegerField[int] = models.PositiveIntegerField()
    img_url = models.ImageField(upload_to='book_covers/', blank=True)

    def __str__(self) -> str:
        return self.title


class BookRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    user: models.ForeignKey[Any] = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title: models.CharField[str] = models.CharField(max_length=200)
    author: models.CharField[str] = models.CharField(max_length=200)
    edition: models.CharField[str] = models.CharField(max_length=50)
    volume: models.CharField[str] = models.CharField(max_length=50)
    status: models.CharField[str] = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    requested_at: models.DateTimeField[datetime] = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.user.username}"