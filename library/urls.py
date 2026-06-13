from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from books import views
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('books/',include('books.urls')),
    path('user/',include('accounts.urls')),
    path('borrow/',include('transactions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
