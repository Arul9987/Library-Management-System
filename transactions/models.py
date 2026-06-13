from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from django.db import models
from datetime import timedelta
from books.models import Book,Category

class BorrowBook(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('RETURNED', 'Returned'),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    borrow_date = models.DateField(auto_now_add=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        ordering = ['-borrow_date']

    def __str__(self):
        return f"{self.book.title} - {self.student.username}"

    # 🚀 Prevent duplicate active borrow
    def clean(self):
        if self.status in ['PENDING', 'APPROVED']:
            exists = BorrowBook.objects.filter(
                student=self.student,
                book=self.book,
                status__in=['PENDING', 'APPROVED']
            ).exclude(pk=self.pk).exists()

            if exists:
                raise ValidationError("You already requested or borrowed this book.")




