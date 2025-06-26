from django.contrib import admin
from django.urls import path, include
from myapp.views import user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_login, name='root'),  # Root URL to login
    path('', include('myapp.urls')),    # Include myapp URLs
]