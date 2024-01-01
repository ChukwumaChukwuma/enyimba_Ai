"""
URL configuration for enyimba_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# enyimba_ai/urls.py

from django.contrib import admin
from django.urls import path
from enyimba_chatbot.views import get_user_query_view  # Import the view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-user-query/', get_user_query_view, name='get_user_query'),  # Directly point to the view
    # ... other patterns ...
]
