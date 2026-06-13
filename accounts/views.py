from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import get_user_model, login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, CustomUserUpdateForm, ForgotPasswordForm, UserRegisterForm
from .decorators import role_required

User = get_user_model()


# 🔹 LIST VIEW
class UserListView(View):
    def has_permission(self, request):
        return request.user.role in ["ADMIN", "LIBRARIAN"]
    def get(self, request):
        # Check login manually
        if not request.user.is_authenticated:
            return redirect('login')

        # Allow only Admin & Librarian
        if request.user.role not in ["ADMIN", "LIBRARIAN"]:
            raise PermissionDenied

        # 🎯 Role-based filtering
        if request.user.role == "LIBRARIAN":
            users = User.objects.filter(role="STUDENT")
        else:
            users = User.objects.all()

        return render(request, 'user_list.html', {'users': users})



# 🔹 CREATE VIEW (uses CustomUserCreationForm)
class UserCreateView(View):

    def get(self, request):
        form = CustomUserCreationForm(
            current_user=request.user   # ✅ pass current user
        )
        return render(request, 'user_form.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(
            request.POST,
            current_user=request.user   # ✅ pass current user
        )

        if form.is_valid():
            user = form.save(commit=False)

            # 🔐 Extra Security (very important)
            if request.user.role == "LIBRARIAN":
                user.role = "STUDENT"

            user.save()
            return redirect('user_list')

        return render(request, 'user_form.html', {'form': form})



# 🔹 DETAIL VIEW
class UserDetailView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'user_detail.html', {'user': user})


# 🔹 UPDATE VIEW (uses CustomUserUpdateForm)
class UserUpdateView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = CustomUserUpdateForm(
            instance=user,
            current_user=request.user   # ✅ IMPORTANT
        )
        return render(request, 'user_form.html', {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = CustomUserUpdateForm(
            request.POST,
            instance=user,
            current_user=request.user   # ✅ IMPORTANT
        )

        if form.is_valid():
            updated_user = form.save(commit=False)

            # 🔐 Extra Security (Very Important)
            if request.user.role == "LIBRARIAN":
                updated_user.role = "STUDENT"

            updated_user.save()
            return redirect('user_list')

        return render(request, 'user_form.html', {'form': form})



# 🔹 DELETE VIEW
class UserDeleteView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'user_delete.html', {'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('user_list')
     
# ================== REGISTER ==================
@never_cache
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})

# ================== LOGOUT ==================
@never_cache
def custom_logout(request):
    request.session.flush()
    logout(request)
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
# ================== DASHBOARD ROUTER ==================
@login_required(login_url='login')
@role_required(['STUDENT', 'LIBRARIAN', 'ADMIN'])
@never_cache
def dashboard(request):
    if request.user.role == "ADMIN" or request.user.role == "LIBRARIAN" or request.user.role == "STUDENT" :
        return render(request, 'dashboard/dashboard.html')
    else:
       return redirect('login') 

# ================== LOGIN ==================
@never_cache
def login_view(request):

    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in directly
            login(request, user)
            messages.success(request, "Login Successfully!")
            return redirect('dashboard')

        # Invalid credentials
        messages.error(request, "Invalid Username or Password")

    return render(request, "registration/login.html")


# ================== forgot password==================
User = get_user_model()

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect("forgot_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("forgot_password")

        user.set_password(new_password)
        user.save()

        messages.success(request, "Password reset successfully. Please login.")
        return redirect("login")

    return render(request, "registration/forgot_password.html")