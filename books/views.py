from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .forms import BookForm
from.models import Book
from .forms import BookRequestForm
from .models import BookRequest
from django.db.models import Q

#****** home page *******
def home(request):
    query = request.GET.get('q')   # get search text

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__name__icontains=query)
        )
    return render(request, 'home.html', {'books': books})

#****** about page *******
def about(request):
    return render(request,'about.html')
#****** feature page *******
def features (request):
    return render(request,'feature.html')

class BookListView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        query = request.GET.get('q')   # get search text

        books = Book.objects.all()

        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(category__name__icontains=query)
            )

        return render(request, 'books.html', {'books': books})
    
class BookCreate(View) :
    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.role not in ["ADMIN"]:
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = BookForm()
        return render(request,'book_form.html',{'form':form})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('book_list')   # redirect after saving

        return render(request, 'book_form.html', {'form': form})

class BookDetailView(View):
    def dispatch(self, request, *args, **kwargs):

        # check if user is logged in
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'book_detail.html', {'book': book})

class BookDeleteView(View):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.role != "ADMIN":
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'book_delete.html', {'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return redirect('book_list')

class BookUpdateView(View):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.role not in ["ADMIN"]:
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)

    # Show form with existing book data
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(instance=book)
        return render(request, 'book_form.html', {'form': form})

    # Handle form submission
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            form.save()
            return redirect('book_list')

        return render(request, 'book_form.html', {'form': form})


# ***********************book request ************************* 
class RequestBookView(View):

    def get(self, request):
        if request.user.role not in ["STUDENT", "LIBRARIAN"]:
            return redirect('dashboard')

        form = BookRequestForm()
        return render(request, 'request_book.html', {'form': form})

    def post(self, request):
        if request.user.role not in ["STUDENT", "LIBRARIAN"]:
            return redirect('dashboard')

        form = BookRequestForm(request.POST)
        if form.is_valid():
            book_request = form.save(commit=False)
            book_request.user = request.user
            book_request.save()
            return redirect('request_list')

        return render(request, 'request_book.html', {'form': form})

# ***********************book request List *************************    
class BookRequestListView(View):
    def get(self, request):

        # ADMIN → See All
        if request.user.role == "ADMIN":
            requests = BookRequest.objects.all()

        # STUDENT & LIBRARIAN → See Only Their Own
        else:
            requests = BookRequest.objects.filter(user=request.user)

        return render(request, 'request_list.html', {
            'requests': requests
        })
    
# ***********************book approved /reject List ************************* 
class ApproveRequestView(View):
    def get(self, request, pk):
        if request.user.role != "ADMIN":
            return redirect('dashboard')

        req = BookRequest.objects.get(pk=pk)
        req.status = "APPROVED"
        req.save()
        return redirect('request_list')


class RejectRequestView(View):
    def get(self, request, pk):
        if request.user.role != "ADMIN":
            return redirect('dashboard')

        req = BookRequest.objects.get(pk=pk)
        req.status = "REJECTED"
        req.save()
        return redirect('request_list')
    

