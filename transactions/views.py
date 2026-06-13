from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.utils import timezone

from django.conf import settings
from .models import Book, BorrowBook
from .forms import ManualBorrowForm

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # prevent if no stock
    if book.available_copies <= 0:
        messages.error(request, "No copies available.")
        return redirect('book_list')

    BorrowBook.objects.create(
        student=request.user,
        book=book
    )

    messages.success(request, "Borrow request sent.")
    return redirect('book_list')

@login_required
def borrow_list(request):
    if request.user.role in ['LIBRARIAN', 'ADMIN']:
        borrows = BorrowBook.objects.all().order_by('-id')
    else:
        borrows = BorrowBook.objects.filter(student=request.user).order_by('-id')

    return render(request, 'borrow_list.html', {
        'borrows': borrows
    })

@login_required
def approve_borrow(request, pk):
    if request.user.role not in ['LIBRARIAN', 'ADMIN']:
        return HttpResponseForbidden()

    borrow = get_object_or_404(BorrowBook, pk=pk)

    if borrow.book.available_copies <= 0:
        messages.error(request, "No copies available.")
        return redirect('borrow_list')

    borrow.status = 'APPROVED'
    borrow.due_date = timezone.now().date() + timedelta(days=7)
    borrow.book.available_copies -= 1

    borrow.book.save()
    borrow.save()

    messages.success(request, "Borrow approved.")
    return redirect('borrow_list')

@login_required
def reject_borrow(request, pk):
    if request.user.role not in ['LIBRARIAN', 'ADMIN']:
        return HttpResponseForbidden()

    borrow = get_object_or_404(BorrowBook, pk=pk)

    # Only allow rejection if still pending
    if borrow.status != 'PENDING':
        messages.warning(request, "This request is already processed.")
        return redirect('borrow_list')

    borrow.status = 'REJECTED'
    borrow.save()

    messages.success(request, "Borrow request rejected.")
    return redirect('borrow_list')

@login_required
def return_book(request, pk):
    if request.user.role not in ['LIBRARIAN', 'ADMIN']:
        return HttpResponseForbidden()

    borrow = get_object_or_404(BorrowBook, pk=pk)

    borrow.status = 'RETURNED'
    borrow.return_date = timezone.now().date()

    # Fine calculation
    if borrow.return_date > borrow.due_date:
        late_days = (borrow.return_date - borrow.due_date).days
        borrow.fine_amount = late_days * 10  # ₹10 per day

    borrow.book.available_copies += 1
    borrow.book.save()
    borrow.save()

    messages.success(request, "Book returned successfully.")
    return redirect('borrow_list')

@login_required
def manual_borrow(request):
    if request.user.role not in ['ADMIN', 'LIBRARIAN']:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ManualBorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)

            if borrow.book.available_copies <= 0:
                messages.error(request, "No copies available.")
                return redirect('manual_borrow')

            borrow.status = 'APPROVED'
            borrow.due_date = timezone.now().date() + timedelta(days=7)
            borrow.book.available_copies -= 1

            borrow.book.save()
            borrow.save()

            messages.success(request, "Book manually issued successfully.")
            return redirect('borrow_list')
    else:
        form = ManualBorrowForm()

    return render(request, 'manual_borrow.html', {'form': form})

#category 
def get_books_by_category(request):

    category_id = request.GET.get('category_id')

    books = Book.objects.filter(
        category_id=category_id,
        available_copies__gt=0
    )

    data = []

    for book in books:
        data.append({
            "id": book.id,
            "title": book.title
        })

    return JsonResponse(data, safe=False)