from django.urls import path
from .views import BookCreate,BookListView,BookDetailView,BookDeleteView,BookUpdateView
from .views import RequestBookView, BookRequestListView, ApproveRequestView, RejectRequestView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('add/', BookCreate.as_view(), name='add_book'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
    path('update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    #*************bookRequest************
    path('request_book/', RequestBookView.as_view(), name='request_book'),
    path('request_list/', BookRequestListView.as_view(), name='request_list'),
    path('approve_request/<int:pk>/', ApproveRequestView.as_view(), name='approve_request'),
    path('reject_request/<int:pk>/', RejectRequestView.as_view(), name='reject_request'),
]