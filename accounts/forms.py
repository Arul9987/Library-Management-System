from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm
from .models import User


# ==============================
# CREATE USER FORM (Admin / Librarian)
# ==============================
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'contact', 'address', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        # 🔐 If Librarian → Only STUDENT
        if current_user and current_user.role == "LIBRARIAN":
            self.fields['role'].choices = [
                ('STUDENT', 'Student')
            ]


# ==============================
# UPDATE USER FORM
# ==============================

class CustomUserUpdateForm(UserChangeForm):

    password = None

    # ✅ define field here
    is_active = forms.ChoiceField(
        choices=[(True, "Active"), (False, "Inactive")],
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'contact', 'address', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        # Librarian can only update Student
        if current_user and current_user.role == "LIBRARIAN":
            self.fields['role'].choices = [
                ('STUDENT', 'Student')
            ]

        # hide is_active when creating user
        if not self.instance.pk:
            self.fields.pop('is_active')

# ==============================
# STUDENT REGISTER FORM
# ==============================
class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'contact', 'address', 'password1', 'password2']
        widgets = {
    'username': forms.TextInput(attrs={
        'class': 'form-control rounded-end-5',
        'placeholder': 'Enter username',
        'required': True,
        'pattern': '^[A-Za-z0-9]{3,20}$',
        'title': 'Username must be 3-20 characters (letters, numbers only)'
    }),

    'email': forms.EmailInput(attrs={
        'class': 'form-control rounded-end-5',
        'placeholder': 'Enter email',
        'required': True,
        'pattern': '[^@]+@[^@]+\.[a-zA-Z]{2,6}',
        'title': 'Enter a valid email address'
    }),

    'role': forms.Select(attrs={
        'class': 'form-select',
        'required': True
    }),

    'contact': forms.TextInput(attrs={
        'class': 'form-control rounded-end-5',
        'placeholder': 'Enter contact number',
        'required': True,
        'pattern': '[0-9]{10}',
        'title': 'Contact number must be exactly 10 digits'
    }),

    'address': forms.Textarea(attrs={
        'class': 'form-control rounded-5',
        'rows': 3,
        'required': True,
        'minlength': '5',
        'title': 'Address must be at least 5 characters'
    }),
}
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-start-5'})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-start-5'})
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "STUDENT"   # 🔐 Force student role
        if commit:
            user.save()
        return user

#login
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control rounded-end-5', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-end-5', 'placeholder': 'Enter password'})
    )


class ForgotPasswordForm(forms.Form):
    email= forms.EmailField(label='Email',max_length=254 ,required='true')

    def clean(self):
        cleaned_data = super().clean()
        email =cleaned_data.get('email')

        if not User.objects.filter(email = email).exists():
            raise  forms.ValidationError("NO User Rejistered with this email")

