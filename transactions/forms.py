from django import forms
from django.core.exceptions import ValidationError
from .models import BorrowBook
from django.contrib.auth import get_user_model
from books.models import Book
from books.models import Category


User = get_user_model()


class ManualBorrowForm(forms.ModelForm):

    class Meta:
        model = BorrowBook
        fields = ['student', 'category', 'book', 'due_date']      #'borrow_date'

        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),

            'category': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_category'
            }),

            'book': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_book'
            }),

            # 'borrow_date': forms.DateInput(attrs={
            #     'class': 'form-control',
            #     'type': 'date'
            # }),

            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show only STUDENT users
        self.fields['student'].queryset = User.objects.filter(role='STUDENT')

        # Initially show NO books
        self.fields['book'].queryset = Book.objects.none()

        # Load books if category selected
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))

                self.fields['book'].queryset = Book.objects.filter(
                    category_id=category_id,
                    available_copies__gt=0
                )

            except (ValueError, TypeError):
                pass
    # Prevent duplicate borrow
    def clean(self):
        cleaned_data = super().clean()

        student = cleaned_data.get('student')
        book = cleaned_data.get('book')

        if student and book:
            exists = BorrowBook.objects.filter(
                student=student,
                book=book,
                status__in=['PENDING', 'APPROVED']
            ).exists()

            if exists:
                raise ValidationError(
                    "⚠ This student already requested or borrowed this book."
                )

        return cleaned_data