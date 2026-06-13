from django.urls import path
from . import views

urlpatterns = [
    # Student borrow request
    path('<int:book_id>/', views.borrow_book, name='borrow_book'),
    # Borrow List
    path('list/', views.borrow_list, name='borrow_list'),
    # Approve / Reject (Librarian / Admin)
    path('approve/<int:pk>/', views.approve_borrow, name='approve_borrow'),
    path('reject/<int:pk>/', views.reject_borrow, name='reject_borrow'),
    # Librarian/Admin return book
    path('return/<int:pk>/', views.return_book, name='return_book'),
    # Librarian/Admin manual borrow  book
    path('manual/', views.manual_borrow, name='manual_borrow'),
    # category
    path('get_books/', views.get_books_by_category, name='get_books'),
]



