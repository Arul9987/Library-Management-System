from django import forms
from .models import Book   # or use get_user_model()
from .models import BookRequest

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = ['title', 'author', 'edition', 'volume']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Book Title'
            }),

            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Author Name'
            }),

            'edition': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Edition'
            }),

            'volume': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Volume'
            }),
        }